import regex as re
import statistics
from copy import deepcopy
from typing import List, Dict, NoReturn, Any, Tuple
from collections import defaultdict
from rara_meta_extractor.tools.utils import detect_language
from rara_meta_extractor.config import (
    LOGGER, META_FIELDS, AUTHOR_FIELDS,
    META_YEAR_FIELDS, AUTHOR_ROLES_DICT,
    TABLE_OF_CONTENTS_MIN_UPPERCASE_RATIO,
    TABLE_OF_CONTENTS_MIN_UPPERCASE_AVG_LENGTH
)
from rara_meta_extractor.constants.data_classes import (
    AuthorField, MetaField, TextBlock, DataRestrictions, MetaField, AuthorType,
    AuthorNameOrder, TitleType, TitleTypeSimple, AUTHOR_TYPES_MAP, TITLE_TYPES_MAP,
    META_FIELDS_WITH_MULTIPLE_VALUES, DEFAULT_ISSUE_TYPE, TextPartLabel
)
from rara_meta_extractor.constants.patterns import SKIP_CHARS, SKIP_WORDS

difference = lambda x, y: set(x) - set(y)

class MetaValidator:
    def __init__(self, meta_fields: List[str] = META_FIELDS,
            author_fields: List[str] = AUTHOR_FIELDS
    ) -> NoReturn:
        self.meta_fields: List[str] = meta_fields
        self.author_fields: List[str] = author_fields

    def _filter_by_length(self,
        key: str, values: List[Any], length: int, values_to_str: bool = False
    ) -> List[Any]:
        """ Filters out values not complying to length requirements.
        """
        original_values = deepcopy(values)
        filtered_values = []
        for value in values:
            if len(str(value)) == length:
                if values_to_str:
                    filtered_values.append(str(value))
                else:
                    filtered_values.append(value)
        diff = difference(original_values, filtered_values)
        if diff:
            LOGGER.debug(
                f"Removed the following values for key '{key}' not complying " \
                f" to length requirement ({length} characters): {list(diff)}"
            )
        return filtered_values

    def _remove_empty(self, key: str, values: List[Any]) -> List[Any]:
        """ Remove empty strings and "None"-s.
        """
        original_values = deepcopy(values)
        values = [
            v for v in values
            if str(v).strip() and str(v).strip() != "None"
        ]
        n_removed = len(original_values) - len(values)
        if n_removed > 0:
            LOGGER.debug(f"Removed {n_removed} empty values for key '{key}'.")
        return values

    def _get_validated_values(self, key: str, values: list,
            check_dates: bool = True
    ) -> List[Any]:
        values = self._remove_empty(key, values)

        if key == MetaField.ISBN:
            values = self._filter_by_length(
                key=key,
                values=values,
                length=DataRestrictions.ISBN_LENGTH,
                values_to_str=True
            )
        elif key == MetaField.ISSN:
            values = self._filter_by_length(
                key=key,
                values=values,
                length=DataRestrictions.ISSN_LENGTH,
                values_to_str=True
            )
        elif check_dates and key.strip() in META_YEAR_FIELDS:
            values = self._filter_by_length(
                key=key,
                values=values,
                length=DataRestrictions.YEAR_LENGTH,
                values_to_str=False
            )
        return values

    def _is_valid_key(self, key: str) -> bool:
        """ Checks, if the key is a valid key present in either
        META_FIELDS or AUTHOR_FIELDS list.
        """
        split_key = " ".join(key.split("_"))
        if key in META_FIELDS or split_key in META_FIELDS:
            return True
        if key in AUTHOR_FIELDS or split_key in AUTHOR_FIELDS:
            return True
        return False


class MetaFormatter:
    """ Formats meta
    """
    def __init__(self,
        meta_fields: List[str] = META_FIELDS,
        author_fields: List[str] = AUTHOR_FIELDS
    ) -> NoReturn:
        self.meta_validator = MetaValidator(
            meta_fields=META_FIELDS,
            author_fields=AUTHOR_FIELDS
        )

    def _filter_by_ratio(self, values: List[Tuple[Any, int]],
            n_trials: int, min_ratio: float
    ) -> List[Any]:
        """ Keeps only values that have been predicted
        in `min_ratio` trials.
        """
        filtered_values = [
            v[0] for v in values
            if float(v[1]/n_trials) >= min_ratio
        ]
        return filtered_values

    def _merge_meta(self, meta_batches: List[dict], min_ratio: float = 0.5) -> dict:
        """ Merges meta into a single dict.
        """
        LOGGER.debug("Merging and formatting metadata.")

        formatted_meta = [
            self._format_meta(meta_dict)
            for meta_dict in meta_batches
        ]
        meta = {}
        frequencies = defaultdict(lambda: defaultdict(int))
        n_trials = len(meta_batches)

        for meta_dict in formatted_meta:
            for key, values in meta_dict.items():
                for value in values:
                    frequencies[key][value]+=1

        for key, value_dict in frequencies.items():
            value_list = sorted(
                list(value_dict.items()),
                key=lambda x: x[1],
                reverse=True
            )
            meta[key] = self._filter_by_ratio(
                values=value_list,
                n_trials=n_trials,
                min_ratio=min_ratio
            )
        return meta

    def _parse_authors(self, authors_list: List[str]) -> List[str]:
        """ Parse weirdly extracted authors like:
        "Reelika RätsepMari-Liis TammikElmar Zimmer"
        """
        LOGGER.debug("Parsing authors.")
        new_authors = []
        for author in authors_list:
            parsed = re.split("(?<=[a-züõöäšž])(?=[A-ZÜÕÖÄŠŽ])", author)
            new_authors.extend(parsed)
        return new_authors

    def _parse_dates(self, values: List[str]) -> List[str]:
        parsed = []
        for value in values:
            match = re.search(r"(?<=\D)\d{4}(?=\D)", value)
            if match:
                parsed.append(match.group())
        return parsed

    def _add_missing_keys(self, meta: dict) -> dict:
        """ Adds missing meta keys.
        """
        meta_copy = deepcopy(meta)
        missing_keys = {}
        for key in META_FIELDS:
            if key not in meta:
                missing_keys[key] = []
        meta_copy.update(missing_keys)
        return meta_copy

    def _remove_empty_fields(self, meta: dict) -> dict:
        """ Removes empty fields.
        """
        new_meta = {}
        for key, values in meta.items():
            if values:
                new_meta[key] = values
        return new_meta

    def _format_meta(self, meta: dict, check_dates: bool = False) -> dict:
        """ Format meta.
        """
        formatted_meta = {}
        for key, values in list(meta.items()):
            key = key.strip()
            if not self.meta_validator._is_valid_key(key):
                LOGGER.error(
                    f"Detected an invalid key '{key}'. " \
                    f"This will NOT be added to the output."
                )
                continue
            values = self.meta_validator._get_validated_values(
                key=key, values=values, check_dates=check_dates
            )
            if values:
                if key in AUTHOR_FIELDS:
                    formatted_meta[key] = self._parse_authors(values)
                elif key in META_YEAR_FIELDS:
                    formatted_meta[key] = self._parse_dates(values)
                else:
                    formatted_meta[key] = values
        return formatted_meta


    def _format_authors(self, meta: dict, simple: bool = False) -> dict:
        """ Convert authors from a flat structure into
        a list of dicts.
        """
        LOGGER.debug("Formatting authors.")
        new_meta = {MetaField.AUTHORS: []}#, "main_author": ""}
        for key, values in list(meta.items()):
            if key in AUTHOR_FIELDS:
                for i, value in enumerate(values):
                    if i == 0 and key == AuthorField.AUTHOR:
                        is_primary = True
                    else:
                        is_primary = False
                    new_author = Author(
                        name=value,
                        role=key,
                        is_primary=is_primary
                    ).to_dict(simple=simple)
                    new_meta["authors"].append(new_author)
            else:
                new_meta[key] = values
        return new_meta


class Author:
    def __init__(self, name: str, role: str, is_primary: bool, author_type: str = AuthorType.UNK,
            unknown_role: str = AuthorField.UNKNOWN, map_role: bool = True,
            author_name_order: int = AuthorNameOrder.FIRST_NAME_FIRST
    ):
        self.name: str = name
        self.is_primary: bool = is_primary
        self.en_role: str = role
        self.et_role: str = AUTHOR_ROLES_DICT.get(self.en_role, unknown_role) if map_role else role
        self.author_type: str = AUTHOR_TYPES_MAP.get(author_type, AuthorType.UNK)
        self.author_name_order: int = author_name_order

    @staticmethod
    def is_false_positive(author_name: str, max_n_words: int = 7,
            max_length: int = 50
    ) -> bool:
        """ Author names detected from EPUBs might sometimes
        contain just a long free form text like:
        'E-raamatu teostus Ants Tuur / www.flagella.ee '
        '- Kvaliteetsed eraamatu lahendused.'
        """
        name_tokens = [
            token.strip()
            for token in author_name.split()
            if token.strip()
        ]
        if len(name_tokens) > max_n_words or len(author_name) > max_length:
            return True
        return False


    def to_dict(self, simple: bool = False) -> dict:
        if simple:
            author_dict = {
                "name": self.name,
                "role": self.et_role
            }
        else:
            author_dict = {
                "is_primary": self.is_primary,
                "name": self.name,
                "role": self.et_role,
                "type": self.author_type,
                "name_order": self.author_name_order
            }
        return author_dict

class Title:
    def __init__(self, titles: List[str], lang: str = "",
        part_number: str = "", title_type: str = ""
    ):
        self.titles = titles
        self.lang = lang
        self.part_number = part_number
        self.title_type = title_type

    @staticmethod
    def find_skip(title: str) -> int:
        """ Number of chars that should not be included into search,
        e.g. Articles like 'the', 'an', various punctuation chars etc.
        """
        skip = 0
        skip_pattern = rf"^(([{SKIP_CHARS}]|({'|'.join(SKIP_WORDS)})\s)\s*)+(?=\S)"
        match = re.search(skip_pattern, title, re.IGNORECASE)
        if match:
            skip = len(match.group())
        return skip

    def _get_title_type(self, i: int, simple: bool) -> str:
        if self.title_type:
            return self.title_type
        if simple:
            title_type_class = TitleTypeSimple
        else:
            title_type_class = TitleType
        if i == 0:
            title_type = title_type_class.TITLE
        if i >= 1:
            title_type = title_type_class.ADDITIONAL_TITLE
        return title_type

    def to_dicts(self, simple: bool = False) -> List[dict]:
        formatted = []
        for i, title in enumerate(self.titles):
            if i > 1 and not simple:
                break

            title_type = self._get_title_type(i=i, simple=simple)
            title_type_int = TITLE_TYPES_MAP.get(title_type, None)
            skip = Title.find_skip(title)
            title_language = detect_language(title) if not self.lang else self.lang

            if not simple:
                title_dict = {
                    "title": title,
                    "title_language": title_language,
                    "part_number": self.part_number,
                    "part_title": "",
                    "version": "",
                    "author_from_title": "",
                    "skip": skip,
                    "title_type": title_type,
                    "title_type_int": title_type_int
                }
            else:
                title_dict = {
                    "title": title,
                    "title_type": title_type
                }
            formatted.append(title_dict)
        return formatted

class TextPart:
    def __init__(self, text_type: str, text_value: str, language: str = ""):
        self.text_type = text_type
        self.text_value = text_value
        self.language = language if language else detect_language(text_value)

    def to_dict(self) -> dict:
        text_part_dict = {
            "text_type": self.text_type,
            "text_value": self.text_value,
            "language": self.language
        }
        return text_part_dict

class Meta:
    def __init__(self, meta_batches: List[dict], text_parts: List[dict], min_ratio: float = 0.8,
        add_missing_keys: bool = False, simple: bool = False, language: str = ""
    ) -> NoReturn:
        self.meta_batches: List[dict] = meta_batches
        self.text_parts: List[dict] = text_parts
        self.min_ratio: float = min_ratio
        self.add_missing_keys: bool = add_missing_keys
        self.simple: bool = simple
        self.language: str = language

        self.meta_formatter: MetaFormatter = MetaFormatter(
            meta_fields = META_FIELDS,
            author_fields = AUTHOR_FIELDS
        )

        self.__merged_meta: dict = {}
        self.__meta_with_reformatted_authors: dict = {}
        self.__meta_with_all_keys: dict = {}
        self.__meta_without_empty_fields: dict = {}

    @property
    def merged_meta(self) -> dict:
        if not self.__merged_meta:
            self.__merged_meta = self.meta_formatter._merge_meta(
                meta_batches=self.meta_batches,
                min_ratio=self.min_ratio
            )
        return self.__merged_meta

    @property
    def meta_with_reformatted_authors(self):
        if not self.__meta_with_reformatted_authors:
            self.__meta_with_reformatted_authors = self.meta_formatter._format_authors(
                meta=self.merged_meta, simple=self.simple
            )
        return self.__meta_with_reformatted_authors

    @property
    def meta_with_all_keys(self):
        if not self.__meta_with_all_keys:
            self.__meta_with_all_keys = self.meta_formatter._add_missing_keys(
                meta=self.meta_without_empty_fields
            )
        return self.__meta_with_all_keys

    @property
    def meta_without_empty_fields(self):
        if not self.__meta_without_empty_fields:
            self.__meta_without_empty_fields = self.meta_formatter._remove_empty_fields(
                meta=self.meta_with_reformatted_authors
            )
        return self.__meta_without_empty_fields

    def _concat(self, meta: dict) -> dict:
        concatted = {}
        for key, value in meta.items():
           key_tokens = key.split()
           new_key = "_".join(key_tokens)
           concatted[new_key] = value
        return concatted

    @staticmethod
    def update_field_types(meta_dict: dict, empty_value: Any = "",
            custom_keys_to_ignore: List[str] = []
    ) -> dict:
        keys_to_ignore = [MetaField.TITLES, MetaField.AUTHORS, MetaField.TEXT_PARTS]
        keys_to_ignore.extend(META_FIELDS_WITH_MULTIPLE_VALUES)
        keys_to_ignore.extend(custom_keys_to_ignore)
        for key, values in list(meta_dict.items()):
            if key not in keys_to_ignore:
                if not isinstance(values, list):
                    continue
                if values:
                    meta_dict[key] = values[0]
                else:
                    meta_dict[key] = empty_value
        return meta_dict

    def to_dict(self):
        if self.add_missing_keys:
            meta_dict = self._concat(self.meta_with_all_keys)
        else:
            meta_dict = self._concat(self.meta_without_empty_fields)
        if self.text_parts or self.add_missing_keys:
            meta_dict[MetaField.TEXT_PARTS] = self.text_parts
        if MetaField.TITLES in meta_dict:
            titles = meta_dict.pop(MetaField.TITLES)
            formatted_titles = Title(titles=titles, lang=self.language).to_dicts(simple=self.simple)
            meta_dict[MetaField.TITLES] = formatted_titles

        meta_dict = Meta.update_field_types(meta_dict)
        # Hotfix
        keys_to_remove = ["country_from_008", "unknown"]
        new_dict = {}
        for key, values in meta_dict.items():
            if key not in keys_to_remove:
                new_dict[key] = values
        meta_dict = new_dict

        # Always add issue type (bib style):
        if MetaField.ISSUE_TYPE not in meta_dict:
            meta_dict[MetaField.ISSUE_TYPE] = DEFAULT_ISSUE_TYPE

        return meta_dict

class TableOfContents:
    def __init__(self, extracted_meta: dict):
        self.__chapters: List[str] = []
        self.__table_of_contents_str: str = ""
        self._text_parts: List[dict] = extracted_meta.get(MetaField.TEXT_PARTS, [])


    def _filter_by_case(self, chapters: List[str],
            min_ratio: float = TABLE_OF_CONTENTS_MIN_UPPERCASE_RATIO,
            min_avg_length: int = TABLE_OF_CONTENTS_MIN_UPPERCASE_AVG_LENGTH
    ) -> List[str]:
        """ If some titles are in uppercase and others are not,
        assume that the lower-case titles are false positives
        and filter them out.
        """
        chapter_stats = {
            "upper": [],
            "other": [],
            "upper_lens": [],
            "other_lens": []
        }
        out = chapters
        for chapter in chapters:
            if chapter.upper() == chapter:
                chapter_stats["upper"].append(chapter)
                chapter_stats["upper_lens"].append(len(chapter))
            else:
                chapter_stats["other"].append(chapter)
                chapter_stats["other_lens"].append(len(chapter))
        if chapters and len(chapter_stats["upper"])/len(chapters) >= min_ratio:
            if statistics.mean(chapter_stats["upper_lens"]) >= min_avg_length:
                out = chapter_stats["upper"]
        return out


    @property
    def table_of_contents_str(self) -> str:
        if not self.__table_of_contents_str:
            for text_part in self._text_parts:
                text_type = text_part.get("text_type", "")
                if text_type == TextPartLabel.TABLE_OF_CONTENTS:
                    self.__table_of_contents_str = text_part.get("text_value", "")
        return self.__table_of_contents_str

    @property
    def table_of_contents(self) -> List[str]:
        """ Extract chapter names from table of contents.
        """
        if not self.__chapters:
            raw_chapters = self.table_of_contents_str.split("\n")
            _chapters = [
                chapter.strip()
                for chapter in raw_chapters
                if chapter.strip()
            ]
            self.__chapters = self._filter_by_case(_chapters)
        return self.__chapters

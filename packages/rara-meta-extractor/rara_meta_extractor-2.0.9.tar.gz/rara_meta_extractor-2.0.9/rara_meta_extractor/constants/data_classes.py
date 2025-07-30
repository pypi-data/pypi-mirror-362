from dataclasses import dataclass

@dataclass(frozen=True)
class TextBlock:
    REGULAR: str = "regular text block"
    METADATA: str = "metadata text block"
    TITLE_PAGE: str = "title page"
    ABSTRACT: str = "abstract text block"
    SUMMARY: str = "summary text block"


@dataclass(frozen=True)
class IssueType:
    NEWSPAPER: str = "Ajaleht"
    JOURNAL: str = "Ajakiri"
    PERIODICAL: str = "Jätkväljaanne"
    BOOK: str = "Raamat"

@dataclass(frozen=True)
class ExtractorType:
    LLAMA: str = "Llama-Extractor"
    EPUB: str = "EPUB-Extractor"
    METS_ALTO: str = "METS/ALTO-Extractor"

@dataclass(frozen=True)
class TextPartLabel:
    TABLE_OF_CONTENTS: str = "Sisukord"
    ABSTRACT: str = "Abstrakt"
    CONCLUSION: str = "Kokkuvõte"
    OTHER: str = "Muu"

@dataclass(frozen=True)
class AuthorField:
    AUTHOR: str = "author"
    UNKNOWN: str = "Teadmata"

@dataclass(frozen=True)
class AuthorType:
    PER: str = "PER"
    ORG: str = "ORG"
    UNK: str = ""


@dataclass(frozen=True)
class TitleType:
    AUTHOR_WITHOUT_TITLE: str = "pealkirjata autor"
    NORMALIZED_TITLE: str = "normitud eelispealkiri"
    TITLE: str = "väljaandes esitatud kujul põhipealkiri"
    ADDITIONAL_TITLE: str = "rööppealkiri"
    METS_TITLE: str = "väljaandes esitatud kujul põhipealkiri"

@dataclass(frozen=True)
class TitleTypeSimple:
    TITLE: str = "main_title"
    ADDITIONAL_TITLE: str = "additional_title_part"
    METS_TITLE: str = "article_or_chapter_title"

@dataclass(frozen=True)
class AuthorNameOrder:
    FIRST_NAME_FIRST: int = 0
    LAST_NAME_FIRST: int = 1
    FAMILY_NAME_FIRST: int = 3

@dataclass(frozen=True)
class DataRestrictions:
    ISBN_LENGTH: int = 13
    ISSN_LENGTH: int = 8
    YEAR_LENGTH: int = 4

@dataclass(frozen=True)
class MetaYearField:
    DISTRIBUTION_DATE: str = "distribution date"
    PUBLICATION_DATE: str = "publication date"
    MANUFACTURE_DATE: str = "manufacture date"


@dataclass(frozen=True)
class MetaField:
    TITLES: str = "titles"
    SUBTITLE: str = "subtitle"
    ISBN: str = "isbn"
    ISSN: str = "issn"
    EDITION_INFO: str = "edition info/number"
    DISTRIBUTION_PLACE: str = "distribution_place"
    DISTRIBUTER_NAME: str = "distributer name"
    DISTRIBUTION_DATE: str = "distribution date"
    MANUFACTURE_DATE: str = "manufacture date"
    MANUFACTURER: str = "manufacturer"
    MANUFACTURE_PLACE: str = "manufacture place"
    PUBLICATION_DATE: str = "publication date"
    PUBLISHER: str = "publisher"
    PUBLICATION_PLACE: str = "publication place"
    SUMMARY_LANG: str = "summary or abstract language"
    TOC_LANG: str = "table of contents language"
    ORIGINAL_LANG: str = "language original"
    COUNTRY_FROM_008: str = "country from 008"
    TEXT_TYPE: str = "text_type"
    AUTHORS: str = "authors"
    TEXT_PARTS: str = "text_parts"
    ISSUE_TYPE: str = "issue_type"
    UDK: str = "udk"
    UDC: str = "udc"
    UNK: str = "unknown"
    INCLUDED_TEXT: str = "description"
    TABLE_OF_CONTENTS: str = "table_of_contents"
    SECTIONS: str = "sections"

TITLE_TYPES_MAP = {
    TitleType.AUTHOR_WITHOUT_TITLE: 130,
    TitleType.NORMALIZED_TITLE: 240,
    TitleType.TITLE: 245,
    TitleType.ADDITIONAL_TITLE: 246,
    TitleType.METS_TITLE: 245
}


ISSUE_STYLE_MAP = {
    "newspaper": IssueType.NEWSPAPER,
    "ajalehed": IssueType.NEWSPAPER,
    "journal": IssueType.JOURNAL,
    "ajakirjad": IssueType.JOURNAL,
    "periodical": IssueType.PERIODICAL,
    "jätkväljanded": IssueType.PERIODICAL,
    "books": IssueType.BOOK,
    "raamatud": IssueType.BOOK
}
AUTHOR_TYPES_MAP = {"personal": AuthorType.PER}

DEFAULT_ISSUE_TYPE = IssueType.BOOK

TEXT_BLOCKS = [v for v in vars(TextBlock()).values()]
META_YEAR_FIELDS = [v for v in vars(MetaYearField()).values()]

META_FIELDS_WITH_MULTIPLE_VALUES = [MetaField.ISBN, MetaField.ISSN, MetaField.UDK, MetaField.UDC]

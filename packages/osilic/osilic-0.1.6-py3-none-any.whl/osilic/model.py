from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from tabulate import tabulate
import textwrap


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Keyword(Enum):
    INTERNATIONAL = "international"
    NON_REUSABLE = "non-reusable"
    OTHER_MISCELLANEOUS = "other-miscellaneous"
    POPULAR_STRONG_COMMUNITY = "popular-strong-community"
    REDUNDANT_WITH_MORE_POPULAR = "redundant-with-more-popular"
    SPECIAL_PURPOSE = "special-purpose"
    SUPERSEDED = "superseded"
    UNCATEGORIZED = "uncategorized"
    VOLUNTARILY_RETIRED = "voluntarily-retired"


@dataclass
class Collection:
    href: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        assert isinstance(obj, dict)
        href = from_union([from_str, from_none], obj.get("href"))
        return Collection(href)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.href is not None:
            result["href"] = from_union([from_str, from_none], self.href)
        return result


@dataclass
class Links:
    links_self: Optional[Collection] = None
    html: Optional[Collection] = None
    collection: Optional[Collection] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Links':
        assert isinstance(obj, dict)
        links_self = from_union([Collection.from_dict, from_none], obj.get("self"))
        html = from_union([Collection.from_dict, from_none], obj.get("html"))
        collection = from_union([Collection.from_dict, from_none], obj.get("collection"))
        return Links(links_self, html, collection)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.links_self is not None:
            result["self"] = from_union([lambda x: to_class(Collection, x), from_none], self.links_self)
        if self.html is not None:
            result["html"] = from_union([lambda x: to_class(Collection, x), from_none], self.html)
        if self.collection is not None:
            result["collection"] = from_union([lambda x: to_class(Collection, x), from_none], self.collection)
        return result


@dataclass
class License:
    id: Optional[str] = None
    name: Optional[str] = None
    spdx_id: Optional[str] = None
    version: Optional[str] = None
    submission_date: Optional[str] = None
    submission_url: Optional[str] = None
    submitter_name: Optional[str] = None
    approved: Optional[bool] = None
    approval_date: Optional[str] = None
    license_steward_version: Optional[str] = None
    license_steward_url: Optional[str] = None
    board_minutes: Optional[str] = None
    stewards: Optional[List[str]] = None
    keywords: Optional[List[Keyword]] = None
    links: Optional[Links] = None

    @staticmethod
    def from_dict(obj: Any) -> 'License':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        spdx_id = from_union([from_str, from_none], obj.get("spdx_id"))
        version = from_union([from_str, from_none], obj.get("version"))
        submission_date = from_union([from_str, from_none], obj.get("submission_date"))
        submission_url = from_union([from_str, from_none], obj.get("submission_url"))
        submitter_name = from_union([from_str, from_none], obj.get("submitter_name"))
        approved = from_union([from_bool, from_none], obj.get("approved"))
        approval_date = from_union([from_str, from_none], obj.get("approval_date"))
        license_steward_version = from_union([from_str, from_none], obj.get("license_steward_version"))
        license_steward_url = from_union([from_str, from_none], obj.get("license_steward_url"))
        board_minutes = from_union([from_str, from_none], obj.get("board_minutes"))
        stewards = from_union([lambda x: from_list(from_str, x), from_none], obj.get("stewards"))
        keywords = from_union([lambda x: from_list(Keyword, x), from_none], obj.get("keywords"))
        links = from_union([Links.from_dict, from_none], obj.get("_links"))
        return License(id, name, spdx_id, version, submission_date, submission_url, submitter_name, approved, approval_date, license_steward_version, license_steward_url, board_minutes, stewards, keywords, links)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.spdx_id is not None:
            result["spdx_id"] = from_union([from_str, from_none], self.spdx_id)
        if self.version is not None:
            result["version"] = from_union([from_str, from_none], self.version)
        if self.submission_date is not None:
            result["submission_date"] = from_union([from_str, from_none], self.submission_date)
        if self.submission_url is not None:
            result["submission_url"] = from_union([from_str, from_none], self.submission_url)
        if self.submitter_name is not None:
            result["submitter_name"] = from_union([from_str, from_none], self.submitter_name)
        if self.approved is not None:
            result["approved"] = from_union([from_bool, from_none], self.approved)
        if self.approval_date is not None:
            result["approval_date"] = from_union([from_str, from_none], self.approval_date)
        if self.license_steward_version is not None:
            result["license_steward_version"] = from_union([from_str, from_none], self.license_steward_version)
        if self.license_steward_url is not None:
            result["license_steward_url"] = from_union([from_str, from_none], self.license_steward_url)
        if self.board_minutes is not None:
            result["board_minutes"] = from_union([from_str, from_none], self.board_minutes)
        if self.stewards is not None:
            result["stewards"] = from_union([lambda x: from_list(from_str, x), from_none], self.stewards)
        if self.keywords is not None:
            result["keywords"] = from_union([lambda x: from_list(lambda x: to_enum(Keyword, x), x), from_none], self.keywords)
        if self.links is not None:
            result["_links"] = from_union([lambda x: to_class(Links, x), from_none], self.links)
        return result


def license_from_dict(s: Any) -> List[License]:
    return from_list(License.from_dict, s)


def license_to_dict(x: List[License]) -> Any:
    return from_list(lambda x: to_class(License, x), x)


def print_licenses_table(licenses: List[License], width: int = 45) -> None:
    """
    Print a list of License objects in a nicely formatted table, wrapping long text fields except Links.
    Excludes Submission URL and Board Minutes columns.
    """
    headers = [
        "ID", "Name", "SPDX ID", "Approved", "Keywords", "Links"
    ]
    table = []
    for lic in licenses:
        links_str = str(lic.links) if lic.links else ""
        links_str = "\n".join([part.strip() for part in links_str.split(",")]) if links_str else ""
        row = [
            lic.id or "",
            lic.name or "",
            lic.spdx_id or "",
            str(lic.approved) if lic.approved is not None else "",
            ", ".join([k.value for k in lic.keywords]) if lic.keywords else "",
            links_str
        ]
        # Wrap each cell except Links
        row = ["\n".join(textwrap.wrap(str(cell), width)) if i != 5 and len(str(cell)) > width else str(cell) for i, cell in enumerate(row)]
        table.append(row)
    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_license_details_table(license: License, width: int = 45) -> None:
    """
    Print all fields of a single License object vertically in a table, wrapping long text fields except Links, Submission URL, and Board Minutes.
    """
    links_str = str(license.links) if license.links else ""
    links_str = "\n".join([part.strip() for part in links_str.split(",")]) if links_str else ""
    fields = [
        ("ID", license.id),
        ("Name", license.name),
        ("SPDX ID", license.spdx_id),
        ("Version", license.version),
        ("Submission Date", license.submission_date),
        ("Submission URL", license.submission_url),
        ("Submitter Name", license.submitter_name),
        ("Approved", str(license.approved) if license.approved is not None else ""),
        ("Approval Date", license.approval_date),
        ("License Steward Version", license.license_steward_version),
        ("License Steward URL", license.license_steward_url),
        ("Board Minutes", license.board_minutes),
        ("Stewards", ", ".join(license.stewards) if license.stewards else ""),
        ("Keywords", ", ".join([k.value for k in license.keywords]) if license.keywords else ""),
        ("Links", links_str)
    ]
    # Wrap values if needed, except Links, Submission URL, Board Minutes
    wrapped_fields = [
        (name, value if name in ["Links", "Submission URL", "Board Minutes"] else ("\n".join(textwrap.wrap(str(value), width)) if value and len(str(value)) > width else str(value) if value else ""))
        for name, value in fields
    ]
    print(tabulate(wrapped_fields, headers=["Field", "Value"], tablefmt="grid"))

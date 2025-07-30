"""Utilities to help maintain and use the Produksjonstilskudd codelist.

Uses a registry pattern to build the Produksjonstilskudd codelist based on all currently created Produksjonskode objects, as they add themselves to the _registry list as they are created.
"""

import logging
import re
from typing import ClassVar

logger = logging.getLogger(__name__)

VALID_MEASUREMENT_UNITS = {"antall", "dekar", "stykk", "kilo"}


class Produksjonstilskudd:
    """A service class for retrieving production codes by various criteria.

    This class provides methods for filtering and retrieving registered
    production codes (Produksjonskode objects) based on categories or
    measurement units.
    """

    def __init__(self: "Produksjonstilskudd") -> None:
        """Initializes the codelist from the Produksjonskode registry.

        This sets the `self.codes` attribute to all currently registered
        `Produksjonskode` instances. It also compiles a sorted list of unique
        categories into `self.categories`.
        """
        logger.debug("Instantiating Produksjonstilskudd.")
        self.codes = Produksjonskode._registry

        logger.debug(f"Contains {len(self.codes)} different codes")

        categories = set()
        for code in self.codes:
            for group in code.groups:
                categories.add(group)
        self.categories = list(sorted(categories))
        logger.debug(
            f"Added {len(self.categories)} categories to the instance.\nCategories: {self.categories}"
        )

    @staticmethod
    def _add_prefix(list_containing_codes: list[str]) -> list[str]:
        """Adds a 'pk_' prefix to each code in the provided list.

        Args:
            list_containing_codes (List[str]): A list of production code strings.

        Returns:
            List[str]: A new list of code strings prefixed with 'pk_'.
        """
        return [f"pk_{x}" for x in list_containing_codes]

    def get_codes(
        self: "Produksjonstilskudd",
        categories: str | list[str] | None = None,
        prefix: bool = False,
    ) -> list[str]:
        """Retrieves production codes filtered by the specified categories.

        - If `categories` is None, the method returns codes from all categories.
        - If `categories` is a string, it is converted into a single-element list.
        - If `prefix` is True, each returned code is prefixed with 'pk_'.

        Args:
            categories (Union[str, List[str], None], optional): Categories to filter by.
                Can be a single category (str), a list of categories, or None.
                Defaults to None, meaning use all categories.
            prefix (bool): Whether to prefix each code with 'pk_'.
                Defaults to False.

        Raises:
            TypeError: If `prefix` is not a bool or `categories` is not a str, list, or None.

        Returns:
            List[str]: A list of matching production codes (optionally prefixed).
        """
        # Input validation
        if not isinstance(prefix, bool):
            raise TypeError(f"prefix should be either True or False, received {prefix}")
        if categories is None:
            categories = self.categories
        if isinstance(categories, str):
            categories = [categories]
        if not isinstance(categories, list):
            raise TypeError(
                f"Received object of type {type(categories)}, expected type str or list."
            )

        # Get the requested codes
        relevant_codes = []

        for code in self.codes:
            if any(group in categories for group in code.groups):
                relevant_codes.append(code)

        list_of_codes = [x.code for x in relevant_codes]

        if prefix:
            list_of_codes = self._add_prefix(list_of_codes)

        return list_of_codes

    def get_codes_by_measurement(
        self: "Produksjonstilskudd", measurement: str, prefix: bool = False
    ) -> list[str]:
        """Retrieves production codes that match a specific measurement unit.

        - If `prefix` is True, each returned code is prefixed with 'pk_'.

        Args:
            measurement (str): The measurement unit to filter by (e.g., 'antall').
            prefix (bool): Whether to prefix each code with 'pk_'.
                Defaults to False.

        Raises:
            ValueError: If the `measurement` is not one of the valid measurement units.
            TypeError: If `prefix` is not a bool.

        Returns:
            List[str]: A list of production codes (optionally prefixed) that match
            the given measurement unit.
        """
        if measurement not in VALID_MEASUREMENT_UNITS:
            raise ValueError(
                f"Invalid measurement unit: {measurement}. Must be one of {VALID_MEASUREMENT_UNITS}"
            )
        if not isinstance(prefix, bool):
            raise TypeError(f"prefix should be either True or False, received {prefix}")

        relevant_codes = []

        for code in self.codes:
            if code.measured_in == measurement:
                relevant_codes.append(code)

        list_of_codes = [x.code for x in relevant_codes]

        if prefix:
            list_of_codes = self._add_prefix(list_of_codes)

        return list_of_codes

    def __str__(self: "Produksjonstilskudd") -> str:
        """Provides a string representation of the Produksjonstilskudd object.

        Returns:
            str: A summary of the number of codes and categories registered.
        """
        return f"Produksjonstilskudd object with {len(self.codes)} Produksjonskoder registered.\nCodes are organized in a total of {len(self.categories)} categories."


class Produksjonskode:
    """Represents a production code used in agricultural classification.

    When initialized, each instance is automatically registered in the class-level
    registry `_registry` for use by `Produksjonstilskudd`.

    Attributes:
        code (str): A 3-digit production code (e.g., "101").
        label (str): The human-readable name of the production code.
        groups (List[str]): A list of categories this production code belongs to.
        measured_in (str): The unit of measurement (e.g., "antall", "dekar").
        description (Optional[str]): A textual description of the production code.
        valid_from (Optional[str]): The year from which the code is valid.
        valid_to (Optional[str]): The year until which the code is valid.
        replaces (List[str]): A list of production codes that this code replaces.
        replaced_by (List[str]): A list of production codes that replace this code.

    Raises:
        ValueError: If `code` is not exactly 3 digits.
        TypeError: If `groups` is not a list.
        ValueError: If any value in `groups` is not a string.
        ValueError: If `measured_in` is not in the set of valid measurement units.

    Example:
        >>> kode = Produksjonskode(
        ...     code="101",
        ...     label="Melkeku",
        ...     groups=["Storfe"],
        ...     measured_in="antall",
        ...     description="Melkekyr for produksjon"
        ... )
        >>> print(kode.code)
        101
    """

    _registry: ClassVar[list["Produksjonskode"]] = []

    def __init__(
        self: "Produksjonskode",
        code: str,
        label: str,
        groups: list[str],
        measured_in: str,
        description: str | None = None,
        valid_from: str | None = None,
        valid_to: str | None = None,
        replaces: list[str] | None = None,
        replaced_by: list[str] | None = None,
    ) -> None:
        """Initializes a Produksjonskode instance and registers it.

        Also performs a validation check using self.is_valid()

        Args:
            code (str): A 3-digit code, e.g. "101".
            label (str): A descriptive label, e.g. "Melkeku".
            groups (List[str]): A list of categories (e.g. ["Storfe"]).
            measured_in (str): The measurement unit, must be one of {"antall", "dekar", "stykk", "kilo"}.
            description (str | None, optional): An optional textual description. Defaults to None.
            valid_from (str | None, optional): The start year of validity. Defaults to None.
            valid_to (str | None, optional): The end year of validity. Defaults to None.
            replaces (List[str] | None, optional): List of codes this one replaces. Defaults to None.
            replaced_by (List[str] | None, optional): List of codes that replace this one. Defaults to None.
        """
        self.code = code
        self.label = label
        self.description = description if description else ""
        self.valid_from = valid_from if valid_from else None
        self.valid_to = valid_to if valid_to else None
        self.replaces = replaces if replaces else []
        self.replaced_by = replaced_by if replaced_by else []
        self.groups = groups if groups else []
        self.measured_in = measured_in

        self.is_valid()

        Produksjonskode._registry.append(self)  # Registers itself in the registry

        logger.debug(f"Instantiated code:\n{self}")

    def is_valid(self: "Produksjonskode") -> None:
        """Validates the Produksjonskode fields.

        Raises:
            ValueError: If `code` is not a 3-digit string.
            TypeError: If `groups` is not a list.
            ValueError: If any item in `groups` is not a string.
            ValueError: If `measured_in` is invalid.
        """
        if not re.fullmatch(r"\d{3}", self.code):  # Checks that the code is 3 digits.
            raise ValueError(
                f"Invalid code: {self.code}. Must be exactly 3 digits (e.g., '101')."
            )

        if not isinstance(self.groups, list):
            raise TypeError(f"Invalid type: {type(self.groups)}. groups must be a list")

        _invalid_values = [value for value in self.groups if not isinstance(value, str)]
        if _invalid_values:
            raise ValueError(
                f"All values in groups must be strings. Invalid values: {_invalid_values}"
            )

        if self.measured_in not in VALID_MEASUREMENT_UNITS:
            raise ValueError(
                f"Invalid measurement unit: {self.measured_in}. Must be one of {VALID_MEASUREMENT_UNITS}"
            )

    def __str__(self: "Produksjonskode") -> str:
        """Returns a human-readable string representation of the object.

        Returns:
            str: Formatted string with code details.
        """
        return (
            f"Produksjonskode:\n"
            f"  Code: {self.code}\n"
            f"  Label: {self.label}\n"
            f"  Valid From: {self.valid_from}\n"
            f"  Valid To: {self.valid_to if self.valid_to else 'N/A'}\n"
            f"  Replaces: {', '.join(self.replaces) if self.replaces else 'None'}\n"
            f"  Replaced By: {', '.join(self.replaced_by) if self.replaced_by else 'None'}\n"
            f"  Groups: {', '.join(self.groups) if self.groups else 'None'}\n"
            f"  Measured In: {self.measured_in if self.measured_in else 'N/A'}"
        )

    def __repr__(self: "Produksjonskode") -> str:
        """Returns a detailed string representation for debugging.

        Returns:
            str: Debug-oriented string with all relevant fields.
        """
        return (
            f"Produksjonskode("
            f"code={self.code!r}, label={self.label!r}, "
            f"valid_from={self.valid_from!r}, valid_to={self.valid_to!r}, "
            f"replaces={self.replaces!r}, replaced_by={self.replaced_by!r}, "
            f"groups={self.groups!r}, measured_in={self.measured_in!r})"
        )


"""Add the codes below by creating instances of the class Produksjonskode.

Copy paste this template and fill it with information.
Produksjonskode(
    code="",
    label="",
    description="",
    groups=[""],
    measured_in="antall",
)

When created they add themselves to the registry, making maintenance simpler.
"""

Produksjonskode(
    code="001",
    label="Epler",
    description="Avling av epler",
    groups=["frukt", "frukt avling"],
    measured_in="kilo",
)


Produksjonskode(
    code="272",
    label="Epler",
    description="Areal med epler",
    groups=["frukt", "frukt areal"],
    measured_in="dekar",
)

Produksjonskode(
    code="002",
    label="Pærer",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="273",
    label="Pærer",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="006",
    label="Epler og pærer til press",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="003",
    label="Plommer",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="274",
    label="Plommer",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="004",
    label="Moreller",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="005",
    label="Kirsebær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="011",
    label="Jordbær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="012",
    label="Bringebær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="013",
    label="Solbær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="014",
    label="Rips",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="016",
    label="Hageblåbær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="021",
    label="Stikkelsbær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="022",
    label="Industribær",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="031",
    label="Tomat",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="032",
    label="Slangeagurk",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="033",
    label="Salat (også friland)",
    description="",
    groups=[""],
    measured_in="stykk",
)

Produksjonskode(
    code="060",
    label="Matpoteter i Nord-Norge",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="115",
    label="Hester, under 3 år",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="116",
    label="Hester, 3 år og eldre",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="118",
    label="Ammekyr av minst 50% kjøttferase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="119",
    label="Øvrige storfe",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="120",
    label="Melkekyr",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="121",
    label="Ammekyr",
    description="",
    groups=[""],
    measured_in="antall",
)


Produksjonskode(
    code="139",
    label="Melkesau",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="140",
    label="Melkegeiter",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="142",
    label="Ammegeiter",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="144",
    label="Bukker og ungdyr, medregnet kje",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="145",
    label="Søyer født i fjor eller tidligere",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="146",
    label="Værer født i fjor eller tidligere",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="154",
    label="Smågriser, levendevekt under 20kg eller alder inntil 8 uker",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="155",
    label="Avlspurker som har fått minst 1 kull",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="156",
    label="Råner som er satt inn i avl",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="157",
    label="Slaktegriser, levendevekt minst 20kg",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="158",
    label="Ungpurker bestemt for avl",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="159",
    label="Ungråner bestemt for avl",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="161",
    label="Verpehøner",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="162",
    label="Rugeegg levert til rugeri",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="168",
    label="Avlsdyr av ender, kalkuner og gjess",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="170",
    label="Minktisper",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="171",
    label="Revetisper",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="174",
    label="Ender, kalkuner og gjess for slakt",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="175",
    label="Livkyllinger",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="176",
    label="Slaktekyllinger",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="178",
    label="Hjort, 1 år og eldre",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="179",
    label="Hjort, under 1 år",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="180",
    label="Kaniner",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="181",
    label="Griser solgt som livdyr, vekt på minst 50 kg",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="183",
    label="Struts",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="185",
    label="Kyllinger og kalkuner solgt som livdyr",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="192",
    label="Esel",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="193",
    label="Hester i pensjon i beitesesongen",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="194",
    label="Bifolk",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="196",
    label="Lama",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="197",
    label="Alpakka",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="210",
    label="Fylldyrket eng",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="211",
    label="Overflatedyrket eng",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="212",
    label="Innmarksbeite",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="213",
    label="Andre grovforvekster til for",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="223",
    label="Grønngjødsling",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="230",
    label="Poteter",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="231",
    label="Annet korn og frø som er berettiget tilskudd",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="235",
    label="Engfør og annen såfrøproduksjon",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="236",
    label="Erter, bønner og andre belgvekster til modning",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="237",
    label="Oljevekster",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="238",
    label="Rug og rughvete",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="239",
    label="Korn til krossing",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="240",
    label="Vårhvete",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="242",
    label="Bygg",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="243",
    label="Havre",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="245",
    label="Erter og bønner til konserveindustri (høstet før modning)",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="247",
    label="Høsthvete",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="264",
    label="Grønnsaker på friland, inkl. matkålrot og urter",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="271",
    label="Moreller og kirsebær",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="280",
    label="Jordbær",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="282",
    label="Andre bærarter",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="283",
    label="Andre fruktarter",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="285",
    label="Planteskoleareal og blomsterdyrking på friland",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="290",
    label="Brakka areal",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="292",
    label="Fulldyrket og/eller overflatedyrket, ute av drift",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="293",
    label="Innmarksbeite, ute av drift",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="294",
    label="Areal i drift, men ikke berettiget produksjonstilskudd",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="410",
    label="Storfe på utmarksbeite - Melkekyr og ammekyr",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="411",
    label="Storfe på beite - Melkekyr og ammekyr",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="420",
    label="Storfe på utmarksbeite - Øvrige storfe",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="422",
    label="Storfe på beite - Øvrige storfe",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="431",
    label="Sauer, født i fjor eller tidligere, utmarksbeite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="432",
    label="Lam, født i år, utmarksbeite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="440",
    label="Geiter, voksne og kje, utmarksbeite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="445",
    label="Geiter, voksne og kje, beitetilskudd",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="450",
    label="Hester på utmarksbeite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="455",
    label="Hester på beite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="480",
    label="Lama på beite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="481",
    label="Alpakka på beite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="486",
    label="Hjort på beite",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="487",
    label="Sauer, født i fjor eller tidligere, beitetilskudd",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="488",
    label="Lam, født i år, beitetilskudd",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="521",
    label="Salg av høy",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="522",
    label="Salg av surfor",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="523",
    label="Salg av høyensilasje",
    description="",
    groups=[""],
    measured_in="kilo",
)

Produksjonskode(
    code="720",
    label="Storfe på utmarksbeite - Kyr av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="721",
    label="Storfe på utmarksbeite - Okser av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="722",
    label="Søyer av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="723",
    label="Værer av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="724",
    label="Ammegeiter av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="725",
    label="Unghester under 3 år av bevaringsverdig rase",
    description="",
    groups=[""],
    measured_in="antall",
)

Produksjonskode(
    code="801",
    label="Økologiske melkekyr",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="802",
    label="Økologiske ammekyr",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="803",
    label="Økologiske øvrige storfe",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="810",
    label="Økologiske melkegeiter",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="811",
    label="Økologiske ammegeiter",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="821",
    label="Økologiske sauer",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="830",
    label="Økologiske avlsgriser",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="833",
    label="Økologiske griser solgt som livdyr",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="841",
    label="Økologiske verpehøner",
    description="",
    groups=["økologisk"],
    measured_in="antall",
)

Produksjonskode(
    code="852",
    label="Grønngjødsling, 2. års karens",
    description="",
    groups=[""],
    measured_in="dekar",
)

Produksjonskode(
    code="855",
    label="Korn til modning og krossing, økologisk samt 2.års karens",
    description="",
    groups=["økologisk", "karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="861",
    label="Poteter, økologisk areal samt 2.års karens",
    description="",
    groups=["økologisk", "karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="863",
    label="Frukt og bær, økologisk areal samt 2. og 3. års karens",
    description="",
    groups=["økologisk", "karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="864",
    label="Grønnsaker, økologisk areal samt 2. års karens",
    description="",
    groups=["økologisk", "karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="870",
    label="Annet areal (grovfôr), økologisk areal samt 2. års karens",
    description="",
    groups=["økologisk", "karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="871",
    label="Innmarksbeite, økologisk areal",
    description="",
    groups=["økologisk"],
    measured_in="dekar",
)

Produksjonskode(
    code="875",
    label="Grønngjødsling, økologisk areal",
    description="",
    groups=["økologisk"],
    measured_in="dekar",
)

Produksjonskode(
    code="876",
    label="Areal brakka for å bekjempe ugras, økologisk eller 2. års karens",
    description="",
    groups=["karens", "økologisk"],
    measured_in="dekar",
)

Produksjonskode(
    code="880",
    label="Innmarksbeite i 1 års karens",
    description="",
    groups=["karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="881",
    label="Grovforareal i 1 års karens",
    description="",
    groups=["karens"],
    measured_in="dekar",
)

Produksjonskode(
    code="882",
    label="Annet areal (enn grovfor) i 1 års karens",
    description="",
    groups=["karens"],
    measured_in="dekar",
)

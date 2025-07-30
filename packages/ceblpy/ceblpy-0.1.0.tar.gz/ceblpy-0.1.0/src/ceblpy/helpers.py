import pandas as pd
from datetime import datetime

def validate_seasons(seasons):
    """
    Checks whether all the provided seasons are valid years and raises an error if not.

    Parameters
    ----------
    seasons: list of int
        A list of years representing seasons to validate.

    Returns
    -------
    None

    Examples
    --------
    >>> validate_seasons([2019, 2020, 2021])
    >>> validate_seasons([2018, "2020"])  # Raises TypeError
    >>> validate_seasons([2022, 2023, 2030])  # Raises ValueError
    """
    if not isinstance(seasons, list):
        raise TypeError("Expected a list of years")
    for year in seasons:
        if not isinstance(year, int):
            raise TypeError(f"Expected an integer for year, got {type(year).__name__}")
        if year < 2019 or year > datetime.now().year:
            raise ValueError(f"Year {year} out of valid range (2019-{datetime.now().year})")
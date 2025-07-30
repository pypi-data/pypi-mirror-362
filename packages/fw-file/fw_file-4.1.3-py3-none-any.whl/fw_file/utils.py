"""Shared utils."""

from datetime import date, datetime, timedelta
from typing import Optional, Union


def birthdate_to_age(
    birth_date: Union[date, datetime], session_date: datetime
) -> Optional[int]:
    """Calculates age in seconds given birthday and date of session."""
    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()

    age = session_date.date() - birth_date
    age_in_seconds = age / timedelta(seconds=1)
    if age_in_seconds < 0:
        return None

    return int(age_in_seconds)

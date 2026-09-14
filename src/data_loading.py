"""
data_loading.py
---------------
Load raw gym members and check-ins datasets.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def load_members(path: Path = RAW_DIR / "members.csv") -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Members file not found: {path}")
    df = pd.read_csv(path, parse_dates=["JoinDate"])
    print(f"[data_loading] Loaded {len(df):,} members")
    return df


def load_checkins(path: Path = RAW_DIR / "checkins.csv") -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Check-ins file not found: {path}")
    df = pd.read_csv(path, parse_dates=["CheckInDate"])
    print(f"[data_loading] Loaded {len(df):,} check-ins")
    return df


def load_all():
    return load_members(), load_checkins()


if __name__ == "__main__":
    members, checkins = load_all()
    print(members.head())
    print(checkins.head())

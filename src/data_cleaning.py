"""
data_cleaning.py
----------------
Clean and prepare gym members and check-ins data.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def clean_members(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset=["MemberID"])
    df["Status"] = df["Status"].str.strip().str.title()
    df["MembershipPlan"] = df["MembershipPlan"].str.strip().str.title()
    df["Gender"] = df["Gender"].str.strip().str.title()
    # Tenure in months (approx, relative to snapshot 2025-09-01)
    snapshot = pd.Timestamp("2025-09-01")
    df["TenureMonths"] = ((snapshot - df["JoinDate"]).dt.days / 30.44).round(1)
    df["IsActive"] = (df["Status"] == "Active").astype(int)
    print(f"[data_cleaning] Members cleaned: {len(df)}")
    return df


def clean_checkins(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset=["CheckInID"])
    df["DayOfWeek"] = df["CheckInDate"].dt.day_name()
    df["Month"] = df["CheckInDate"].dt.to_period("M").astype(str)
    df["TimeSlot"] = pd.cut(
        df["CheckInHour"],
        bins=[-1, 9, 12, 16, 19, 24],
        labels=["Early Morning", "Morning", "Afternoon", "Evening", "Night"]
    )
    print(f"[data_cleaning] Check-ins cleaned: {len(df)}")
    return df


def merge_member_activity(members: pd.DataFrame, checkins: pd.DataFrame) -> pd.DataFrame:
    """Aggregate check-ins per member and merge."""
    activity = checkins.groupby("MemberID").agg(
        TotalVisits=("CheckInID", "count"),
        AvgDuration=("DurationMinutes", "mean"),
        LastVisit=("CheckInDate", "max"),
        UniqueClasses=("ClassAttended", "nunique")
    ).reset_index()
    activity["AvgDuration"] = activity["AvgDuration"].round(1)
    merged = members.merge(activity, on="MemberID", how="left")
    merged["TotalVisits"] = merged["TotalVisits"].fillna(0).astype(int)
    merged["AvgDuration"] = merged["AvgDuration"].fillna(0)
    merged["UniqueClasses"] = merged["UniqueClasses"].fillna(0).astype(int)
    print(f"[data_cleaning] Merged member activity: {len(merged)}")
    return merged


def save_processed(members: pd.DataFrame, checkins: pd.DataFrame, member_activity: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    members.to_csv(PROCESSED_DIR / "members_cleaned.csv", index=False)
    checkins.to_csv(PROCESSED_DIR / "checkins_cleaned.csv", index=False)
    member_activity.to_csv(PROCESSED_DIR / "member_activity.csv", index=False)
    print(f"[data_cleaning] Saved processed files → {PROCESSED_DIR}")


if __name__ == "__main__":
    from data_loading import load_all
    m, c = load_all()
    m = clean_members(m)
    c = clean_checkins(c)
    act = merge_member_activity(m, c)
    save_processed(m, c, act)

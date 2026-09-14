"""
analysis.py
-----------
Core analysis and insights for gym membership & fitness data.
"""

import pandas as pd


def overall_summary(members: pd.DataFrame, checkins: pd.DataFrame, activity: pd.DataFrame) -> dict:
    active = (members["Status"] == "Active").sum()
    return {
        "total_members": len(members),
        "active_members": int(active),
        "active_rate_pct": round(active / len(members) * 100, 1),
        "total_checkins": len(checkins),
        "avg_visits_per_member": round(activity["TotalVisits"].mean(), 1),
        "avg_session_minutes": round(checkins["DurationMinutes"].mean(), 1),
        "plans": members["MembershipPlan"].nunique(),
    }


def membership_breakdown(members: pd.DataFrame) -> pd.DataFrame:
    return (
        members.groupby("MembershipPlan")
        .agg(
            Members=("MemberID", "count"),
            Active=("IsActive", "sum"),
            Avg_Tenure_Months=("TenureMonths", "mean"),
            Avg_Fee=("MonthlyFee", "mean"),
        )
        .assign(Active_Rate_Pct=lambda x: (x["Active"] / x["Members"] * 100).round(1))
        .round(1)
        .sort_values("Members", ascending=False)
    )


def status_breakdown(members: pd.DataFrame) -> pd.DataFrame:
    return (
        members["Status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Count")
        .assign(Pct=lambda x: (x["Count"] / x["Count"].sum() * 100).round(1))
    )


def class_popularity(checkins: pd.DataFrame) -> pd.DataFrame:
    return (
        checkins["ClassAttended"]
        .value_counts()
        .rename_axis("Class")
        .reset_index(name="Visits")
        .assign(Pct=lambda x: (x["Visits"] / x["Visits"].sum() * 100).round(1))
    )


def peak_hours(checkins: pd.DataFrame) -> pd.DataFrame:
    return (
        checkins.groupby("CheckInHour")
        .size()
        .rename("CheckIns")
        .reset_index()
        .sort_values("CheckInHour")
    )


def day_of_week_traffic(checkins: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = checkins["DayOfWeek"].value_counts().reindex(order).fillna(0).astype(int)
    return counts.rename_axis("Day").reset_index(name="CheckIns")


def demographics(members: pd.DataFrame) -> dict:
    return {
        "by_gender": members["Gender"].value_counts().to_dict(),
        "by_age_group": members["AgeGroup"].value_counts().sort_index().to_dict(),
        "by_city": members["City"].value_counts().to_dict(),
    }


def top_active_members(activity: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    cols = ["MemberID", "MembershipPlan", "Status", "TotalVisits", "AvgDuration", "PreferredClass", "AgeGroup"]
    available = [c for c in cols if c in activity.columns]
    return activity.nlargest(n, "TotalVisits")[available]


def print_insights(members, checkins, activity) -> None:
    print("\n" + "=" * 60)
    print("KEY INSIGHTS – GYM MEMBERSHIP & FITNESS")
    print("=" * 60)
    s = overall_summary(members, checkins, activity)
    for k, v in s.items():
        print(f"{k:25}: {v}")

    print("\n--- Membership Plans ---")
    print(membership_breakdown(members))

    print("\n--- Status ---")
    print(status_breakdown(members))

    print("\n--- Top Classes ---")
    print(class_popularity(checkins).head(8))

    print("\n--- Peak Hours (top 5) ---")
    ph = peak_hours(checkins).nlargest(5, "CheckIns")
    print(ph)


if __name__ == "__main__":
    from data_loading import load_all
    from data_cleaning import clean_members, clean_checkins, merge_member_activity

    m, c = load_all()
    m = clean_members(m)
    c = clean_checkins(c)
    a = merge_member_activity(m, c)
    print_insights(m, c, a)

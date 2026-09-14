"""
visualization.py
----------------
Charts for Gym Membership & Fitness Analytics.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CHARTS_DIR = BASE_DIR / "outputs" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)


def _save(name: str) -> None:
    path = CHARTS_DIR / name
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[visualization] Saved {name}")


def plot_membership_status(members: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    members["Status"].value_counts().plot.pie(
        autopct="%1.1f%%", ax=ax, colors=["#4CAF50", "#FFC107", "#F44336"], startangle=90
    )
    ax.set_ylabel("")
    ax.set_title("Membership Status Distribution")
    _save("01_membership_status.png")


def plot_plan_distribution(members: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    order = members["MembershipPlan"].value_counts().index
    sns.countplot(data=members, x="MembershipPlan", order=order, ax=ax, palette="Blues_d")
    ax.set_title("Members by Membership Plan")
    ax.set_xlabel("")
    _save("02_members_by_plan.png")


def plot_active_rate_by_plan(members: pd.DataFrame) -> None:
    rate = members.groupby("MembershipPlan")["IsActive"].mean().sort_values() * 100
    fig, ax = plt.subplots()
    rate.plot(kind="barh", color="#59a14f", ax=ax)
    ax.set_title("Active Rate by Membership Plan (%)")
    ax.set_xlabel("Active Rate (%)")
    _save("03_active_rate_by_plan.png")


def plot_class_popularity(checkins: pd.DataFrame) -> None:
    data = checkins["ClassAttended"].value_counts().sort_values()
    fig, ax = plt.subplots()
    data.plot(kind="barh", color="#4e79a7", ax=ax)
    ax.set_title("Class / Activity Popularity (Check-ins)")
    ax.set_xlabel("Number of Visits")
    _save("04_class_popularity.png")


def plot_peak_hours(checkins: pd.DataFrame) -> None:
    hourly = checkins.groupby("CheckInHour").size()
    fig, ax = plt.subplots()
    hourly.plot(kind="bar", color="#f28e2b", ax=ax)
    ax.set_title("Check-ins by Hour of Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Check-ins")
    ax.tick_params(axis="x", rotation=0)
    _save("05_peak_hours.png")


def plot_day_of_week(checkins: pd.DataFrame) -> None:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = checkins["DayOfWeek"].value_counts().reindex(order).fillna(0)
    fig, ax = plt.subplots()
    counts.plot(kind="bar", color="#76b7b2", ax=ax)
    ax.set_title("Check-ins by Day of Week")
    ax.set_xlabel("")
    ax.set_ylabel("Check-ins")
    ax.tick_params(axis="x", rotation=30)
    _save("06_day_of_week.png")


def plot_age_gender(members: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.countplot(data=members, x="AgeGroup", order=sorted(members["AgeGroup"].unique()), ax=axes[0], palette="Set2")
    axes[0].set_title("Members by Age Group")
    axes[0].tick_params(axis="x", rotation=20)
    members["Gender"].value_counts().plot.pie(autopct="%1.1f%%", ax=axes[1], startangle=90)
    axes[1].set_ylabel("")
    axes[1].set_title("Gender Distribution")
    _save("07_demographics.png")


def plot_visits_by_plan(activity: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    order = activity.groupby("MembershipPlan")["TotalVisits"].median().sort_values(ascending=False).index
    sns.boxplot(data=activity, x="MembershipPlan", y="TotalVisits", order=order, ax=ax, palette="pastel")
    ax.set_title("Visit Frequency by Membership Plan")
    ax.set_ylabel("Total Visits (recent period)")
    _save("08_visits_by_plan.png")


def generate_all_charts(members, checkins, activity) -> None:
    print("[visualization] Generating charts...")
    plot_membership_status(members)
    plot_plan_distribution(members)
    plot_active_rate_by_plan(members)
    plot_class_popularity(checkins)
    plot_peak_hours(checkins)
    plot_day_of_week(checkins)
    plot_age_gender(members)
    plot_visits_by_plan(activity)
    print(f"[visualization] All charts → {CHARTS_DIR}")


if __name__ == "__main__":
    from data_loading import load_all
    from data_cleaning import clean_members, clean_checkins, merge_member_activity

    m, c = load_all()
    m = clean_members(m)
    c = clean_checkins(c)
    a = merge_member_activity(m, c)
    generate_all_charts(m, c, a)

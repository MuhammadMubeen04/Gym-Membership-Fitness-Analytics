"""
main.py
-------
Entry point for Gym Membership & Fitness Analytics.
Pipeline: Load → Clean → Analyze → Visualize
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.data_loading import load_all
from src.data_cleaning import clean_members, clean_checkins, merge_member_activity, save_processed
from src.analysis import print_insights, membership_breakdown, class_popularity
from src.visualization import generate_all_charts


def main():
    print("=" * 60)
    print("GYM MEMBERSHIP & FITNESS ANALYTICS")
    print("=" * 60)

    members_raw, checkins_raw = load_all()
    members = clean_members(members_raw)
    checkins = clean_checkins(checkins_raw)
    activity = merge_member_activity(members, checkins)
    save_processed(members, checkins, activity)

    print_insights(members, checkins, activity)

    print("\n--- Membership Breakdown ---")
    print(membership_breakdown(members))

    print("\n--- Class Popularity ---")
    print(class_popularity(checkins))

    generate_all_charts(members, checkins, activity)

    print("\n" + "=" * 60)
    print("✅ Pipeline complete!")
    print("   Charts → outputs/charts/")
    print("   Processed data → data/processed/")
    print("=" * 60)


if __name__ == "__main__":
    main()

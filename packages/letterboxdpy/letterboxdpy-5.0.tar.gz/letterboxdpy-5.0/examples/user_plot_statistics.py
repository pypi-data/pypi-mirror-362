if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import matplotlib.pyplot as plt
from letterboxdpy.user import User
import argparse
import sys


def gather_user_statistics_by_year(username: str, start_year: int, end_year: int) -> dict:
    """Fetch user statistics for each year."""
    stats_by_year = {}
    
    for year in range(start_year, end_year + 1):
        try:
            user = User(username)
            stats = user.get_wrapped(year)
            stats_by_year[year] = {
                "monthly": stats.get("months"),
                "daily": stats.get("days")
            }
        except Exception as error:
            raise RuntimeError(f"Failed to gather stats for {username} in {year}") from error

    return stats_by_year


def plot_statistics_by_year(stats_by_year: dict) -> None:
    """Plot user movie watching statistics for multiple years."""
    days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    num_years = len(stats_by_year)
    fig, axes = plt.subplots(num_years, 2, figsize=(10, 3 * num_years))  # Adjusted size
    fig.suptitle('Movies Watched (2020-2024)', fontsize=16)

    for i, (year, stats) in enumerate(stats_by_year.items()):
        daily_values = [stats['daily'].get(day, 0) for day in range(1, 8)]
        monthly_values = [stats['monthly'].get(month, 0) for month in range(1, 13)]

        axes[i, 0].bar(days_labels, daily_values, color='skyblue')
        axes[i, 0].set_title(f'{year} - Daily')
        axes[i, 0].set_ylabel('Movies')

        axes[i, 1].bar(months_labels, monthly_values, color='salmon')
        axes[i, 1].set_title(f'{year} - Monthly')
        axes[i, 1].set_ylabel('Movies')

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout
    plt.show()


def prompt_for_username() -> str:
    """Prompt user for a valid username."""
    username = ""
    while not username.strip():
        username = input("Enter a Letterboxd username: ")
    return username


def main() -> None:
    """Main function."""
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Visualize Letterboxd user statistics")
    parser.add_argument("--user", help="Letterboxd username")
    args = parser.parse_args()

    username = args.user or prompt_for_username()

    start_year = 2023
    end_year = 2024

    stats_by_year = gather_user_statistics_by_year(username, start_year, end_year)
    plot_statistics_by_year(stats_by_year)


if __name__ == "__main__":
    main()

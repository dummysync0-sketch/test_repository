import json
from datetime import datetime

import pandas as pd


def generate_price_report():
    # 1. Load configuration and data
    try:
        with open("config.json", "r") as f:
            config = json.load(f)

        df = pd.read_csv("prices.csv")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    if len(df) < 2:
        print("Not enough data to calculate percent change. Need at least two rows.")
        return

    # 2. Identify the last two entries for comparison
    # Assuming the last row is 'Today' and the second to last is 'Previous'
    latest_idx = len(df) - 1
    previous_idx = len(df) - 2

    report_lines = [
        "# Price Analysis Report\n",
        f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "| Item | Previous Price | Current Price | % Change | Notes |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    # 3. Calculate changes for each item in config
    for item in config["items"]:
        item_name = item["name"]

        if item_name in df.columns:
            prev = float(df.iloc[previous_idx][item_name])
            curr = float(df.iloc[latest_idx][item_name])

            # Calculate percent change: ((V2 - V1) / V1) * 100
            pct_change = ((curr - prev) / prev) * 100

            # Logic for the 10% threshold note
            note = ""
            if abs(pct_change) > 10:
                direction = "increased" if pct_change > 0 else "decreased"
                note = f"⚠️ Significant change: {direction} by {abs(pct_change):.1f}%"

            report_lines.append(
                f"| {item_name} | {prev:.2f} | {curr:.2f} | {pct_change:+.1f}% | {note} |"
            )
        else:
            print(f"Warning: {item_name} not found in prices.csv columns.")

    # 4. Write to report.md
    with open("report.md", "w") as f:
        f.write("\n".join(report_lines))

    print("Successfully generated report.md")


if __name__ == "__main__":
    generate_price_report()

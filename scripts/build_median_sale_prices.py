#!/usr/bin/env python3
"""Build per-city median sale prices for the static site."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'college_town_home_sales.csv'
OUTPUT = ROOT / 'data' / 'median_sale_prices_by_city.json'


def median(values):
    values = sorted(values)
    middle = len(values) // 2
    return values[middle] if len(values) % 2 else (values[middle - 1] + values[middle]) / 2


def main():
    sales = defaultdict(list)
    with SOURCE.open(newline='', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            price = int(row['sale_price'])
            if price >= 1000:
                sales[(row['city'], row['state'])].append(price)
    rows = [
        {'city': city, 'state': state, 'sales_count': len(prices), 'median_sale_price': median(prices)}
        for (city, state), prices in sales.items()
    ]
    rows.sort(key=lambda row: (row['median_sale_price'], row['city'], row['state']))
    OUTPUT.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(rows)} city medians to {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

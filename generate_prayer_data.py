#!/usr/bin/env python3
"""
Generate prayer times JSON data for all Malaysian JAKIM zones.
Uses approximate base times with zone-specific offsets for demonstration.
"""
import json
import os
from datetime import datetime, timedelta

# Base times (in minutes from midnight) for a reference location
# These are approximate base times for demonstration
BASE_TIMES = {
    "imsak": 330,   # 05:30
    "subuh": 345,   # 05:45
    "syuruk": 420,  # 07:00
    "zohor": 790,   # 13:10
    "asar": 980,    # 16:20
    "maghrib": 1155,# 19:15
    "isyak": 1285,  # 21:25
}

# Zone offsets in minutes from base (approximate longitudinal differences)
ZONE_OFFSETS = {
    "JHR01": {"imsak": -5, "subuh": -5, "syuruk": -5, "zohor": 5, "asar": 5, "maghrib": 5, "isyak": 5},
    "JHR02": {"imsak": 0, "subuh": 0, "syuruk": 0, "zohor": 0, "asar": 0, "maghrib": 0, "isyak": 0},
    "JHR03": {"imsak": -2, "subuh": -2, "syuruk": -2, "zohor": 2, "asar": 2, "maghrib": 2, "isyak": 2},
    "JHR04": {"imsak": -3, "subuh": -3, "syuruk": -3, "zohor": 3, "asar": 3, "maghrib": 3, "isyak": 3},
    "KDH01": {"imsak": 8, "subuh": 8, "syuruk": 8, "zohor": -8, "asar": -8, "maghrib": -8, "isyak": -8},
    "KDH02": {"imsak": 6, "subuh": 6, "syuruk": 6, "zohor": -6, "asar": -6, "maghrib": -6, "isyak": -6},
    "KDH03": {"imsak": 7, "subuh": 7, "syuruk": 7, "zohor": -7, "asar": -7, "maghrib": -7, "isyak": -7},
    "KDH04": {"imsak": 9, "subuh": 9, "syuruk": 9, "zohor": -9, "asar": -9, "maghrib": -9, "isyak": -9},
    "KDH05": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "KDH06": {"imsak": 10, "subuh": 10, "syuruk": 10, "zohor": -10, "asar": -10, "maghrib": -10, "isyak": -10},
    "KDH07": {"imsak": 7, "subuh": 7, "syuruk": 7, "zohor": -7, "asar": -7, "maghrib": -7, "isyak": -7},
    "KTN01": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "KTN03": {"imsak": 7, "subuh": 7, "syuruk": 7, "zohor": -7, "asar": -7, "maghrib": -7, "isyak": -7},
    "MLK01": {"imsak": -2, "subuh": -2, "syuruk": -2, "zohor": 2, "asar": 2, "maghrib": 2, "isyak": 2},
    "NGS01": {"imsak": -1, "subuh": -1, "syuruk": -1, "zohor": 1, "asar": 1, "maghrib": 1, "isyak": 1},
    "NGS02": {"imsak": 0, "subuh": 0, "syuruk": 0, "zohor": 0, "asar": 0, "maghrib": 0, "isyak": 0},
    "PHG01": {"imsak": 2, "subuh": 2, "syuruk": 2, "zohor": -2, "asar": -2, "maghrib": -2, "isyak": -2},
    "PHG02": {"imsak": 3, "subuh": 3, "syuruk": 3, "zohor": -3, "asar": -3, "maghrib": -3, "isyak": -3},
    "PHG03": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "PHG04": {"imsak": 6, "subuh": 6, "syuruk": 6, "zohor": -6, "asar": -6, "maghrib": -6, "isyak": -6},
    "PHG05": {"imsak": 4, "subuh": 4, "syuruk": 4, "zohor": -4, "asar": -4, "maghrib": -4, "isyak": -4},
    "PHG06": {"imsak": 6, "subuh": 6, "syuruk": 6, "zohor": -6, "asar": -6, "maghrib": -6, "isyak": -6},
    "PLS01": {"imsak": 9, "subuh": 9, "syuruk": 9, "zohor": -9, "asar": -9, "maghrib": -9, "isyak": -9},
    "PNG01": {"imsak": 7, "subuh": 7, "syuruk": 7, "zohor": -7, "asar": -7, "maghrib": -7, "isyak": -7},
    "PRK01": {"imsak": 4, "subuh": 4, "syuruk": 4, "zohor": -4, "asar": -4, "maghrib": -4, "isyak": -4},
    "PRK02": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "PRK03": {"imsak": 8, "subuh": 8, "syuruk": 8, "zohor": -8, "asar": -8, "maghrib": -8, "isyak": -8},
    "PRK04": {"imsak": 9, "subuh": 9, "syuruk": 9, "zohor": -9, "asar": -9, "maghrib": -9, "isyak": -9},
    "PRK05": {"imsak": 3, "subuh": 3, "syuruk": 3, "zohor": -3, "asar": -3, "maghrib": -3, "isyak": -3},
    "PRK06": {"imsak": 6, "subuh": 6, "syuruk": 6, "zohor": -6, "asar": -6, "maghrib": -6, "isyak": -6},
    "PRK07": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "SBH01": {"imsak": -15, "subuh": -15, "syuruk": -15, "zohor": 15, "asar": 15, "maghrib": 15, "isyak": 15},
    "SBH02": {"imsak": -12, "subuh": -12, "syuruk": -12, "zohor": 12, "asar": 12, "maghrib": 12, "isyak": 12},
    "SBH03": {"imsak": -18, "subuh": -18, "syuruk": -18, "zohor": 18, "asar": 18, "maghrib": 18, "isyak": 18},
    "SBH04": {"imsak": -20, "subuh": -20, "syuruk": -20, "zohor": 20, "asar": 20, "maghrib": 20, "isyak": 20},
    "SBH05": {"imsak": -10, "subuh": -10, "syuruk": -10, "zohor": 10, "asar": 10, "maghrib": 10, "isyak": 10},
    "SBH06": {"imsak": -13, "subuh": -13, "syuruk": -13, "zohor": 13, "asar": 13, "maghrib": 13, "isyak": 13},
    "SBH07": {"imsak": -14, "subuh": -14, "syuruk": -14, "zohor": 14, "asar": 14, "maghrib": 14, "isyak": 14},
    "SBH08": {"imsak": -16, "subuh": -16, "syuruk": -16, "zohor": 16, "asar": 16, "maghrib": 16, "isyak": 16},
    "SBH09": {"imsak": -17, "subuh": -17, "syuruk": -17, "zohor": 17, "asar": 17, "maghrib": 17, "isyak": 17},
    "SGR01": {"imsak": 0, "subuh": 0, "syuruk": 0, "zohor": 0, "asar": 0, "maghrib": 0, "isyak": 0},
    "SGR02": {"imsak": 3, "subuh": 3, "syuruk": 3, "zohor": -3, "asar": -3, "maghrib": -3, "isyak": -3},
    "SGR03": {"imsak": -1, "subuh": -1, "syuruk": -1, "zohor": 1, "asar": 1, "maghrib": 1, "isyak": 1},
    "SWK01": {"imsak": -22, "subuh": -22, "syuruk": -22, "zohor": 22, "asar": 22, "maghrib": 22, "isyak": 22},
    "SWK02": {"imsak": -20, "subuh": -20, "syuruk": -20, "zohor": 20, "asar": 20, "maghrib": 20, "isyak": 20},
    "SWK03": {"imsak": -18, "subuh": -18, "syuruk": -18, "zohor": 18, "asar": 18, "maghrib": 18, "isyak": 18},
    "SWK04": {"imsak": -21, "subuh": -21, "syuruk": -21, "zohor": 21, "asar": 21, "maghrib": 21, "isyak": 21},
    "SWK05": {"imsak": -23, "subuh": -23, "syuruk": -23, "zohor": 23, "asar": 23, "maghrib": 23, "isyak": 23},
    "SWK06": {"imsak": -25, "subuh": -25, "syuruk": -25, "zohor": 25, "asar": 25, "maghrib": 25, "isyak": 25},
    "SWK07": {"imsak": -26, "subuh": -26, "syuruk": -26, "zohor": 26, "asar": 26, "maghrib": 26, "isyak": 26},
    "SWK08": {"imsak": -27, "subuh": -27, "syuruk": -27, "zohor": 27, "asar": 27, "maghrib": 27, "isyak": 27},
    "SWK09": {"imsak": -24, "subuh": -24, "syuruk": -24, "zohor": 24, "asar": 24, "maghrib": 24, "isyak": 24},
    "TRG01": {"imsak": 4, "subuh": 4, "syuruk": 4, "zohor": -4, "asar": -4, "maghrib": -4, "isyak": -4},
    "TRG02": {"imsak": 5, "subuh": 5, "syuruk": 5, "zohor": -5, "asar": -5, "maghrib": -5, "isyak": -5},
    "TRG03": {"imsak": 6, "subuh": 6, "syuruk": 6, "zohor": -6, "asar": -6, "maghrib": -6, "isyak": -6},
    "TRG04": {"imsak": 2, "subuh": 2, "syuruk": 2, "zohor": -2, "asar": -2, "maghrib": -2, "isyak": -2},
    "WLY01": {"imsak": 0, "subuh": 0, "syuruk": 0, "zohor": 0, "asar": 0, "maghrib": 0, "isyak": 0},
    "WLY02": {"imsak": -12, "subuh": -12, "syuruk": -12, "zohor": 12, "asar": 12, "maghrib": 12, "isyak": 12},
}

def minutes_to_time(mins):
    h = mins // 60
    m = mins % 60
    return f"{h:02d}:{m:02d}"

def generate_month_data(zone, year, month):
    """Generate prayer times for a given zone, year, and month."""
    offsets = ZONE_OFFSETS.get(zone, {k: 0 for k in BASE_TIMES})
    
    # Approximate day-of-month variation (solar declination effect)
    # Peak summer/winter shift ~15 mins for Malaysia
    def daily_shift(day):
        import math
        # Day of year approximation
        day_of_year = (datetime(year, month, 1) - datetime(year, 1, 1)).days + day
        return int(15 * math.sin((day_of_year - 80) * 2 * 3.14159 / 365))
    
    days_in_month = (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day
    if month == 12:
        days_in_month = 31
    
    schedule = []
    for day in range(1, days_in_month + 1):
        shift = daily_shift(day)
        entry = {
            "date": f"{year}-{month:02d}-{day:02d}",
            "day": day,
            "imsak": minutes_to_time(BASE_TIMES["imsak"] + offsets["imsak"] + shift),
            "subuh": minutes_to_time(BASE_TIMES["subuh"] + offsets["subuh"] + shift),
            "syuruk": minutes_to_time(BASE_TIMES["syuruk"] + offsets["syuruk"] + shift),
            "zohor": minutes_to_time(BASE_TIMES["zohor"] + offsets["zohor"] + shift),
            "asar": minutes_to_time(BASE_TIMES["asar"] + offsets["asar"] + shift),
            "maghrib": minutes_to_time(BASE_TIMES["maghrib"] + offsets["maghrib"] + shift),
            "isyak": minutes_to_time(BASE_TIMES["isyak"] + offsets["isyak"] + shift),
        }
        schedule.append(entry)
    
    # Also generate next month for 30-day lookahead
    next_month = month % 12 + 1
    next_year = year + (1 if next_month == 1 else 0)
    
    for day in range(1, 32):
        try:
            d = datetime(next_year, next_month, day)
            shift = daily_shift(day + days_in_month)
            entry = {
                "date": f"{next_year}-{next_month:02d}-{day:02d}",
                "day": day,
                "imsak": minutes_to_time(BASE_TIMES["imsak"] + offsets["imsak"] + shift),
                "subuh": minutes_to_time(BASE_TIMES["subuh"] + offsets["subuh"] + shift),
                "syuruk": minutes_to_time(BASE_TIMES["syuruk"] + offsets["syuruk"] + shift),
                "zohor": minutes_to_time(BASE_TIMES["zohor"] + offsets["zohor"] + shift),
                "asar": minutes_to_time(BASE_TIMES["asar"] + offsets["asar"] + shift),
                "maghrib": minutes_to_time(BASE_TIMES["maghrib"] + offsets["maghrib"] + shift),
                "isyak": minutes_to_time(BASE_TIMES["isyak"] + offsets["isyak"] + shift),
            }
            schedule.append(entry)
        except ValueError:
            break
    
    return schedule

def main():
    with open("data/zones.json", "r", encoding="utf-8") as f:
        zones = json.load(f)
    
    now = datetime.now()
    year, month = now.year, now.month
    
    for zone_code in zones:
        schedule = generate_month_data(zone_code, year, month)
        data = {
            "zone": zone_code,
            "zone_name": zones[zone_code],
            "month": month,
            "year": year,
            "generated": now.isoformat(),
            "schedule": schedule,
            "source": "JAKIM (approximate demo data)"
        }
        filepath = os.path.join("data", f"{zone_code}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Generated {filepath}")

if __name__ == "__main__":
    main()

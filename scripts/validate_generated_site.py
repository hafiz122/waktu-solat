#!/usr/bin/env python3
"""
Validate generated static prayer-time artifacts.

Checks:
1) All expected zone JSON files exist and have non-empty schedules.
2) Global max schedule date is at least N days ahead of today.
3) Expected HTML coverage exists in root + en/zh/ta/ar directories.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List


LANG_DIRS = ("", "en", "zh", "ta", "ar")
PRAYER_KEYS = ("imsak", "subuh", "syuruk", "zohor", "asar", "maghrib", "isyak")


@dataclass
class ValidationResult:
    errors: List[str]
    warnings: List[str]
    global_max_date: date | None
    zone_count: int
    expected_per_language: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated prayer site output.")
    parser.add_argument("--repo-dir", default=".", help="Repository root path.")
    parser.add_argument(
        "--min-days-ahead",
        type=int,
        default=7,
        help="Minimum number of days ahead from today required for max schedule date.",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Override current date in YYYY-MM-DD (for testing).",
    )
    return parser.parse_args()


def parse_iso_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid {field_name} date '{value}': {exc}") from exc


def validate_json_artifacts(repo_dir: Path, zones: Dict[str, str], errors: List[str]) -> date | None:
    data_dir = repo_dir / "data"
    global_max: date | None = None

    for zone_code in zones:
        zone_path = data_dir / f"{zone_code}.json"
        if not zone_path.exists():
            errors.append(f"Missing zone JSON: {zone_path}")
            continue

        try:
            payload = json.loads(zone_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {zone_path}: {exc}")
            continue

        schedule = payload.get("schedule")
        if not isinstance(schedule, list) or not schedule:
            errors.append(f"Empty or invalid schedule in {zone_path}")
            continue

        zone_max: date | None = None
        for idx, entry in enumerate(schedule, start=1):
            if not isinstance(entry, dict):
                errors.append(f"{zone_path}: schedule item #{idx} is not an object")
                continue

            raw_date = entry.get("date")
            if not isinstance(raw_date, str):
                errors.append(f"{zone_path}: schedule item #{idx} missing string 'date'")
                continue

            try:
                parsed_date = parse_iso_date(raw_date, "schedule")
            except ValueError as exc:
                errors.append(f"{zone_path}: {exc}")
                continue

            for prayer_key in PRAYER_KEYS:
                value = entry.get(prayer_key)
                if not isinstance(value, str) or ":" not in value:
                    errors.append(
                        f"{zone_path}: schedule item #{idx} missing/invalid prayer time '{prayer_key}'"
                    )

            if zone_max is None or parsed_date > zone_max:
                zone_max = parsed_date

        if zone_max and (global_max is None or zone_max > global_max):
            global_max = zone_max

    return global_max


def validate_html_coverage(repo_dir: Path, zones: Dict[str, str], errors: List[str], warnings: List[str]) -> None:
    expected_zone_pages = [f"{code}.html" for code in zones]
    expected_names = {"index.html", *expected_zone_pages}

    total_expected = len(expected_names) * len(LANG_DIRS)
    total_actual = 0

    for lang_dir in LANG_DIRS:
        base = repo_dir if not lang_dir else repo_dir / lang_dir
        label = "root" if not lang_dir else lang_dir
        if not base.exists():
            errors.append(f"Missing language directory: {base}")
            continue

        html_names = {path.name for path in base.glob("*.html")}
        total_actual += len(html_names)

        missing = sorted(expected_names - html_names)
        if missing:
            preview = ", ".join(missing[:5])
            suffix = "" if len(missing) <= 5 else f" ... (+{len(missing) - 5} more)"
            errors.append(f"{label}: missing {len(missing)} expected HTML files ({preview}{suffix})")

        extra = sorted(html_names - expected_names)
        if extra:
            warnings.append(f"{label}: found {len(extra)} extra HTML files (not failing)")

    if total_actual < total_expected:
        errors.append(
            f"Total HTML below baseline: expected at least {total_expected}, found {total_actual}"
        )


def run_validation(repo_dir: Path, min_days_ahead: int, today: date) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    zones_path = repo_dir / "data" / "zones.json"
    if not zones_path.exists():
        errors.append(f"Missing zones file: {zones_path}")
        return ValidationResult(errors, warnings, None, 0, 0)

    try:
        zones = json.loads(zones_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid zones.json: {exc}")
        return ValidationResult(errors, warnings, None, 0, 0)

    if not isinstance(zones, dict) or not zones:
        errors.append("zones.json must contain a non-empty object.")
        return ValidationResult(errors, warnings, None, 0, 0)

    global_max = validate_json_artifacts(repo_dir, zones, errors)
    validate_html_coverage(repo_dir, zones, errors, warnings)

    if global_max is None:
        errors.append("Unable to determine max schedule date from zone files.")
    else:
        required = today + timedelta(days=min_days_ahead)
        if global_max < required:
            errors.append(
                "Schedule freshness below threshold: "
                f"max date {global_max.isoformat()} < required {required.isoformat()} "
                f"(today={today.isoformat()}, min_days_ahead={min_days_ahead})"
            )

    return ValidationResult(
        errors=errors,
        warnings=warnings,
        global_max_date=global_max,
        zone_count=len(zones),
        expected_per_language=len(zones) + 1,
    )


def main() -> int:
    args = parse_args()
    repo_dir = Path(args.repo_dir).resolve()
    if args.today:
        today = parse_iso_date(args.today, "today")
    else:
        today = date.today()

    result = run_validation(repo_dir=repo_dir, min_days_ahead=args.min_days_ahead, today=today)

    print("Validation summary:")
    print(f"- repo_dir: {repo_dir}")
    print(f"- zones: {result.zone_count}")
    print(f"- expected_html_per_language: {result.expected_per_language}")
    print(f"- global_max_schedule_date: {result.global_max_date}")
    print(f"- warnings: {len(result.warnings)}")
    print(f"- errors: {len(result.errors)}")

    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the static talk-map data used by talkmap/map.html.

The script reads the YAML-style front matter in ``_talks/*.md``, skips online
talks, groups in-person talks by location, and writes ``talkmap/org-locations.js``.
Coordinates are cached in ``talkmap/location-coordinates.json`` so the live
website never calls a geocoding service.

Run ``python talkmap.py --geocode`` only when a new location needs coordinates.
The geocoding mode follows the public Nominatim usage policy by identifying the
site and waiting more than one second between requests.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
TALKS_DIR = ROOT / "_talks"
CACHE_PATH = ROOT / "talkmap" / "location-coordinates.json"
OUTPUT_PATH = ROOT / "talkmap" / "org-locations.js"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "AlexisAkiraTodaTalkMap/1.0 (https://alexisakira.github.io/)"
ONLINE_LABELS = {"online", "virtual", "zoom"}


def parse_front_matter(path: Path) -> dict[str, str]:
    """Read the simple scalar fields used by the talk Markdown files."""
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path.name}: missing YAML front matter")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        fields[key.strip()] = html.unescape(value)
    return fields


def talk_url(path: Path, fields: dict[str, str]) -> str:
    permalink = fields.get("permalink", "").strip()
    if permalink:
        return permalink
    return f"/talks/{path.stem}/"


def load_talks() -> tuple[list[dict[str, str]], int]:
    talks: list[dict[str, str]] = []
    online_count = 0

    for path in sorted(TALKS_DIR.glob("*.md")):
        fields = parse_front_matter(path)
        location = fields.get("location", "").strip()
        if not location:
            raise ValueError(f"{path.name}: missing location")
        if location.casefold() in ONLINE_LABELS:
            online_count += 1
            continue

        talks.append(
            {
                "date": fields.get("date", ""),
                "location": location,
                "title": fields.get("title", path.stem),
                "type": fields.get("type", "Talk"),
                "url": talk_url(path, fields),
                "venue": fields.get("venue", ""),
            }
        )

    return talks, online_count


def load_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict[str, dict[str, Any]]) -> None:
    CACHE_PATH.write_text(
        json.dumps(dict(sorted(cache.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def geocode(location: str) -> dict[str, Any]:
    query = urlencode({"q": location, "format": "jsonv2", "limit": 1})
    request = Request(
        f"{NOMINATIM_URL}?{query}",
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=30) as response:
        results = json.load(response)
    if not results:
        raise RuntimeError(f"No coordinates found for {location!r}")
    result = results[0]
    return {
        "display_name": result.get("display_name", location),
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
    }


def fill_missing_coordinates(locations: list[str], cache: dict[str, dict[str, Any]]) -> None:
    missing = [location for location in locations if location not in cache]
    for index, location in enumerate(missing, start=1):
        if index > 1:
            time.sleep(1.1)
        print(f"Geocoding {index}/{len(missing)}: {location}", flush=True)
        cache[location] = geocode(location)
        save_cache(cache)


def build_dataset(
    talks: list[dict[str, str]], online_count: int, cache: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for talk in talks:
        grouped[talk["location"]].append(talk)

    missing = sorted(set(grouped) - set(cache))
    if missing:
        formatted = "\n  - ".join(missing)
        raise RuntimeError(
            "Coordinates are missing for these locations. "
            "Run 'python talkmap.py --geocode':\n  - " + formatted
        )

    locations: list[dict[str, Any]] = []
    for location in sorted(grouped):
        coordinates = cache[location]
        location_talks = sorted(
            grouped[location], key=lambda item: item.get("date", ""), reverse=True
        )
        locations.append(
            {
                "label": location,
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "talks": location_talks,
            }
        )

    return {
        "in_person_talk_count": len(talks),
        "location_count": len(locations),
        "online_talk_count": online_count,
        "locations": locations,
    }


def write_javascript(dataset: dict[str, Any]) -> None:
    payload = json.dumps(dataset, ensure_ascii=False, indent=2)
    OUTPUT_PATH.write_text(
        "// Generated by talkmap.py. Edit _talks files or the coordinate cache, not this file.\n"
        f"window.talkMapData = {payload};\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--geocode",
        action="store_true",
        help="look up and cache coordinates for locations not already cached",
    )
    args = parser.parse_args()

    talks, online_count = load_talks()
    locations = sorted({talk["location"] for talk in talks})
    cache = load_cache()

    if args.geocode:
        fill_missing_coordinates(locations, cache)

    # Drop stale coordinates after a location label is corrected or normalized.
    active_cache = {location: cache[location] for location in locations if location in cache}
    if args.geocode and active_cache != cache:
        save_cache(active_cache)
    cache = active_cache

    dataset = build_dataset(talks, online_count, cache)
    write_javascript(dataset)
    print(
        f"Wrote {dataset['in_person_talk_count']} in-person talks across "
        f"{dataset['location_count']} locations; omitted "
        f"{dataset['online_talk_count']} online talks."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)

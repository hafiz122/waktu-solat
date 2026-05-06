# Waktu Solat Malaysia

Static multilingual prayer-time site for Malaysia zones, with generated zone pages and JSON schedules.

## Quick Start (Localhost)

From the project root:

```bash
python -m http.server 8000
```

Then open:

- `http://localhost:8000/`

## Project Structure

- `index.html`: Malay homepage.
- `en/`, `zh/`, `ta/`, `ar/`: localized pages.
- `data/*.json`: generated prayer schedules and metadata.
- `js/main.js`: client-side rendering, search, countdown, and zone loading.
- `css/style.css`: site styles.
- `generate_prayer_data.py`: generates zone JSON schedule files.
- `generate_html.py`: generates homepage + zone pages for all languages.
- `scripts/`: automation tooling (refresh pipeline, validation, cron template).

## Regenerate Data and Pages

```bash
python generate_prayer_data.py
python generate_html.py
```

## Validate Generated Output

```bash
python scripts/validate_generated_site.py --repo-dir . --min-days-ahead 7
```

## Daily Server Automation

Main script:

```bash
bash scripts/refresh_site.sh --repo-dir /opt/waktu-solat --branch main --min-days-ahead 7
```

Cron template:

- `scripts/cron.example`

Detailed automation notes:

- `scripts/README.md`

# Automation Scripts

This directory contains the server automation pipeline for daily static refresh.

## Files

- `refresh_site.sh`: Non-interactive pull -> regenerate -> validate -> commit -> push pipeline.
- `validate_generated_site.py`: Validation checks for JSON integrity, freshness window, and HTML coverage.
- `cron.example`: Daily cron entry template with log and email alerting.

## Refresh Script Interface

```bash
bash scripts/refresh_site.sh \
  --repo-dir /opt/waktu-solat \
  --branch main \
  --min-days-ahead 7
```

Options:
- `--remote` (default `origin`)
- `--python` (default `python3`)
- `--dry-run` (skip commit/push, useful for testing)

## Required Environment / Git Setup

Commit identity can be provided either via environment or git config:

```bash
export GIT_AUTHOR_NAME="Waktu Solat Bot"
export GIT_AUTHOR_EMAIL="bot@example.com"
```

Or:

```bash
git config user.name "Waktu Solat Bot"
git config user.email "bot@example.com"
```

Push authentication should be available through SSH key or token-backed remote.

## Validator Example

```bash
python3 scripts/validate_generated_site.py --repo-dir /opt/waktu-solat --min-days-ahead 7
```

The validator fails if:
- any zone schedule is missing/empty,
- max schedule date is behind threshold,
- expected HTML coverage is incomplete across root + `en`/`zh`/`ta`/`ar`.


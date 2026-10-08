"""Download the US industry-523 API extract, preserving raw records and paging logs.

Run with the notebook's Python environment:
    /opt/anaconda3/envs/bu-spark312/bin/python pull_naics_523_api.py

Uses the current API guide: https://met-employability-services.azurewebsites.net/api/docs/
The career/title filter is intentionally separate from this raw industry extract.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent


def save_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint', choices=['job-facts', 'jobs'], default='job-facts')
    parser.add_argument('--page-size', type=int, default=100)
    parser.add_argument('--read-timeout', type=int, default=60)
    args = parser.parse_args()
    if not 1 <= args.page_size <= 500 or args.read_timeout <= 0:
        parser.error('Page size must be 1–500 and read timeout must be positive.')

    load_dotenv(ROOT / '.env')
    key = os.getenv('EMPLOYABILITY_API_KEY')
    if not key:
        raise SystemExit('EMPLOYABILITY_API_KEY is missing from the repository .env.')
    configured_base = os.getenv('EMPLOYABILITY_API_BASE_URL', 'https://met-employability-services.azurewebsites.net')
    parsed_base = urlsplit(configured_base)
    # Accept either the old origin-only setting or the guide's current student API base.
    base = f'{parsed_base.scheme}://{parsed_base.netloc}/api/v1/student'
    endpoint = f'{base}/{args.endpoint}/'
    output = ROOT / 'data/raw_naics_523.json'
    log_path = ROOT / 'data/raw_naics_523.download_log.json'
    pages_dir = ROOT / 'data/raw_naics_523_pages'
    if output.exists():
        raise SystemExit(f'{output.name} already exists. Rename it before making a fresh extract.')

    filters = {'country': 'US', 'naics': '523'}
    records = []
    first_meta = None
    offset = 0
    seen_offsets = set()
    log = {'started_at': datetime.now(timezone.utc).isoformat(), 'endpoint': endpoint,
           'filters': filters, 'complete': False, 'record_count': 0, 'requests': []}
    save_json(log_path, log)

    def checkpoint(complete):
        log['complete'] = complete
        log['record_count'] = len(records)
        save_json(log_path, log)
        # A failed request with no API response must not produce a misleading empty dataset.
        if first_meta is not None:
            save_json(output, {'meta': first_meta, 'filters': filters,
                              'record_count': len(records), 'results': records,
                              'download': {'endpoint': endpoint, 'complete': complete,
                                           'next_offset': None if complete else offset,
                                           'started_at': log['started_at']}})

    try:
        with requests.Session() as session:
            session.headers.update({'X-API-Key': key})
            while True:
                if offset in seen_offsets:
                    raise ValueError('API pagination repeated an offset.')
                seen_offsets.add(offset)
                params = {**filters, 'limit': args.page_size, 'offset': offset}
                entry = {'requested_at': datetime.now(timezone.utc).isoformat(),
                         'offset': offset, 'limit': args.page_size}
                log['requests'].append(entry)
                save_json(log_path, log)
                print(f'Requesting {args.endpoint}: country=US, naics=523, offset={offset}, limit={args.page_size}', flush=True)
                response = session.get(endpoint, params=params, timeout=(10, args.read_timeout))
                entry['status'] = response.status_code
                response.raise_for_status()
                payload = response.json()
                rows, meta = payload.get('results'), payload.get('meta')
                if not isinstance(rows, list) or not isinstance(meta, dict):
                    raise ValueError('Unexpected API response: results must be a list and meta an object.')
                if not all(isinstance(row, dict) for row in rows):
                    raise ValueError('API results contain a non-object record.')
                if first_meta is None:
                    first_meta = meta
                save_json(pages_dir / f'page_{offset:08d}.json', payload)
                entry['rows_returned'] = len(rows)
                records.extend(rows)
                print(f'Received {len(rows)} rows; total {len(records):,}.', flush=True)

                if 'next' in meta:
                    complete = not meta['next']
                elif 'has_more' in meta:
                    complete = not meta['has_more']
                elif isinstance(meta.get('count'), int):
                    complete = len(records) >= meta['count']
                else:
                    raise ValueError('API did not provide next, has_more, or a total count to verify completion.')
                if not rows and not complete:
                    raise ValueError('API returned an empty page before completion.')
                if complete:
                    checkpoint(True)
                    print(f'Saved complete extract: {output} ({len(records):,} rows).')
                    return 0

                next_offset = offset + len(rows)
                if meta.get('next'):
                    query = parse_qs(urlsplit(meta['next']).query)
                    if query.get('offset'):
                        next_offset = int(query['offset'][0])
                if next_offset <= offset:
                    raise ValueError('API pagination did not advance.')
                offset = next_offset
                checkpoint(False)
    except (requests.RequestException, ValueError, KeyboardInterrupt) as error:
        log['error_type'] = type(error).__name__
        if isinstance(error, ValueError):
            log['error_detail'] = str(error)
        checkpoint(False)
        print(f'Download stopped: {type(error).__name__}. Received {len(records):,} rows.', flush=True)
        print(f'Request log: {log_path}', flush=True)
        if first_meta is None:
            print('No raw JSON created because no valid API page was received.', flush=True)
        else:
            print('The saved JSON is marked complete=false; do not treat it as the full extract.', flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

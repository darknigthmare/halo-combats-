#!/usr/bin/env python3
"""Freeze completed V6 attempts into one audit journal, without losing failures.

Default: inspect only. --apply refuses pending attempts, missing catalog entries,
missing PNGs, changed input journals, and incomplete coverage of the 33 new
extension identities plus the previously missing Chief guard.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

WORK = Path(__file__).resolve().parent
INPUTS = ('generation_results_root.json', 'generation_results_unsc.json', 'generation_results_aliens.json')
CATALOGS = ('root_catalog.json', 'unsc_catalog.json', 'alien_catalog.json')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    results, inputs, pending = [], [], []
    for filename in INPUTS:
        path = WORK / filename
        data = json.loads(path.read_text(encoding='utf-8'))
        rows = data['results']
        inputs.append({'path': 'work/wave6/' + filename, 'sha256': sha(path), 'attempts': len(rows)})
        for row in rows:
            if row.get('status') not in {'generated_candidate', 'generation_failed'}:
                pending.append({'source': filename, 'entity_id': row.get('entity_id'), 'status': row.get('status')})
            if row.get('status') == 'generated_candidate':
                source = Path(row['source_path'])
                assert source.is_file(), f'PNG absent: {source}'
            results.append(row)
    entries = []
    missing_catalogs = []
    for filename in CATALOGS:
        path = WORK / filename
        if not path.exists():
            missing_catalogs.append(filename)
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        entries.extend(data if isinstance(data, list) else data.get('entries', data.get('characters', data.get('records', []))))
    expected = {e['id'] for e in entries if e.get('generation_required', True)} | {'chief_infinite'}
    attempted = {r['entity_id'] for r in results}
    missing_attempts = sorted(expected - attempted)
    unexpected_attempts = sorted(attempted - expected)
    if args.apply:
        assert not pending, f'Pending attempts: {pending}'
        assert not missing_catalogs, f'Missing catalogs: {missing_catalogs}'
        assert len(entries) == 34 and len({e['id'] for e in entries}) == 34, 'Expected 34 unique catalog entries'
        assert len(expected) == 34, 'Expected 33 new extension identities plus Chief guard'
        assert not missing_attempts and not unexpected_attempts, f'Coverage mismatch: missing {missing_attempts}; unexpected {unexpected_attempts}'
        assert 'warden_eternal_h5' not in attempted, 'Warden must be reused, not generated again'
        assert all(sha(WORK / x['path'].split('/')[-1]) == x['sha256'] for x in inputs), 'A journal changed during merge'
        output = {'wave': 6, 'task': 'Générer les 33 identités/classes manquantes des extensions déjà listées, reprendre la garde du Major et publier dans la PR existante ; Warden réutilisé sans nouvelle génération.', 'merged_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'source_journals': inputs, 'results': results}
        destination = WORK / 'generation_results.json'
        temporary = destination.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(destination)
    print(json.dumps({'applied': args.apply, 'attempts': len(results), 'generated': sum(r.get('status') == 'generated_candidate' for r in results), 'failed': sum(r.get('status') == 'generation_failed' for r in results), 'pending': pending, 'catalog_entries': len(entries), 'missing_catalogs': missing_catalogs, 'missing_attempts': missing_attempts, 'unexpected_attempts': unexpected_attempts}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

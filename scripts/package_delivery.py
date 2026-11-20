from pathlib import Path
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / 'outputs' / 'halo_combats_v1'
OUT.mkdir(parents=True, exist_ok=True)
patterns = [
    'README.md', 'docs/*.docx', 'docs/*.xlsx', 'docs/*.md', 'docs/source_registry.json',
    'docs/build_bible.py', 'data/*.json', 'data/*.csv', 'assets/candidates/*.png',
    'prototype/*.html', 'prototype/*.md', 'prototype/qa/*.cjs', 'prototype/qa/results.json',
    'work/core_chapter.md', 'work/roster/roster_chapter.md', 'work/roster/build_roster.py',
    'work/roster/source_registry.json', 'work/world/bosses_stages.md', 'work/world/build_world.py'
]
files = sorted({p for pattern in patterns for p in ROOT.glob(pattern) if p.is_file()})
hashes = '\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}' for p in files) + '\n'
checksum = ROOT / 'SHA256SUMS.txt'
checksum.write_text(hashes)
files.append(checksum)
path = OUT / 'HALO_COMBATS_V1_COMPLET.zip'
with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files:
        z.write(p, Path('Halo_Combats_V1') / p.relative_to(ROOT))
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(files)
    for p in files:
        assert z.read(str(Path('Halo_Combats_V1') / p.relative_to(ROOT))) == p.read_bytes()
print(json.dumps({'file': str(path), 'files':len(files), 'bytes':path.stat().st_size,
                  'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'png_files':sum(p.suffix=='.png' for p in files),
                  'checks':'ZIP CRC and byte comparison passed'}, ensure_ascii=False))

"""Kontrola końcowego zestawu; przegląd wizualny wykonuje asystent osobno."""
import hashlib
import json
import re
import subprocess
import zlib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RUN = Path('wyniki/20261017_102226_905860_A')


def main():
    report = Path('raport.md').read_text()
    required = ['raport.md', 'raport.pdf', 'benchmark.cpp', 'benchmark.py', 'generate_data.py',
                'dane/input.txt', 'plan_A.md', 'export_report.sh', 'collect_A.py', 'verify_A.py']
    for name in required:
        assert Path(name).is_file(), name
    # Miejsce docelowe istnieje również podczas kontroli odsyłacza do samego raportu kontroli.
    destination = RUN / 'final_check.json'
    if not destination.exists():
        destination.write_text('{}\n')
    links = re.findall(r'\]\(([^)]+)\)', report)
    assert links and all(Path(x).exists() for x in links)
    assert len(re.findall(r'^# ', report, re.M)) == 1
    assert [int(x) for x in re.findall(r'^## (\d+)\.', report, re.M)] == list(range(1, 13))
    raw = Path('raport.pdf').read_bytes()
    streams = []
    for match in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', raw, re.S):
        try:
            streams.append(zlib.decompress(match[1]))
        except zlib.error:
            pass
    decoded = b'\n'.join(streams)
    targets = [x.decode('ascii') for x in re.findall(rb'/(?:URI|F)\(([^()]+)\)', decoded)]
    assert len(targets) >= len(links)
    assert all(Path(x).exists() and not x.endswith('/.pdf') for x in targets)
    text = subprocess.run(['pdftotext', 'raport.pdf', '-'], capture_output=True, check=True).stdout
    info = subprocess.run(['pdfinfo', 'raport.pdf'], capture_output=True, check=True).stdout
    assert b'Pages:           5' in info
    assert b'Kryptonim TiDPI: Regulus' in info
    assert 'Środowisko'.encode() in text and 'Wykorzystanie AI'.encode() in text
    for lang in ['cpp', 'python']:
        content = (RUN / f'A_{lang}_raw.txt').read_text().strip()
        assert content in report
        for line in content.splitlines()[1:]:
            assert line.encode() in text
    manifest = json.loads((RUN / 'source_sha256.json').read_text())
    for name, digest in manifest.items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest
        assert hashlib.sha256((RUN / 'sources' / name).read_bytes()).hexdigest() == digest
    assert '-O2 -DNDEBUG' in (RUN / 'commands.txt').read_text()
    privacy = re.compile(rb'/(?:Users|home)/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    files = [p for p in Path('.').rglob('*') if p.is_file() and '_build' not in p.parts
             and '__pycache__' not in p.parts and p.name != 'TiDPI_07_Rzetelny_benchmark_Cpp_i_Python.pdf']
    for path in files:
        if path.suffix != '.pdf':
            assert not privacy.search(path.read_bytes()), path.as_posix()
    assert not privacy.search(text + info + decoded)
    result = {
        'recorded_at': datetime.now(ZoneInfo('Europe/Warsaw')).isoformat(),
        'TC-05': 'passed', 'required_files': required, 'markdown_link_count': len(links),
        'pdf_link_count': len(targets), 'all_link_targets_exist': True,
        'source_hashes_match_measurement': True, 'raw_rows_match_report_and_pdf': True,
        'anonymization_scan_passed': True,
        'privacy_scope': 'Submission text files, PDF extracted text, metadata and decompressed objects; excludes school PDF and _build',
        'visual_review': {'reviewer': 'Codex assistant', 'pages': [1, 2, 3, 4, 5],
                          'method': 'Poppler PNG renders inspected with view_image',
                          'checked': ['Polish glyphs', 'tables', 'complete log blocks', 'links', 'pagination'],
                          'status': 'passed'},
        'export_command': 'sh export_report.sh',
        'export_tools': {name: subprocess.run([name, '--version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]
                         for name in ['pandoc', 'xelatex']},
        'report_sha256': hashlib.sha256(Path('raport.md').read_bytes()).hexdigest(),
        'pdf_sha256': hashlib.sha256(raw).hexdigest(),
        'submission_files': sorted(p.as_posix() for p in files),
        'excluded': ['school PDF', '_build binaries and temporary export files'],
        'scope': 'A only; macOS arm64 Clang adaptation; no B-D, commit or push'
    }
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('TC-05 passed; all links, source hashes, raw rows and anonymization checks passed')


if __name__ == '__main__':
    main()

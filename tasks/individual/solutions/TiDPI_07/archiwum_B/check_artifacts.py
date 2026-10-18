"""Końcowa kontrola B; przegląd PNG jest osobną czynnością asystenta."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import zlib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

GOOD=['przebiegi/20261017_104449_232316_good1','przebiegi/20261017_104916_993218_good2']
FAULT=Path('przebiegi/20261017_104540_940321_fault')
TESTS=Path('przebiegi/20261017_104245_986516_validator_tests')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--visual-pages',help='Numery faktycznie obejrzanych stron PNG, oddzielone przecinkami')
    args=parser.parse_args()
    report=Path('raport.md').read_text()
    assert len(re.findall(r'^# ',report,re.M))==1
    assert [int(x) for x in re.findall(r'^## (\d+)\.',report,re.M)]==list(range(1,13))
    assert all(x in report for x in ['author: "Kryptonim TiDPI: Regulus"','lang: pl-PL','date: "2026-10-17"'])
    required=['raport.md','raport.pdf','benchmark.cpp','benchmark.py','generate_data.py','dane/input.txt',
              'plan_B.md','run_benchmark.py','validate_results.py','test_validate_results.py','verify_B.py',
              'kontrola_bledna/benchmark.py','kontrola_bledna/histogram_check.json','archiwum_A/integrity.json']
    assert all(Path(x).is_file() for x in required)
    destination=Path('kontrole_B/final_check.json')
    if not destination.exists():destination.write_text('{}\n')
    links=re.findall(r'\]\(([^)]+)\)',report)
    assert all(Path(x).is_file() for x in links),[x for x in links if not Path(x).is_file()]
    for root in [Path('wyniki/20261017_102226_905860_A')]+[Path(x) for x in GOOD]+[FAULT]:
        manifest=json.loads((root/'source_sha256.json').read_text())
        for name,digest in manifest.items():
            assert hashlib.sha256((root/'sources'/name).read_bytes()).hexdigest()==digest
    archive=json.loads(Path('archiwum_A/integrity.json').read_text())
    for name,digest in archive['archive_sha256'].items():
        assert hashlib.sha256((Path('archiwum_A')/name).read_bytes()).hexdigest()==digest
    tests=json.loads((TESTS/'summary.json').read_text())
    assert tests['passed']==18 and tests['failed']==0
    assert all(not (TESTS/x['name']/'results.csv').exists() for x in tests['cases'] if not x['expected_accept'])
    independent=json.loads(Path('kontrole_B/independent_check.json').read_text())
    assert independent['conclusion_repeats'] and independent['fault_rejected_no_csv']
    for name in GOOD:
        root=Path(name)
        assert json.loads((root/'validation.json').read_text())['accepted']
        assert json.loads((root/'runner_result.json').read_text())['exit_code']==0
        with (root/'results.csv').open() as f:assert len(list(csv.DictReader(f,delimiter=';')))==20
        for block in [1,2]:
            for lang in ['cpp','python']:
                for stream in ['stdout','stderr']:assert (root/f'block{block}_{lang}_{stream}.txt').is_file()
        for name,digest in json.loads((root/'source_sha256.json').read_text()).items():
            assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest
    assert not json.loads((FAULT/'validation.json').read_text())['accepted']
    assert not (FAULT/'results.csv').exists()
    assert json.loads((FAULT/'runner_result.json').read_text())['exit_code']==1
    raw=Path('raport.pdf').read_bytes()
    streams=[]
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream',raw,re.S):
        try:streams.append(zlib.decompress(m[1]))
        except zlib.error:pass
    decoded=b'\n'.join(streams)
    targets=[x.decode('ascii') for x in re.findall(rb'/(?:URI|F)\(([^()]+)\)',decoded)]
    assert len(targets)>=len(links),(len(targets),len(links))
    assert all(Path(x).is_file() for x in targets)
    text=subprocess.run(['pdftotext','-layout','raport.pdf','-'],capture_output=True,check=True).stdout
    info=subprocess.run(['pdfinfo','raport.pdf'],capture_output=True,check=True).stdout
    pages=int(re.search(rb'Pages:\s+(\d+)',info)[1])
    assert b'Kryptonim TiDPI: Regulus' in info
    assert all(x.encode() in text for x in ['Środowisko','Wykorzystanie AI','501000000','346187,5'])
    for root in [Path('wyniki/20261017_102226_905860_A')]+[Path(x) for x in GOOD]:
        for block in [1,2]:
            for lang in ['cpp','python']:
                for row in (root/f'block{block}_{lang}_stdout.txt').read_text().splitlines()[1:]:
                    assert row in report and row.encode() in text
    privacy=re.compile(rb'/(?:Users|home)/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    files=[p for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['_build','__pycache__'])
           and p.name!='TiDPI_07_Rzetelny_benchmark_Cpp_i_Python.pdf']
    for path in files:
        if path.suffix!='.pdf':assert not privacy.search(path.read_bytes()),path
    assert not privacy.search(text+info+decoded)
    # Także historyczny eksport należy do archiwum przeznaczonego do oddania.
    for command in [['pdftotext','archiwum_A/raport.pdf','-'],['pdfinfo','archiwum_A/raport.pdf']]:
        assert not privacy.search(subprocess.run(command,capture_output=True,check=True).stdout)
    visual={'status':'pending','pages':[]}
    if args.visual_pages:
        inspected=list(map(int,args.visual_pages.split(',')))
        assert inspected==list(range(1,pages+1))
        visual={'status':'passed','pages':inspected,'reviewer':'Codex assistant',
                'method':'Poppler PNG pages inspected with view_image',
                'checked':['Polish glyphs','tables','logs','link labels and targets','pagination']}
    result={'recorded_at':datetime.now(ZoneInfo('Europe/Warsaw')).isoformat(),
            'TC-12':'passed' if visual['status']=='passed' else 'pending_visual_review',
            'required_files':required,'source_snapshot_hashes_match':True,'new_sources_match_good_runs':True,
            'historical_A_preserved':True,'accepted_runs':GOOD,'fault_rejected_without_csv':True,
            'validator_tests_passed':18,'independent_arithmetic_passed':True,'markdown_link_count':len(links),
            'pdf_link_count':len(targets),'all_link_targets_exist':True,'raw_rows_match_report_and_pdf':True,
            'anonymization_scan_passed':True,'pdf_pages':pages,'visual_review':visual,
            'report_sha256':hashlib.sha256(Path('raport.md').read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256(raw).hexdigest(),'submission_files':sorted(str(x) for x in files),
            'excluded':['school PDF','_build binaries and renders','__pycache__'],
            'scope':'A history and B; no C-D; macOS arm64 Clang; no commit/push/external sending'}
    destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Checks passed; PDF pages={pages}; links={len(links)}; visual={visual['status']}")


if __name__=='__main__':main()

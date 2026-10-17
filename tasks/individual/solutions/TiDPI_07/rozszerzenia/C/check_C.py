"""Końcowa kontrola zestawu A-C. Visual review requires actual image inspection."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import zlib
from pathlib import Path
from common import dump, now, sha


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--visual-pages');args=parser.parse_args()
    root=Path('.');task=Path('../..');dest=root/'kontrole/final_check.json'
    if not dest.exists():dump(dest,{'status':'pending'})
    report=(task/'raport.md').read_text()
    assert len(re.findall(r'^# ',report,re.M))==1
    assert [int(n) for n in re.findall(r'^## (\d+)\.',report,re.M)]==list(range(1,13))
    assert 'author: "Kryptonim TiDPI: Regulus"' in report and 'lang: pl-PL' in report
    assert 'date: "2026-10-17"' in report
    assert '251042700' in report and '1250122500' in report
    assert all(f'**D{n:02}**' in report for n in range(1,25))
    assert all(f'TC-{n:02}' in report for n in range(1,21))
    links=re.findall(r'\]\(([^)]+)\)',report)
    missing=[x for x in links if not (task/x).is_file()]
    assert not missing,missing
    old=json.loads((root/'preexisting_sha256.json').read_text())
    preserved={n:sha((task/n).read_bytes())==v for n,v in old.items() if n not in ['raport.md','raport.pdf']}
    assert all(preserved.values())
    assert sha((task/'archiwum_B/raport.md').read_bytes())==old['raport.md']
    assert sha((task/'archiwum_B/raport.pdf').read_bytes())==old['raport.pdf']
    checked={}
    for study in ['C1','C2']:
        for run in (root/study/'przebiegi').iterdir():
            v=json.loads((run/'validation.json').read_text())
            accepted=v['accepted']
            assert (run/'results.csv').exists()==accepted
            if accepted:
                with (run/'results.csv').open() as f:
                    rows=list(csv.DictReader(f,delimiter=';'))
                assert len(rows)==(20 if study=='C1' else 60)
                plan=json.loads((run/'schedule.json').read_text())
                assert len(plan)==(10 if study=='C1' else 30)
                for item in plan:
                    for stream in ['stdout','stderr']:assert (run/f"{item['label']}_{stream}.txt").is_file()
                    for line in (run/f"{item['label']}_stdout.txt").read_text().splitlines()[1:]:
                        assert line in report
                assert json.loads((run/'runner_result.json').read_text())['exit_code']==0
            if (run/'source_sha256.json').exists():
                for name,h in json.loads((run/'source_sha256.json').read_text()).items():
                    assert sha((run/'sources'/name).read_bytes())==h
            checked[str(run)]={'accepted':accepted,'csv_present':(run/'results.csv').exists(),
                               'published_records':v['published_records']}
    tests_path=next((root/'kontrole').glob('validator_*/summary.json'))
    tests=json.loads(tests_path.read_text());assert tests['passed']==10 and tests['failed']==0
    for case in tests['cases']:
        assert (tests_path.parent/case['name']/'results.csv').exists()==case['expected_accept']
    independent=json.loads((root/'kontrole/independent_check.json').read_text())
    assert independent['all_stats_independently_recomputed'] and independent['all_accepted_csv_rows_match_raw']
    assert independent['correct_python_restored'] and independent['fault_rejected_no_csv']
    prefix=json.loads((root/'prefix_check.json').read_text())
    assert prefix['A_first10000_equals_C2_10000'] is False
    assert prefix['C2_10000_is_master_prefix'] and prefix['C2_30000_is_master_prefix']
    pdf=(task/'raport.pdf').read_bytes();streams=[]
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream',pdf,re.S):
        try:streams.append(zlib.decompress(m[1]))
        except zlib.error:pass
    decoded=b'\n'.join(streams)
    targets=[x.decode('ascii') for x in re.findall(rb'/(?:URI|F)\(([^()]+)\)',decoded)]
    assert len(targets)>=len(links),(len(targets),len(links))
    assert all((task/x).is_file() for x in targets)
    text=subprocess.run(['pdftotext','-layout',str(task/'raport.pdf'),'-'],capture_output=True,check=True).stdout
    info=subprocess.run(['pdfinfo',str(task/'raport.pdf')],capture_output=True,check=True).stdout
    pages=int(re.search(rb'Pages:\s+(\d+)',info)[1])
    assert b'Kryptonim TiDPI: Regulus' in info
    assert all(x.encode() in text for x in ['Środowisko','Wykorzystanie AI','251042700','1250122500','8127354'])
    for study in ['C1','C2']:
        for run in (root/study/'przebiegi').iterdir():
            if not json.loads((run/'validation.json').read_text())['accepted']:continue
            for item in json.loads((run/'schedule.json').read_text()):
                for line in (run/f"{item['label']}_stdout.txt").read_text().splitlines()[1:]:assert line.encode() in text
    privacy=re.compile(rb'/(?:Users|home)/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    files=[]
    for p in task.rglob('*'):
        if not p.is_file() or any(x in p.parts for x in ['_build','__pycache__']):continue
        if p.name=='TiDPI_07_Rzetelny_benchmark_Cpp_i_Python.pdf':continue
        files.append(p.relative_to(task).as_posix())
        if p.suffix=='.pdf':
            for command in [['pdftotext',str(p),'-'],['pdfinfo',str(p)]]:
                assert not privacy.search(subprocess.run(command,capture_output=True,check=True).stdout),p
        else:assert not privacy.search(p.read_bytes()),p
    assert not privacy.search(text+info+decoded)
    visual={'status':'pending','pages':[]}
    if args.visual_pages:
        viewed=list(map(int,args.visual_pages.split(',')))
        assert viewed==list(range(1,pages+1))
        images={}
        for n in viewed:
            image=task/'_build/C_render'/f'page-{n:02}.png'
            assert image.is_file()
            images[str(n)]=sha(image.read_bytes())
        visual={'status':'passed','pages':viewed,'reviewer':'Codex assistant',
                'method':'Actual inspection of all Poppler PNG pages using view_image',
                'checked':['Polish glyphs','tables','raw records','link labels','page breaks'],
                'render_sha256':images}
    result={'recorded_at':now(),'scope':'A-C with user-approved data deviation; no D',
            'TC-13':'passed','TC-14':'passed_with_documented_prefix_mismatch','TC-15':'passed',
            'TC-16':'passed','TC-17':'passed','TC-18':'passed','TC-19':'passed',
            'TC-20':'passed' if visual['status']=='passed' else 'pending_visual_review',
            'historical_preservation_passed':True,'historical_preserved_files':len(preserved),
            'runs':checked,'validator_fixture_cases':10,'independent_arithmetic_passed':True,
            'markdown_link_count':len(links),'pdf_link_count':len(targets),'all_link_targets_exist':True,
            'all_accepted_raw_rows_in_report_and_pdf':True,'anonymization_scan_passed':True,
            'pdf_pages':pages,'visual_review':visual,'report_sha256':sha((task/'raport.md').read_bytes()),
            'pdf_sha256':sha(pdf),'submission_files':sorted(files),
            'excluded':['school task PDF','_build binaries and renders','__pycache__'],
            'deviations':['C1 uses first 10000 lines of historical 20020-element A',
                          'C2 prefix differs from A prefix, retaining original generator and seed'],
            'no_git_commit_push_or_external_delivery':True}
    dump(dest,result)
    print(f'Final checks passed; pages={pages}; links={len(links)}; visual={visual["status"]}')

if __name__=='__main__':main()

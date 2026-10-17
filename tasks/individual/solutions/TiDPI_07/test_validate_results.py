"""Sztuczne fixture B — bez pomiarów wydajności."""
import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from validate_results import DATA_SHA, HEADER, SCHEDULE, dump


def main():
    base=Path('przebiegi')/datetime.now(ZoneInfo('Europe/Warsaw')).strftime('%Y%m%d_%H%M%S_%f_validator_tests')
    fixture=base/'fixture';fixture.mkdir(parents=True)
    shutil.copyfile('dane/input.txt',fixture/'input.txt')
    (fixture/'sources').mkdir()
    names=['benchmark.cpp','benchmark.py','generate_data.py','run_benchmark.py','validate_results.py','plan_B.md']
    for n in names: shutil.copyfile(n,fixture/'sources'/n)
    dump(fixture/'source_sha256.json',{n:hashlib.sha256((fixture/'sources'/n).read_bytes()).hexdigest() for n in names})
    dump(fixture/'schedule.json',SCHEDULE)
    dump(fixture/'environment.json',{'rounds':100,'time_unit':'ns','debugger':False,
        'data_sha256_before':DATA_SHA,'data_sha256_after':DATA_SHA,
        'flags':['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-pedantic']})
    codes={'compile':0}
    for item in SCHEDULE:
        label=f"block{item['block']}_{item['language']}";codes[label]=0
        (fixture/f'{label}_stdout.txt').write_text(HEADER+'\n'+''.join(f"{item['language']};{n};{n};501000000;true\n" for n in range(item['first_trial'],item['first_trial']+5)))
        clock='clock=steady_clock;is_steady=1;period_num=1;period_den=1000000000' if item['language']=='cpp' else json.dumps({'monotonic':True,'resolution_seconds':1e-9})
        (fixture/f'{label}_stderr.txt').write_text(clock+'\n'+''.join(f'warmup={n};time_ns=1;checksum=501000000;correct=true\n' for n in [1,2]))
    dump(fixture/'exit_codes.json',codes)
    variants=[('valid',None,None,True),('zero_time','cpp;1;1;','cpp;1;0;',True),
      ('header','time_ns','time_us',False),
      ('missing_field','cpp;1;1;501000000;true','cpp;1;1;501000000',False),
      ('extra_field','cpp;1;1;501000000;true','cpp;1;1;501000000;true;extra',False),
      ('language','cpp;1;1;','rust;1;1;',False),('wrong_producer','cpp;1;1;','python;1;1;',False),
      ('integer','cpp;1;1;','cpp;1;1.5;',False),('negative_time','cpp;1;1;','cpp;1;-1;',False),
      ('duplicate','cpp;2;2;','cpp;1;2;',False),
      ('missing_trial','cpp;1;1;501000000;true\n','',False),
      ('extra_trial','cpp;1;1;501000000;true\n','cpp;1;1;501000000;true\ncpp;11;1;501000000;true\n',False),
      ('false','cpp;1;1;501000000;true','cpp;1;1;501000000;false',False),
      ('wrong_checksum_true','cpp;1;1;501000000;true','cpp;1;1;1001000000;true',False),
      ('warmup',None,None,False),('process_exit',None,None,False),
      ('schedule',None,None,False),('data_hash',None,None,False)]
    cases=[]
    for name,old,new,accepted in variants:
        run=base/name;shutil.copytree(fixture,run)
        if old is not None:
            p=run/'block1_cpp_stdout.txt';p.write_text(p.read_text().replace(old,new,1))
        if name=='warmup':
            p=run/'block1_cpp_stderr.txt';p.write_text(p.read_text().replace('checksum=501000000','checksum=0',1))
        if name=='process_exit':
            changed=dict(codes);changed['block1_cpp']=1;dump(run/'exit_codes.json',changed)
        if name=='schedule':dump(run/'schedule.json',list(reversed(SCHEDULE)))
        if name=='data_hash':(run/'input.txt').write_text('0\n')
        if not accepted:shutil.copyfile(base/'valid/results.csv',run/'results.csv')
        before=(run/'results.csv').exists()
        proc=subprocess.run(['python3','validate_results.py',str(run)],capture_output=True)
        (run/'validator_stdout.txt').write_bytes(proc.stdout);(run/'validator_stderr.txt').write_bytes(proc.stderr)
        report=json.loads((run/'validation.json').read_text());actual=(run/'results.csv').exists()
        cases.append({'name':name,'expected_accept':accepted,'exit_code':proc.returncode,'csv_before':before,
          'csv_after':actual,'passed':proc.returncode==(0 if accepted else 1) and actual==accepted and report['accepted']==accepted,
          'rules':[x['rule'] for x in report['errors']]})
    summary={'scope':'Sztuczne fixture kontraktu, nie czasy benchmarku','cases':cases,
       'passed':sum(x['passed'] for x in cases),'failed':sum(not x['passed'] for x in cases)}
    dump(base/'summary.json',summary)
    print(base);print(f"passed={summary['passed']} failed={summary['failed']}")
    return int(summary['failed']!=0)


if __name__=='__main__':raise SystemExit(main())

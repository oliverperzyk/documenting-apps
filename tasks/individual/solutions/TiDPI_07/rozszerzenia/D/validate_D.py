"""Validate whole series before publishing any CSV; metadata stays outside raw stdout."""
from common import *
import csv,re,sys

def validate(run):
    run=Path(run)
    for name in ['results.csv','warmups.csv']:(run/name).unlink(missing_ok=True)
    errors=[];rows=[];warmups=[]
    def check(ok,rule):
        if not ok:errors.append(rule)
    try:
        env=json.loads((run/'environment.json').read_text());series=env['series'];assert series in [1,2]
        schedule=trials(series);check(json.loads((run/'schedule.json').read_text())==schedule,'SCHEDULE')
        prep=json.loads((run/'prepared.json').read_text())
        for n,h in prep['hashes'].items():
            p=run/'sources'/n if n=='plan_D.md' else run/n
            check(sha(p)==h,'PREPARED_HASH:'+n)
        check(json.loads((run/'schedules.json').read_text())==schedules(),'SCHEDULE_CONTENT')
        check(json.loads((run/'planned_trials.json').read_text())=={str(i):trials(i) for i in [1,2]},'PLANNED_TRIALS')
        source_hashes=json.loads((run/'source_sha256.json').read_text());check(set(source_hashes)==set(SOURCES),'SOURCES')
        for n,h in source_hashes.items():check(sha(run/'sources'/n)==h,'SOURCE_HASH:'+n)
        vals=[i%1001 for i in range(20020)];random.Random(20261017).shuffle(vals)
        all_data=''.join(f'{x}\n' for x in vals).encode('ascii');check(hashlib.sha256(all_data).hexdigest()==A_SHA,'A_REPRODUCTION')
        data=(run/'data/input_10000.txt').read_bytes();check(data==b''.join(all_data.splitlines(keepends=True)[:10000]),'DATA_CONTENT')
        v=list(map(int,data.split()));lo=[x for x in v if x<500];hi=[x for x in v if x>500]
        expected=100*(500*len(lo)-sum(lo)+sum(hi)-500*len(hi));check(expected==251042700,'INDEPENDENT_EXPECTATION')
        m=json.loads((run/'data_manifest.json').read_text())
        check(m['count']==10000 and m['rounds']==100 and m['expected']==expected and m['sha256']==sha(run/'data/input_10000.txt'),'DATA_MANIFEST')
        check(env['data_sha256_before']==env['data_sha256_after']==m['sha256'],'DATA_CHANGED')
        check(env['binary_sha256_before']==env['binary_sha256_after']==sha(run/'_build/benchmark'),'BINARY_CHANGED')
        check(env['flags']==FLAGS and env['debugger'] is False and env['rounds']==100 and env['count']==10000 and env['time_unit']=='ns','CONFIGURATION')
        check(env['python_version']=='3.14.4' and env['python_implementation']=='CPython' and env['architecture']=='arm64','ENVIRONMENT')
        check((run/'python_version_stdout.txt').read_text().strip()=='Python 3.14.4','PYTHON_VERSION')
        codes=json.loads((run/'exit_codes.json').read_text());events=json.loads((run/'execution.json').read_text());commands=json.loads((run/'commands.json').read_text())
        labels=['compiler_version','macOS','build','cpu','memory','python_version','compile']+[i['label'] for i in schedule]
        check(set(codes)==set(labels) and all(type(c) is int and c==0 for c in codes.values()),'EXIT_CODES')
        check([x['label'] for x in events]==labels and [x['label'] for x in commands]==labels,'EXECUTION_ORDER')
        check((run/'exit_codes.txt').read_text()==''.join(f'{k}={v}\n' for k,v in codes.items()),'EXIT_CODES_TEXT')
        for i,e in enumerate(events):
            check(e['code']==0 and prep['prepared_at']<=e['started_at']<=e['finished_at'],'EVENT_STATUS')
            check(e['start_monotonic_ns']<=e['end_monotonic_ns'],'MONOTONIC')
            if i:check(events[i-1]['end_monotonic_ns']<=e['start_monotonic_ns'] and events[i-1]['finished_at']<=e['started_at'],'SEQUENTIAL')
        argv={c['label']:c['argv'] for c in commands}
        # Fixture copies retain actual commands, so compare with original logical path.
        original=Path(argv['compile'][-1]).parent.parent if series==2 else Path(argv['compile'][-1]).parent.parent
        compile_cmd=['clang++',*FLAGS,str(original/'sources/benchmark.cpp'),'-o',str(original/'_build/benchmark')] if series==1 else ['cp',str(original.parent/'seria_1/_build/benchmark'),str(original/'_build/benchmark')]
        check(argv['compile']==compile_cmd,'RELEASE_COMMAND')
        for item in schedule:
            label=item['label'];lang=item['language']
            exe=[str(original/'_build/benchmark')] if lang=='cpp' else ['python3',str(original/'sources/benchmark.py')]
            check(argv[label]==exe+[str(original/'data/input_10000.txt'),'10000',str(expected),'1','1'],'PARAMETERS:'+label)
            lines=(run/f'{label}_stdout.txt').read_text().splitlines()
            check(len(lines)==2 and lines[0]==HEADER,'HEADER_COUNT:'+label)
            if len(lines)!=2:continue
            record=lines[1].split(';');check(len(record)==5,'FIELDS:'+label)
            if len(record)!=5:continue
            language,trial,ns,checksum,correct=record
            check(language==lang and trial=='1' and correct=='true','IDENTITY_CORRECT:'+label)
            check(bool(re.fullmatch('[0-9]+',ns)) and bool(re.fullmatch('[0-9]+',checksum)),'INTEGER:'+label)
            ns=int(ns);checksum=int(checksum);check(ns>=0 and checksum==expected,'CHECKSUM_TIME:'+label)
            rows.append(dict(item,time_ns=ns,checksum=checksum,correct=correct,source_stdout=f'{label}_stdout.txt',source_line=2,source_stderr=f'{label}_stderr.txt'))
            diagnostics=(run/f'{label}_stderr.txt').read_text().splitlines();check(len(diagnostics)==3,'DIAGNOSTICS_COUNT:'+label)
            if lang=='cpp':check(diagnostics[0]=='clock=steady_clock;is_steady=1;period_num=1;period_den=1000000000','CPP_CLOCK:'+label)
            else:
                clock=json.loads(diagnostics[0]);check(clock['monotonic'] is True and clock['resolution_seconds']>0,'PYTHON_CLOCK:'+label)
            for num,w in enumerate(diagnostics[1:],1):
                match=re.fullmatch(r'warmup=([0-9]+);time_ns=([0-9]+);checksum=([0-9]+);correct=true',w)
                check(match is not None,'WARMUP_FORMAT:'+label)
                if match:
                    number,t,c=map(int,match.groups());check(number==num and c==expected and t>=0,'WARMUP_VALUE:'+label)
                    warmups.append(dict(item,warmup=number,time_ns=t,checksum=c,source_stderr=f'{label}_stderr.txt',source_line=num+1))
        check(len(rows)==80 and len(warmups)==160,'TOTAL_COUNT')
        for s in schedules():
            for lang in ['cpp','python']:
                group=[r for r in rows if r['schedule']==s and r['language']==lang]
                check(len(group)==20 and {r['pair'] for r in group}==set(range(1,21)),'GROUP_COMPLETENESS')
                check(all(sum(r['position']==p for r in group)==10 for p in [1,2]),'POSITION_BALANCE')
    except (OSError,ValueError,KeyError,TypeError,IndexError,AssertionError) as exc:errors.append('READ_STRUCTURE:'+type(exc).__name__)
    result=dict(accepted=not errors,errors=errors,published_records=0,warmup_records=0,csv_created=False)
    if not errors:
        for name,records in [('results.csv',rows),('warmups.csv',warmups)]:
            with (run/name).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(records[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(records)
        result.update(published_records=len(rows),warmup_records=len(warmups),csv_created=True)
    dump(run/'validation.json',result)
    return result
if __name__=='__main__':
    r=validate(sys.argv[1]);print(json.dumps(r,indent=2));sys.exit(0 if r['accepted'] else 1)

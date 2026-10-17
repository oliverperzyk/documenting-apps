"""Sequential fresh processes; run from rozszerzenia/D, no benchmark concurrency."""
from common import *
import platform,subprocess,shutil,sys,time

def main():
    assert platform.python_version()=='3.14.4'
    prepared=json.loads(Path('prepared.json').read_text())
    for n,h in prepared['hashes'].items():assert sha(n)==h
    stamp=datetime.now(ZoneInfo('Europe/Warsaw')).strftime('%Y%m%d_%H%M%S_%f')
    root=Path('przebiegi')/stamp;root.mkdir(parents=True)
    for series in [1,2]:
        run=root/f'seria_{series}';run.mkdir();(run/'sources').mkdir();(run/'data').mkdir();(run/'_build').mkdir()
        for n in SOURCES:shutil.copy2(n,run/'sources'/n)
        for n in ['prepared.json','schedules.json','planned_trials.json','data_manifest.json']:shutil.copy2(n,run/n)
        shutil.copy2('data/input_10000.txt',run/'data/input_10000.txt')
        dump(run/'source_sha256.json',{n:sha(run/'sources'/n) for n in SOURCES})
        dump(run/'schedule.json',trials(series))
        commands=[];events=[];codes={}
        def call(label,argv):
            commands.append(dict(label=label,argv=argv));start=now();mono=time.monotonic_ns()
            with (run/f'{label}_stdout.txt').open('wb') as out,(run/f'{label}_stderr.txt').open('wb') as err:
                p=subprocess.run(argv,stdout=out,stderr=err,timeout=120)
            events.append(dict(label=label,started_at=start,finished_at=now(),start_monotonic_ns=mono,
                               end_monotonic_ns=time.monotonic_ns(),code=p.returncode))
            codes[label]=p.returncode
            dump(run/'commands.json',commands);dump(run/'execution.json',events);dump(run/'exit_codes.json',codes)
            (run/'exit_codes.txt').write_text(''.join(f'{k}={v}\n' for k,v in codes.items()))
            return p.returncode
        # Select compiler metadata at collection time; no private install path is captured.
        meta_cmd=['python3','-c','import subprocess,sys; p=subprocess.run(["clang++","--version"],capture_output=True); sys.stdout.buffer.write(b"\\n".join(p.stdout.splitlines()[:2])+b"\\n"); sys.stderr.buffer.write(p.stderr); sys.exit(p.returncode)']
        for label,argv in [('compiler_version',meta_cmd),('macOS',['sw_vers','-productVersion']),('build',['sw_vers','-buildVersion']),
                           ('cpu',['sysctl','-n','machdep.cpu.brand_string']),('memory',['sysctl','-n','hw.memsize']),('python_version',['python3','--version'])]:
            assert call(label,argv)==0
        build_argv=['clang++',*FLAGS,str(run/'sources/benchmark.cpp'),'-o',str(run/'_build/benchmark')] if series==1 else ['cp',str(root/'seria_1/_build/benchmark'),str(run/'_build/benchmark')]
        assert call('compile',build_argv)==0
        binary_hash=sha(run/'_build/benchmark')
        dump(run/'environment.json',dict(series=series,started_at=now(),architecture=platform.machine(),
            python_implementation=platform.python_implementation(),python_version=platform.python_version(),
            flags=FLAGS,debugger=False,count=10000,rounds=100,time_unit='ns',data_sha256_before=sha(run/'data/input_10000.txt'),
            binary_sha256_before=binary_hash,preparation=prepared['prepared_at']))
        for item in trials(series):
            exe=[str(run/'_build/benchmark')] if item['language']=='cpp' else ['python3',str(run/'sources/benchmark.py')]
            call(item['label'],exe+[str(run/'data/input_10000.txt'),'10000','251042700','1','1'])
        meta=json.loads((run/'environment.json').read_text());meta.update(finished_at=now(),
            data_sha256_after=sha(run/'data/input_10000.txt'),binary_sha256_after=sha(run/'_build/benchmark'))
        dump(run/'environment.json',meta)
        from validate_D import validate
        result=validate(run);print(run,result['accepted'],flush=True)
        if not result['accepted']:raise SystemExit(1)
    dump('latest.json',dict(root=str(root),series=[str(root/f'seria_{i}') for i in [1,2]]))
if __name__=='__main__':main()

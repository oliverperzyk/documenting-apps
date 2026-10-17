"""Rzeczywiste wywołania walidatora na oznaczonych kopiach fixture."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from common import dump, now


def main():
    p=argparse.ArgumentParser();p.add_argument('good_run',type=Path);args=p.parse_args()
    base=Path('kontrole')/('validator_'+now().replace(':','').replace('+','_'))
    base.mkdir(parents=True)
    cases=['complete','wrong_checksum_true','missing_trial','duplicate_trial','wrong_size',
           'wrong_configuration','missing_warmup','wrong_header_unit','wrong_schedule','nonzero_exit']
    results=[]
    for name in cases:
        dest=base/name
        shutil.copytree(args.good_run,dest,ignore=shutil.ignore_patterns('_build'))
        commands=json.loads((dest/'commands.json').read_text())
        for cmd in commands:
            cmd['argv']=[v.replace(str(args.good_run)+'/',str(dest)+'/') if isinstance(v,str) else v for v in cmd['argv']]
        dump(dest/'commands.json',commands)
        label='b1_10000_cpp'
        stdout=dest/f'{label}_stdout.txt';stderr=dest/f'{label}_stderr.txt'
        lines=stdout.read_text().splitlines()
        if name=='wrong_checksum_true':
            fields=lines[1].split(';');fields[3]=str(int(fields[3])+1);lines[1]=';'.join(fields)
        elif name=='missing_trial': lines.pop()
        elif name=='duplicate_trial':
            fields=lines[2].split(';');fields[1]='1';lines[2]=';'.join(fields)
        elif name=='wrong_header_unit': lines[0]=lines[0].replace('time_ns','time_us')
        stdout.write_text('\n'.join(lines)+'\n')
        if name=='missing_warmup':
            stderr.write_text('\n'.join(x for x in stderr.read_text().splitlines() if not x.startswith('warmup=2;'))+'\n')
        if name=='wrong_size':
            path=dest/'data_manifest.json';m=json.loads(path.read_text());m['data']['10000']['count']=30000;dump(path,m)
        if name=='wrong_configuration':
            path=dest/'environment.json';m=json.loads(path.read_text());m['flags']['Release']=['-std=c++17','-O0','-g'];dump(path,m)
        if name=='wrong_schedule':
            path=dest/'schedule.json';m=json.loads(path.read_text());m[0],m[1]=m[1],m[0];dump(path,m)
        if name=='nonzero_exit':
            path=dest/'exit_codes.json';m=json.loads(path.read_text());m[label]=1;dump(path,m)
        # Poprawny CSV skopiowany przed odrzuceniem sprawdza usunięcie starej publikacji.
        stale=(dest/'results.csv').exists()
        proc=subprocess.run(['python3','validate_C.py',str(dest)],capture_output=True,check=False)
        (dest/'validator_stdout.txt').write_bytes(proc.stdout);(dest/'validator_stderr.txt').write_bytes(proc.stderr)
        (dest/'validator_exit_code.txt').write_text(str(proc.returncode)+'\n')
        actual=json.loads((dest/'validation.json').read_text())
        expected=name=='complete'
        passed=(actual['accepted']==expected and (dest/'results.csv').exists()==expected and proc.returncode==(0 if expected else 1))
        results.append({'name':name,'expected_accept':expected,'passed':passed,'code':proc.returncode,
                        'had_stale_csv':stale,'errors':actual['errors']})
    dump(base/'summary.json',{'kind':'synthetic validation fixtures, not benchmark measurements','cases':results,
                             'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results)})
    print(base)
    assert all(x['passed'] for x in results),results

if __name__=='__main__':main()

from pathlib import Path
from common import *
import shutil

def main():
    if Path('prepared.json').exists():raise SystemExit('Already prepared; retain immutable plan')
    a=Path('../../dane/input.txt'); assert sha(a)==A_SHA
    data=b''.join(a.read_bytes().splitlines(keepends=True)[:10000])
    values=list(map(int,data.split()));low=[x for x in values if x<500];high=[x for x in values if x>500]
    expected=100*(500*len(low)-sum(low)+sum(high)-500*len(high))
    assert expected==251042700 and len(values)==10000
    Path('data').mkdir();Path('data/input_10000.txt').write_bytes(data)
    dump('data_manifest.json',dict(count=10000,rounds=100,seed=20261017,range=[0,1000],
        generator='[i % 1001 for i in range(20020)]; random.Random(20261017).shuffle(values); ASCII LF; first 10000 lines',
        historical_A_count=20020,historical_A_sha256=A_SHA,sha256=sha('data/input_10000.txt'),expected=expected,
        low_count=len(low),low_sum=sum(low),high_count=len(high),high_sum=sum(high),one_round=expected//100,
        deviation='A has 20020 numbers; D uses its exact 10000-line prefix, same as C1'))
    dump('schedules.json',schedules());dump('planned_trials.json',{str(i):trials(i) for i in [1,2]})
    dump('prepared.json',dict(prepared_at=now(),measurements_started=False,
        hashes={p:sha(p) for p in ['plan_D.md','schedules.json','planned_trials.json','data_manifest.json','data/input_10000.txt']}))
    print('Plan, schedules, data and independent expectation frozen before D measurements')
if __name__=='__main__':main()

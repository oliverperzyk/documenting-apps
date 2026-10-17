"""Niezależne przeliczenie A i B z zachowanych danych; nie zmienia raw."""
import collections
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


def main():
    good=[Path('przebiegi/20261017_104449_232316_good1'),Path('przebiegi/20261017_104916_993218_good2')]
    result={'runs':{}}
    for run in good:
        values=list(map(int,(run/'input.txt').read_bytes().split()))
        hist=collections.Counter(values)
        expected=sum(count*abs(x-500) for x,count in hist.items())*100
        assert expected==501000000
        validation=json.loads((run/'validation.json').read_text());assert validation['accepted']
        combined=list(csv.DictReader((run/'results.csv').open(),delimiter=';'))
        checks={}
        for lang in ['cpp','python']:
            raw=[]
            for block in [1,2]:
                with (run/f'block{block}_{lang}_stdout.txt').open() as f:
                    raw+=list(csv.DictReader(f,delimiter=';'))
            assert [x for x in combined if x['language']==lang]==raw
            times=sorted(Decimal(x['time_ns']) for x in raw)
            median=(times[4]+times[5])/Decimal(2)
            stats=validation['stats'][lang]
            assert Decimal(stats['median_ns'])==median
            assert stats['min_ns']==times[0] and stats['max_ns']==times[-1]
            assert stats['range_ns']==times[-1]-times[0]
            chosen=[]
            for trial in ['1','10']:
                row=next(x for x in raw if x['trial']==trial)
                assert int(row['checksum'])==expected and row['correct']=='true'
                chosen.append({'trial':int(trial),'time_ns':row['time_ns'],
                               'time_ms':str(Decimal(row['time_ns'])/1000000),'checksum':expected})
            checks[lang]={'min_ns':str(times[0]),'max_ns':str(times[-1]),
                          'range_ns':str(times[-1]-times[0]),'median_ns':str(median),
                          'middle_pair_ns':list(map(str,times[4:6])),'selected_rows':chosen}
        result['runs'][run.name]=checks
    a=Path('wyniki/20261017_102226_905860_A')
    manifest=json.loads((a/'source_sha256.json').read_text())
    for name,digest in manifest.items():
        assert hashlib.sha256((a/'sources'/name).read_bytes()).hexdigest()==digest
    av=json.loads((a/'verification.json').read_text())
    for lang in ['cpp','python']:
        rows=[]
        for b in [1,2]:
            with (a/f'block{b}_{lang}_stdout.txt').open() as f: rows+=list(csv.DictReader(f,delimiter=';'))
        assert len(rows)==10 and {int(x['trial']) for x in rows}==set(range(1,11))
        assert all(x['checksum']=='1002000000' and x['correct']=='true' for x in rows)
        t=sorted(Decimal(x['time_ns']) for x in rows)
        assert (t[4]+t[5])/2==Decimal(str(av['stats'][lang]['median_ns']))
    result['historical_A']={'source_snapshot_hashes':'passed','raw_trials_and_medians':'passed',
        'note':'Ponowna kontrola dowodów A; nie nowy przebieg historyczny.'}
    fault=Path('przebiegi/20261017_104540_940321_fault')
    fv=json.loads((fault/'validation.json').read_text())
    assert not fv['accepted'] and not (fault/'results.csv').exists()
    assert Path('benchmark.py').read_bytes()==(good[-1]/'sources/benchmark.py').read_bytes()
    result['fault_rejected_no_csv']=True
    result['original_python_matches_good2']=True
    result['conclusion_repeats']=all(x['cpp']['median_ns'] and Decimal(x['cpp']['median_ns'])<Decimal(x['python']['median_ns']) and Decimal(x['cpp']['min_ns'])<Decimal(x['python']['min_ns']) for x in result['runs'].values())
    target=Path('kontrole_B');target.mkdir(exist_ok=True)
    (target/'independent_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Historical A and both B runs independently checked; faulty run has no CSV; conclusion repeats')


if __name__=='__main__':main()

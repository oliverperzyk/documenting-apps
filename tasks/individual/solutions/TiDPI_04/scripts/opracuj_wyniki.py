"""Sprawdź surowe wyniki Release, odśwież tabele raportu i wykresy B/D.
Uruchom z Pythonem zawierającym matplotlib. Nie wykonuje nowych pomiarów.
"""
from pathlib import Path
from collections import defaultdict
import csv
import io
import os
import re
import argparse

ROOT = Path(__file__).resolve().parents[1]
SIZES = (500, 1000, 2000, 4000)
ORDERS = ('sorted', 'reversed', 'pseudorandom')
FIELDS = ('fingerprint', 'comparisons', 'swaps', 'passes', 'correct')
PATHS = {
    'A': 'wyniki/A_bazowy.txt',
    'seed': 'wyniki/A_zmieniony_seed.txt',
    'generator': 'wyniki/A_zmieniony_generator.txt',
    'C1': 'rozszerzenia/C/wiele_seedow/output.txt',
    'C2': 'rozszerzenia/C/bez_early_exit/output.txt',
    'D': 'rozszerzenia/D/output.txt',
}


def read(path):
    lines = path.read_text().splitlines()
    assert lines[-1] == 'all_correct=true', path
    header = next(i for i, line in enumerate(lines) if line.startswith('size;'))
    rows = list(csv.DictReader(io.StringIO('\n'.join(lines[header:-1])), delimiter=';'))
    assert all(row['correct'] == 'true' for row in rows), path
    return rows


def signature(row):
    return tuple(row[key] for key in FIELDS)


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                     '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                    ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def groups(rows, keys):
    result = defaultdict(list)
    for row in rows:
        result[tuple(row[key] for key in keys)].append(row)
    return result


def validate(data):
    for name in ('A', 'seed', 'generator'):
        rows = data[name]
        assert len(rows) == 120
        expected_seeds = {'20260499', '20260402'} if name == 'seed' else {'20260401', '20260402'}
        g = groups(rows, ('size', 'seed', 'order'))
        assert set(g) == {(str(n), s, o) for n in SIZES for s in expected_seeds for o in ORDERS}
        for samples in g.values():
            assert len(samples) == 5 and {r['trial'] for r in samples} == {'1','2','3','4','5'}
            assert len({signature(r) for r in samples}) == 1
    baseline = {(r['size'], r['seed'], r['order'], r['trial']): r for r in data['A']}
    for name in ('seed', 'generator'):
        for row in data[name]:
            original_seed = '20260401' if row['seed'] == '20260499' else row['seed']
            old = baseline[(row['size'], original_seed, row['order'], row['trial'])]
            changed = row['order'] == 'pseudorandom' and (name == 'generator' or row['seed'] == '20260499')
            if changed:
                assert row['fingerprint'] != old['fingerprint']
            else:
                assert signature(row) == signature(old)
    for row in data['A']:
        n = int(row['size'])
        if row['order'] == 'sorted':
            assert (int(row['comparisons']), int(row['swaps']), int(row['passes'])) == (n-1, 0, 1)
        if row['order'] == 'reversed':
            assert int(row['comparisons']) == int(row['swaps']) == n*(n-1)//2
    assert len([r for r in data['A'] if r['seed'] == '20260401']) == 60
    assert len(data['C1']) == 20
    assert {(r['size'], r['seed']) for r in data['C1']} == {(str(n), str(s)) for n in SIZES for s in range(20260401,20260406)}
    assert all(r['order'] == 'pseudorandom' and r['trial'] == '1' for r in data['C1'])
    for n in SIZES:
        assert len({r['fingerprint'] for r in data['C1'] if r['size'] == str(n)}) == 5
    for name, key, variants in [('C2','variant',('early','full')), ('D','algo',('bubble','std_sort'))]:
        assert len(data[name]) == 24
        g = groups(data[name], ('size', 'order'))
        assert set(g) == {(str(n),o) for n in SIZES for o in ORDERS}
        for (n,order), samples in g.items():
            assert len(samples) == 2 and {r[key] for r in samples} == set(variants)
            assert all(r['seed'] == '20260401' for r in samples)
            assert len({r['fingerprint'] for r in samples}) == 1
            by_variant = {r[key]:r for r in samples}
            early = by_variant[variants[0]]
            assert signature(early) == signature(baseline[(n,'20260401',order,'1')])
            if name == 'C2':
                full = by_variant['full']
                assert int(full['comparisons']) == int(n)*(int(n)-1)//2
                assert int(full['passes']) == int(n)-1
                assert full['swaps'] == early['swaps']
                assert int(full['comparisons']) >= int(early['comparisons'])
    repeat = ROOT/'wyniki/A_powtorzony.txt'
    repeated = read(repeat)
    assert len(repeated) == 120
    assert [{k:v for k,v in row.items() if k != 'time_us'} for row in repeated] == [{k:v for k,v in row.items() if k != 'time_us'} for row in data['A']]
    for name, filename in [('A','A_bazowy'),('seed','A_zmieniony_seed'),('generator','A_zmieniony_generator'),('C1','C_wiele_seedow'),('C2','C_bez_early_exit'),('D','D_std_sort')]:
        assert [signature(r) for r in data[name]] == [signature(r) for r in read(ROOT/'wyniki/debug'/f'{filename}.txt')]
    print('OK: kompletność A/B/C/D, poprawność, odciski, liczniki, warianty i zgodność liczników z Debug.')


def materials(data):
    report = (ROOT/'raport.md').read_text()
    a = {(n,o): sorted([r for r in data['A'] if r['size']==str(n) and r['order']==o and r['seed']=='20260401'], key=lambda r:int(r['trial'])) for n in SIZES for o in ORDERS}
    d = {(int(r['size']),r['order'],r['algo']):r for r in data['D']}
    replacements = []
    for order in ORDERS:
        replacements.append(table(['trial','fingerprint','comparisons','swaps','passes','correct','time_us [µs]'], [[r[k] for k in ('trial',)+FIELDS+('time_us',)] for r in a[500,order]]))
    # Pozostałe tabele zachowują swoją kolejność w raporcie.
    replacements.append(None)  # 2d
    seed = next(r for r in data['seed'] if r['size']=='500' and r['seed']=='20260499' and r['order']=='pseudorandom')
    seed_rows = []
    for o in ORDERS:
        changed = next(r for r in data['seed'] if r['size']=='500' and r['seed']=='20260499' and r['order']==o)
        seed_rows.append([o,a[500,o][0]['fingerprint'],changed['fingerprint'],'tak' if o=='pseudorandom' else 'nie'])
    replacements.append(table(['Układ','fingerprint seed 20260401','fingerprint seed 20260499','Zmiana?'],seed_rows))
    gen = next(r for r in data['generator'] if r['size']=='500' and r['seed']=='20260401' and r['order']=='pseudorandom')
    replacements.append(table(['Wariant','fingerprint','comparisons','swaps','passes'], [[label]+[r[k] for k in FIELDS[:4]] for label,r in [("bazowy `% 10\'000U`",a[500,'pseudorandom'][0]),("`% 9\'999U`",gen)]]))
    replacements.append(table(['n','układ','comparisons','swaps','time_us min [µs]','time_us max [µs]'], [[n,o,a[n,o][0]['comparisons'],a[n,o][0]['swaps'],min(int(r['time_us']) for r in a[n,o]),max(int(r['time_us']) for r in a[n,o])] for n in SIZES for o in ORDERS]))
    replacements.append(table(['n','układ','time_us [µs] (próby 1–5)'],[[n,o,', '.join(r['time_us'] for r in a[n,o])] for n in SIZES for o in ORDERS]))
    def growth(get, digits):
        return [f'{get(2*n)/get(n):.{digits}f}' for n in SIZES[:-1]]
    replacements.append(table(['układ','500→1000','1000→2000','2000→4000','obserwacja'], [[o]+growth(lambda n:int(a[n,o][0]['comparisons']),6)+['wzrost liniowy' if o=='sorted' else 'wzrost bliski kwadratowemu'] for o in ORDERS]))
    replacements.append(table(['n','sorted observed','n - 1','zgodne?','reversed observed','n(n - 1)/2','zgodne?'],[[n,a[n,'sorted'][0]['comparisons'],n-1,'tak',a[n,'reversed'][0]['comparisons'],n*(n-1)//2,'tak'] for n in SIZES]))
    replacements.append(table(['seed','comparisons','swaps','passes','fingerprint','correct'],[[r[k] for k in ('seed','comparisons','swaps','passes','fingerprint','correct')] for r in data['C1'] if r['size']=='500']))
    spreads=[]
    for n in (500,4000):
        rows=[r for r in data['C1'] if r['size']==str(n)]
        row=[n]
        for k in ('comparisons','swaps','passes'):
            values=[int(r[k]) for r in rows]; lo,hi=min(values),max(values)
            row.append(f'{lo}–{hi} ({hi-lo})')
        row.append(f"{len({r['fingerprint'] for r in rows})}/5");spreads.append(row)
    replacements.append(table(['n','comparisons min–max (zakres)','swaps min–max (zakres)','passes min–max (zakres)','unikalne odciski'],spreads))
    for n in (500,4000):
        keys=('order','variant','comparisons','swaps','passes','fingerprint','correct')
        replacements.append(table(['układ']+list(keys[1:]),[[r[k] for k in keys] for r in data['C2'] if r['size']==str(n)]))
    replacements.append(None)  # Rejestr kontroli
    replacements.append(table(['n','układ','bubble comparisons','std_sort comparisons'],[[n,o,d[n,o,'bubble']['comparisons'],d[n,o,'std_sort']['comparisons']] for n in SIZES for o in ORDERS]))
    replacements.append(table(['układ / algo','500→1000','1000→2000','2000→4000'],[[f'{algo} / {o}']+growth(lambda n:int(d[n,o,algo]['comparisons']),3) for algo in ('bubble','std_sort') for o in ORDERS]))
    # Pierwsza tabela to metryczka środowiska.
    matches=list(re.finditer(r'^\|[^\n]*\n\|[ :|\-]+\n(?:\|[^\n]*\n?)+',report,re.M))
    assert len(matches)==len(replacements)+1, (len(matches),len(replacements))
    for match,replacement in reversed(list(zip(matches[1:],replacements))):
        if replacement is not None:
            report=report[:match.start()]+replacement+'\n'+report[match.end():]
    lo=min(int(r['time_us']) for r in a[500,'reversed']); hi=max(int(r['time_us']) for r in a[500,'reversed'])
    report=report.replace('1313–1941',f'{lo}–{hi}')
    (ROOT/'raport.md').write_text(report)
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.build/matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,6))
    for o in ORDERS:
        ax.plot(SIZES,[int(a[n,o][0]['comparisons']) for n in SIZES],marker='o',label=o)
    ax.set(title='Liczba porównań Bubble Sort względem n (seed 20260401)',xlabel='n (liczba elementów)',ylabel='Liczba porównań')
    ax.legend(title='Układ danych');ax.grid(alpha=.3);fig.tight_layout();fig.savefig(ROOT/'images/B_porownania.png',dpi=160);plt.close(fig)
    # Dwie skale zachowują porównanie wielkości i pokazują małe serie std::sort.
    fig,axes=plt.subplots(1,2,figsize=(13,5.5))
    for ax in axes:
        for algo in ('bubble','std_sort'):
            for o in ORDERS:
                ax.plot(SIZES,[int(d[n,o,algo]['comparisons']) for n in SIZES],marker='o',label=f'{algo} / {o}')
        ax.set(xlabel='n (liczba elementów)',ylabel='Liczba porównań');ax.grid(alpha=.3)
    axes[0].set_title('Skala liniowa');axes[1].set_title('Skala logarytmiczna osi Y');axes[1].set_yscale('log');axes[1].legend(fontsize=8)
    fig.suptitle('Porównania Bubble Sort i std::sort (seed 20260401)');fig.tight_layout();fig.savefig(ROOT/'images/D_std_sort_porownania.png',dpi=160);plt.close(fig)
    print('OK: tabele raportu i wykresy B/D odświeżone z surowych danych.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Tylko sprawdzenie danych; bez zmian raportu i wykresów.')
    args=parser.parse_args()
    data={name:read(ROOT/path) for name,path in PATHS.items()}
    validate(data)
    if not args.check:
        materials(data)

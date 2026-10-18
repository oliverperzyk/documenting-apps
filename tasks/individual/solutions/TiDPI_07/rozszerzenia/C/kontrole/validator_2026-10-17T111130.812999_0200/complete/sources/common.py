"""Stałe projektu C i niezależny wzorzec (poza badaną pętlą)."""
import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo

HEADER = 'language;trial;time_ns;checksum;correct'
SEED = 20261017
A_SHA = '1e1422a8679f65bb7ec778bdbd821b74a4596431774711e89671acaa9ddca3d8'
FLAGS = {'Debug': ['-std=c++17', '-O0', '-g'],
         'Release': ['-std=c++17', '-O2', '-DNDEBUG']}
SOURCES = ['common.py', 'prepare_C.py', 'run_C.py', 'validate_C.py',
           'benchmark.cpp', 'benchmark.py', 'plan_C.md']


def now():
    return datetime.now(ZoneInfo('Europe/Warsaw')).isoformat()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def expectation(data):
    values = list(map(int, data.split()))
    if not values or any(x < 0 or x > 1000 for x in values):
        raise ValueError('DATA_RANGE')
    low = [x for x in values if x < 500]
    high = [x for x in values if x > 500]
    # Inny algorytm niż ręczne pętle benchmarków: liczności i sumy partycji.
    one = 500*len(low)-sum(low) + sum(high)-500*len(high)
    return {'count': len(values), 'sha256': sha(data), 'expected': one*100,
            'one_round': one, 'min': min(values), 'max': max(values),
            'range': [0, 1000], 'rounds': 100}


def schedule(study):
    result = []
    orders = [[10000,30000,50000],[30000,50000,10000],[50000,10000,30000],
              [10000,30000,50000],[30000,50000,10000]]
    for block in range(1,6):
        sizes = [10000] if study == 'C1' else orders[block-1]
        variants = ['Debug','Release'] if study == 'C1' else ['cpp','python']
        if block % 2 == 0:
            variants = variants[::-1]
        for size in sizes:
            for variant in variants:
                lang = 'cpp' if study == 'C1' else variant
                config = variant if study == 'C1' else ('Release' if lang == 'cpp' else 'CPython')
                result.append({'label': f'b{block}_{size}_{variant}', 'block': block,
                               'size': size, 'language': lang, 'configuration': config,
                               'first_trial': 1+2*(block-1), 'trials': 2, 'warmups': 2})
    return result

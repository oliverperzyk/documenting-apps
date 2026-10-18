"""Walidacja całego eksperymentu B; CSV powstaje wyłącznie po akceptacji."""
import argparse
import collections
import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

HEADER = 'language;trial;time_ns;checksum;correct'
DATA_SHA = '1e1422a8679f65bb7ec778bdbd821b74a4596431774711e89671acaa9ddca3d8'
SCHEDULE = [{'block': b, 'language': lang, 'first_trial': 1 + (b-1)*5,
             'warmups': 2, 'trials': 5}
            for b, langs in [(1, ['cpp', 'python']), (2, ['python', 'cpp'])] for lang in langs]


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def expectation(data):
    values = [int(x) for x in data.split()]
    if hashlib.sha256(data).hexdigest() != DATA_SHA:
        raise ValueError('DATA_HASH')
    if collections.Counter(values) != {x: 20 for x in range(1001)}:
        raise ValueError('DATA_HISTOGRAM')
    low = [x for x in values if x < 500]
    high = [x for x in values if x > 500]
    expected = (500*len(low)-sum(low) + sum(high)-500*len(high))*100
    if expected != 501000000:
        raise ValueError('INDEPENDENT_EXPECTATION')
    return expected


def validate(run):
    run = Path(run)
    output = run / 'results.csv'
    # Jedynym usuwanym plikiem jest własny wynik pochodny w katalogu przebiegu.
    if output.is_symlink():
        raise ValueError('OUTPUT_SYMLINK')
    output.unlink(missing_ok=True)
    errors, rows = [], []

    def error(rule, location):
        errors.append({'rule': rule, 'location': location})

    def check(test, rule, location):
        if not test:
            error(rule, location)
        return test

    def integer(value):
        return re.fullmatch(r'-?[0-9]+', value) is not None

    try:
        expected = expectation((run / 'input.txt').read_bytes())
        manifest = json.loads((run / 'source_sha256.json').read_text())
        for name, digest in manifest.items():
            check(hashlib.sha256((run / 'sources' / name).read_bytes()).hexdigest() == digest,
                  'SOURCE_HASH', name)
        check(set(manifest) == {'benchmark.cpp', 'benchmark.py', 'generate_data.py', 'run_benchmark.py', 'validate_results.py', 'plan_B.md'}, 'SOURCE_SET', 'source_sha256.json')
        schedule = json.loads((run / 'schedule.json').read_text())
        check(schedule == SCHEDULE, 'SCHEDULE', 'schedule.json')
        meta = json.loads((run / 'environment.json').read_text())
        check(meta['rounds'] == 100 and meta['time_unit'] == 'ns' and meta['debugger'] is False,
              'CONFIGURATION', 'environment.json')
        check(meta['data_sha256_before'] == DATA_SHA == meta['data_sha256_after'],
              'DATA_CHANGED', 'environment.json')
        check(meta['flags'] == ['-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-pedantic'], 'RELEASE_FLAGS', 'environment.json')
        codes = json.loads((run / 'exit_codes.json').read_text())
        required = {'compile'} | {f"block{x['block']}_{x['language']}" for x in SCHEDULE}
        check(set(codes) == required, 'EXIT_CODE_SET', 'exit_codes.json')
        for name, code in codes.items():
            check(type(code) is int and code == 0, 'PROCESS_EXIT', name)
        for item in SCHEDULE:
            b, lang, first = item['block'], item['language'], item['first_trial']
            label = f'block{b}_{lang}'
            content = (run / f'{label}_stdout.txt').read_text(encoding='utf-8').splitlines()
            check(bool(content) and content[0] == HEADER, 'HEADER', label)
            blockrows = list(csv.reader(content[1:], delimiter=';', strict=True))
            check(len(blockrows) == 5, 'BLOCK_COUNT', label)
            ids = []
            for line, row in enumerate(blockrows, 2):
                loc = f'{label}:{line}'
                if not check(len(row) == 5, 'FIELD_COUNT', loc):
                    continue
                check(row[0] in ('cpp', 'python') and row[0] == lang, 'LANGUAGE', loc)
                valid_ints = all(integer(x) for x in row[1:4])
                if check(valid_ints, 'INTEGER', loc):
                    trial, ns, checksum = map(int, row[1:4])
                    ids.append(trial)
                    check(ns >= 0, 'TIME_NS_NONNEGATIVE', loc)
                    check(checksum == expected, 'CHECKSUM', loc)
                    rows.append((row[0], trial, ns, checksum, row[4]))
                check(row[4] == 'true', 'CORRECT', loc)
            check(ids == list(range(first, first+5)), 'TRIAL_SEQUENCE', label)
            diagnostics = (run / f'{label}_stderr.txt').read_text(encoding='utf-8').splitlines()
            warmups = [x for x in diagnostics if x.startswith('warmup=')]
            check(len(warmups) == 2, 'WARMUP_COUNT', label)
            for i, line in enumerate(warmups, 1):
                loc = f'{label}:warmup{i}'
                match = re.fullmatch(r'warmup=([0-9]+);time_ns=(-?[0-9]+);checksum=(-?[0-9]+);correct=(true|false)', line)
                if check(match is not None, 'WARMUP_FORMAT', loc):
                    num, ns, checksum, correct = match.groups()
                    check(int(num) == i, 'WARMUP_NUMBER', loc)
                    check(int(ns) >= 0, 'WARMUP_TIME', loc)
                    check(int(checksum) == expected, 'WARMUP_CHECKSUM', loc)
                    check(correct == 'true', 'WARMUP_CORRECT', loc)
            clocklines = [x for x in diagnostics if not x.startswith('warmup=')]
            if check(len(clocklines) == 1, 'CLOCK_METADATA', label):
                if lang == 'cpp':
                    check(re.fullmatch(r'clock=steady_clock;is_steady=1;period_num=[0-9]+;period_den=[1-9][0-9]*', clocklines[0]) is not None,
                          'CPP_CLOCK', label)
                else:
                    clock = json.loads(clocklines[0])
                    check(clock['monotonic'] is True and clock['resolution_seconds'] > 0,
                          'PYTHON_CLOCK', label)
        for lang in ['cpp', 'python']:
            ids = [r[1] for r in rows if r[0] == lang]
            check(len(ids) == 10 and len(set(ids)) == 10 and set(ids) == set(range(1, 11)),
                  'TRIAL_COMPLETENESS_UNIQUENESS', lang)
    except (OSError, ValueError, KeyError, TypeError, csv.Error, UnicodeError) as exc:
        error('READ_OR_STRUCTURE', type(exc).__name__)
    result = {'accepted': not errors, 'errors': errors, 'csv_created': False,
              'expected': 501000000, 'time_unit': 'ns', 'trials_per_language': 10,
              'warmups_per_language': 4}
    if not errors:
        # Całość już zaakceptowana: dopiero teraz statystyki i eksport.
        stats = {}
        for lang in ['cpp', 'python']:
            times = sorted(r[2] for r in rows if r[0] == lang)
            stats[lang] = {'min_ns': times[0], 'max_ns': times[-1],
                           'range_ns': times[-1]-times[0],
                           'median_ns': str(Decimal(times[4]+times[5])/2),
                           'sorted_ns': times, 'middle_pair_ns': times[4:6]}
        temp = run / 'results.csv.tmp'
        with temp.open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerow(HEADER.split(';'))
            writer.writerows(rows)
        temp.replace(output)
        result.update(csv_created=True, stats=stats, published_records=len(rows))
    else:
        result['published_records'] = 0
    dump(run / 'validation.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.run)
    except (OSError, ValueError):
        print('Validation output/configuration error')
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['accepted'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

"""Ręczna pętla: 100 rund sumowania odległości od 500."""
import json
import sys
import time
from pathlib import Path

ROUNDS = 100


def calculate(values):
    result = 0
    for _ in range(ROUNDS):
        for x in values:
            d = x - 0
            if d < 0:
                d = -d
            result += d
    return result


def main():
    if len(sys.argv) != 6:
        print("usage: benchmark.py input count expected first_trial trials", file=sys.stderr)
        return 2
    try:
        count, expected, first, trials = map(int, sys.argv[2:])
        if not (1 <= count <= 50000 and 0 <= expected <= count*500*100 and
                1 <= first <= 10 and 1 <= trials <= 10 and first+trials <= 11):
            raise ValueError()
    except ValueError:
        print("invalid parameters", file=sys.stderr)
        return 2
    try:
        values = [int(x) for x in Path(sys.argv[1]).read_text(encoding="ascii").split()]
    except (OSError, ValueError):
        print("input read/parse error", file=sys.stderr)
        return 2
    if len(values) != count or any(x < 0 or x > 1000 for x in values):
        print("invalid count/range", file=sys.stderr)
        return 2
    clock = time.get_clock_info("perf_counter")
    print(json.dumps({"clock": clock.implementation, "resolution_seconds": clock.resolution,
                      "monotonic": clock.monotonic}), file=sys.stderr)
    print("language;trial;time_ns;checksum;correct")
    for offset in range(-2, trials):
        start = time.perf_counter_ns()
        checksum = calculate(values)
        stop = time.perf_counter_ns()
        correct = checksum == expected
        if offset < 0:
            print(f"warmup={offset + 3};time_ns={stop-start};checksum={checksum};correct={str(correct).lower()}", file=sys.stderr)
        else:
            print(f"python;{first+offset};{stop-start};{checksum};{str(correct).lower()}")
        if not correct:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

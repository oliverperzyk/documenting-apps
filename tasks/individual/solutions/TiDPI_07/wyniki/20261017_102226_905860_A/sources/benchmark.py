"""Ręczna pętla: 200 rund sumowania odległości od 500."""
import json
import sys
import time
from pathlib import Path

ROUNDS = 200
EXPECTED = 1002000000


def calculate(values):
    result = 0
    for _ in range(ROUNDS):
        for x in values:
            d = x - 500
            if d < 0:
                d = -d
            result += d
    return result


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("1", "6"):
        print("usage: benchmark.py input.txt first_trial(1|6)", file=sys.stderr)
        return 2
    try:
        values = [int(x) for x in Path(sys.argv[1]).read_text(encoding="ascii").split()]
    except (OSError, ValueError):
        print("input read/parse error", file=sys.stderr)
        return 2
    if len(values) != 20020 or any(x < 0 or x > 1000 for x in values):
        print("invalid count/range", file=sys.stderr)
        return 2
    clock = time.get_clock_info("perf_counter")
    print(json.dumps({"clock": clock.implementation, "resolution_seconds": clock.resolution,
                      "monotonic": clock.monotonic}), file=sys.stderr)
    print("language;trial;time_ns;checksum;correct")
    for offset in range(-2, 5):
        start = time.perf_counter_ns()
        checksum = calculate(values)
        stop = time.perf_counter_ns()
        correct = checksum == EXPECTED
        if offset < 0:
            print(f"warmup={offset + 3};time_ns={stop-start};checksum={checksum};correct={str(correct).lower()}", file=sys.stderr)
        else:
            print(f"python;{int(sys.argv[2])+offset};{stop-start};{checksum};{str(correct).lower()}")
        if not correct:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

import hashlib
import json
import random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HEADER = "language;trial;time_ns;checksum;correct"
FLAGS = ["-std=c++17", "-O2", "-DNDEBUG"]
A_SHA = "1e1422a8679f65bb7ec778bdbd821b74a4596431774711e89671acaa9ddca3d8"
SOURCES = ["benchmark.cpp", "benchmark.py", "common.py", "prepare_D.py", "run_D.py", "validate_D.py", "plan_D.md"]


def now():
    return datetime.now(ZoneInfo("Europe/Warsaw")).isoformat()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(p, v):
    Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")


def schedules():
    alt = [["cpp", "python"] if i % 2 == 0 else ["python", "cpp"] for i in range(20)]
    rnd = [["cpp", "python"] for _ in range(10)] + [["python", "cpp"] for _ in range(10)]
    random.Random(20260402).shuffle(rnd)
    return {"naprzemienny": alt, "losowany": rnd}


def trials(series):
    result = []
    for block, s in enumerate(["naprzemienny", "losowany"] if series == 1 else ["losowany", "naprzemienny"], 1):
        for pair, order in enumerate(schedules()[s], 1):
            for position, lang in enumerate(order, 1):
                result.append(
                    dict(
                        series=series,
                        schedule=s,
                        block=block,
                        pair=pair,
                        position=position,
                        language=lang,
                        label=f"{s}_p{pair:02d}_{position}_{lang}",
                        count=10000,
                        rounds=100,
                        warmups=2,
                        trials=1,
                        trial=1,
                    )
                )
    return result

"""Deterministyczny wspólny plik; uruchom z katalogu TiDPI_07."""

import hashlib
import json
import random
from pathlib import Path

COUNT = 20020
SEED = 20261017

if __name__ == "__main__":
    values = [i % 1001 for i in range(COUNT)]
    random.Random(SEED).shuffle(values)
    data = "".join(f"{x}\n" for x in values).encode("ascii")
    Path("dane").mkdir(exist_ok=True)
    Path("dane/input.txt").write_bytes(data)
    print(
        json.dumps(
            {
                "count": COUNT,
                "seed": SEED,
                "range": [0, 1000],
                "copies_per_value": 20,
                "sha256": hashlib.sha256(data).hexdigest(),
            },
            indent=2,
        )
    )

"""Utworzyć jeden plik danych używany przez benchmarki C++ i Pythona."""

import argparse
import random
from pathlib import Path


def main():
    """Wygenerować powtarzalne dane i zapisać je w UTF-8."""
    parser = argparse.ArgumentParser(description="Generate shared benchmark data.")
    parser.add_argument("output", type=Path)
    parser.add_argument("--count", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=202607)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("COUNT must be positive")

    generator = random.Random(args.seed)
    values = [generator.randint(-1000, 1000) for _ in range(args.count)]

    # Generujemy dane tylko raz, ponieważ ten sam seed nie gwarantuje identycznego
    # ciągu w różnych językach. Oba benchmarki odczytają dokładnie ten sam plik.
    args.output.write_text("\n".join(map(str, values)) + "\n", encoding="utf-8")
    print(f"Created {args.output}: count={args.count}, seed={args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

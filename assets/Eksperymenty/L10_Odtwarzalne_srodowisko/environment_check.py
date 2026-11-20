"""Zapisać metryczkę środowiska i sprawdzić możliwość odtworzenia eksperymentu."""

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def sha256(path: Path) -> str:
    """Obliczyć skrót SHA-256 bajtów pliku bez modyfikowania źródła."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    """Wczytać minimalną, wersjonowaną konfigurację eksperymentu.

    Raises:
        ValueError: Gdy struktura lub wartości konfiguracji są niepoprawne.
        OSError: Gdy pliku nie można odczytać.
    """
    # Niektóre edytory Windows zapisują opcjonalny znacznik BOM przed JSON-em.
    with path.open(encoding="utf-8-sig") as source:
        config = json.load(source)
    required = {"schema_version", "experiment_id", "data_file", "rounds", "mode"}
    missing = sorted(required - config.keys())
    if missing:
        raise ValueError(f"missing configuration fields: {', '.join(missing)}")
    if config["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported configuration schema: {config['schema_version']}")
    if not isinstance(config["rounds"], int) or config["rounds"] < 1:
        raise ValueError("rounds must be a positive integer")
    if config["mode"] not in {"comparison", "validation"}:
        raise ValueError("mode must be comparison or validation")
    return config


def build_manifest(config_path: Path) -> dict[str, Any]:
    """Zbudować metryczkę czynników istotnych dla demonstracji."""
    config = load_config(config_path)
    data_path = config_path.parent / config["data_file"]
    if not data_path.is_file():
        raise ValueError(f"data file does not exist: {data_path}")
    return {
        "manifest_schema": SCHEMA_VERSION,
        "experiment_id": config["experiment_id"],
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "config_sha256": sha256(config_path),
        "data_file": config["data_file"],
        "data_sha256": sha256(data_path),
        "rounds": config["rounds"],
        "mode": config["mode"],
    }


def compare(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    """Zwrócić czytelną listę różnic zamiast ukrywać je w wyniku testu."""
    differences = []
    for key in sorted(set(expected) | set(actual)):
        if expected.get(key) != actual.get(key):
            differences.append(f"{key}: expected={expected.get(key)!r}, actual={actual.get(key)!r}")
    return differences


def write_json(path: Path, value: dict[str, Any]) -> None:
    """Zapisać deterministyczny JSON odpowiedni do porównania i kontroli wersji."""
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    """Obsłużyć zapis wzorca albo kontrolę bieżącego środowiska."""
    parser = argparse.ArgumentParser(description="Record or verify an experiment environment.")
    parser.add_argument("command", choices=("record", "check"))
    parser.add_argument("--config", type=Path, default=Path("experiment_config.json"))
    parser.add_argument("--manifest", type=Path, default=Path("environment_manifest.json"))
    args = parser.parse_args()

    try:
        actual = build_manifest(args.config)
        if args.command == "record":
            write_json(args.manifest, actual)
            print(f"RECORDED: {args.manifest}")
            return 0
        with args.manifest.open(encoding="utf-8-sig") as source:
            expected = json.load(source)
        differences = compare(expected, actual)
        if differences:
            print("MISMATCH: environment is not identical")
            for difference in differences:
                print(f"- {difference}")
            return 1
        print("MATCH: recorded factors are identical")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

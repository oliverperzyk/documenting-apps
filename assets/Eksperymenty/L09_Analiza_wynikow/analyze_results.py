"""Walidować i opisywać serie czasów z pliku CSV bez usuwania obserwacji."""

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path


def percentile(sorted_values: list[int], fraction: float) -> float:
    """Obliczyć kwantyl metodą liniowej interpolacji między obserwacjami.

    Args:
        sorted_values: Niepusta lista wartości uporządkowanych rosnąco.
        fraction: Położenie kwantyla od 0.0 do 1.0.

    Returns:
        Wartość kwantyla, która może leżeć między dwiema obserwacjami.
    """
    position = (len(sorted_values) - 1) * fraction
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = position - lower_index
    return sorted_values[lower_index] * (1.0 - weight) + sorted_values[upper_index] * weight


def load_results(path: Path) -> dict[str, list[tuple[int, int]]]:
    """Odczytać i zwalidować wyniki pogrupowane według wariantu.

    Args:
        path: Plik CSV z separatorem średnikowym i wymaganymi kolumnami.

    Returns:
        Słownik wariantów zawierający pary (numer próby, czas w ns).

    Raises:
        ValueError: Gdy brakuje pola, wartość jest błędna albo próba się powtarza.
        OSError: Gdy pliku nie można odczytać.
    """
    required_fields = {"variant", "trial", "time_ns", "correct"}
    grouped: dict[str, list[tuple[int, int]]] = defaultdict(list)
    seen_trials: set[tuple[str, int]] = set()

    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter=";")
        if reader.fieldnames is None or not required_fields.issubset(reader.fieldnames):
            missing = sorted(required_fields - set(reader.fieldnames or []))
            raise ValueError(f"missing required columns: {', '.join(missing)}")

        for line_number, row in enumerate(reader, start=2):
            variant = row["variant"].strip()
            if not variant:
                raise ValueError(f"line {line_number}: empty variant")
            try:
                trial = int(row["trial"])
                time_ns = int(row["time_ns"])
            except ValueError as error:
                raise ValueError(f"line {line_number}: trial and time_ns must be integers") from error
            if trial < 1 or time_ns < 1:
                raise ValueError(f"line {line_number}: trial and time_ns must be positive")
            if row["correct"].strip().lower() != "true":
                raise ValueError(f"line {line_number}: incorrect functional result")
            key = (variant, trial)
            if key in seen_trials:
                raise ValueError(f"line {line_number}: duplicate trial {trial} for {variant}")
            seen_trials.add(key)
            grouped[variant].append((trial, time_ns))

    if not grouped:
        raise ValueError("file contains no data rows")
    return dict(grouped)


def describe(values: list[int]) -> dict[str, object]:
    """Policzyć jawnie zdefiniowany profil serii i oznaczyć odstające obserwacje."""
    if len(values) < 4:
        raise ValueError("each variant requires at least four trials")
    ordered = sorted(values)
    q1 = percentile(ordered, 0.25)
    q3 = percentile(ordered, 0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = [value for value in values if value < lower_fence or value > upper_fence]
    return {
        "count": len(values),
        "minimum": min(values),
        "median": statistics.median(values),
        "mean": statistics.fmean(values),
        "maximum": max(values),
        "range": max(values) - min(values),
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
        "outliers": outliers,
    }


def format_number(value: float | int) -> str:
    """Zapisać wynik z dokładnością wystarczającą do raportu demonstracyjnego."""
    return f"{value:.2f}"


def main() -> int:
    """Wczytać CSV i wypisać profil każdej kompletnej serii."""
    parser = argparse.ArgumentParser(description="Describe benchmark series and flag IQR outliers.")
    parser.add_argument("results_file", type=Path)
    args = parser.parse_args()

    try:
        grouped = load_results(args.results_file)
        for variant, trials in sorted(grouped.items()):
            profile = describe([time_ns for _, time_ns in trials])
            outlier_values = set(profile["outliers"])
            outlier_trials = [str(trial) for trial, time_ns in trials if time_ns in outlier_values]
            print(f"variant={variant}")
            print(f"  n={profile['count']}")
            print(
                "  min/median/mean/max="
                f"{profile['minimum']}/{format_number(profile['median'])}/"
                f"{format_number(profile['mean'])}/{profile['maximum']} ns"
            )
            print(f"  range={profile['range']} ns")
            print(
                f"  q1/q3/iqr={format_number(profile['q1'])}/"
                f"{format_number(profile['q3'])}/{format_number(profile['iqr'])} ns"
            )
            print(f"  fences={format_number(profile['lower_fence'])}..{format_number(profile['upper_fence'])} ns")
            print(f"  outlier_trials={','.join(outlier_trials) if outlier_trials else 'none'}")
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

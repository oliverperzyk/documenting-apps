"""Dostarczyć niewielki program do demonstracji profilowania cProfile."""


def transform_values(values: list[int]) -> list[int]:
    """Wykonać celowo kosztowne przekształcenie przygotowane do profilowania."""
    transformed = []
    for value in values:
        transformed.append(sum((value + offset) % 97 for offset in range(80)))
    return transformed


def calculate_checksum(values: list[int]) -> int:
    """Zwrócić wynik kontrolny potrzebny do wykazania wykonania pracy."""
    return sum(value * value for value in values)


def main() -> None:
    """Uruchomić obliczenia i wypisać ich wynik kontrolny."""
    values = list(range(20_000))
    transformed = transform_values(values)
    print(f"checksum={calculate_checksum(transformed)}")


if __name__ == "__main__":
    main()

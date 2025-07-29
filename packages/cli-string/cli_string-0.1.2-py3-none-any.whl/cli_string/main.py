from collections import Counter
from functools import lru_cache
from cli_string.utils import perf_counter_deco
import argparse


@perf_counter_deco
@lru_cache
def count_chars_in_string(s: str) -> str:
    """Повертає рядок, що містить лише унікальні символи з вхідного рядка."""
    if not isinstance(s, str):
        raise TypeError("Аргумент має бути рядком")
    if not s:
        raise TypeError("Рядок не може бути порожнім")
    processed_str = "".join(k.lower() for k, v in Counter(s.lower()).items() if v == 1)
    print(f"Рядок: '{s} => Унікальні символи: {processed_str}'")
    return processed_str


def main() -> None:
    """Головна функція для запуску програми."""
    parser = argparse.ArgumentParser(
        description="Підрахунок унікальних символів у рядку."
    )
    parser.add_argument("--string", type=str, help="Рядок для аналізу")
    parser.add_argument("--file", type=str, help="Шлях до файлу з рядками")
    args = parser.parse_args()
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as file:
                print("\n\n---Виконую читання з файлу---\n\n")
                lines = file.readlines()
                for line in lines:
                    count_chars_in_string(line.strip())
        except FileNotFoundError:
            print(f"Файл '{args.file}' не знайдено.")
    elif args.string:
        count_chars_in_string(args.string)
    else:
        print("Будь ласка, вкажіть рядок або файл з рядками.")


if __name__ == "__main__":
    main()

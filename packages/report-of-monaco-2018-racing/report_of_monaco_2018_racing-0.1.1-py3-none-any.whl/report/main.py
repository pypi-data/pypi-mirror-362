"""Генератор звіту про гонку F1 Monaco 2018"""

import argparse
from report.report_maker import ReportMaker


def main() -> None:
    """Головна функція для запуску генерації звіту про гонку F1 Monaco 2018."""
    parser = argparse.ArgumentParser(
        description="Генератор звіту про гонку F1 Monaco 2018",
    )
    parser.add_argument(
        "--files",
        required=True,
        help="Шлях до папки з файлами start.log, end.log та abbreviations.txt",
    )
    parser.add_argument(
        "--asc",
        action="store_true",
        help="Сортування за зростанням (за замовчуванням)",
    )
    parser.add_argument(
        "--desc",
        action="store_true",
        help="Сортування за спаданням",
    )
    parser.add_argument(
        "--driver",
        help="Показати інформацію про конкретного гонщика (по імені)",
    )

    args = parser.parse_args()
    asc = not args.desc

    report = ReportMaker(folder_path=args.files)
    report.print_report(asc=asc, driver=args.driver)


if __name__ == "__main__":
    main()

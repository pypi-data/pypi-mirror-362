"""Модуль для створення звіту про гонку F1 Monaco 2018.
Цей модуль містить клас ReportMaker, який відповідає за зчитування лог-файлів,
отримання інформації про гонщиків та формування звіту."""

import os.path
from datetime import datetime, timedelta
from pathlib import Path
import os


class ReportMaker:
    """Клас для створення звіту про гонку F1 Monaco 2018."""

    def __init__(self, folder_path: str) -> None:
        """Ініціалізує клас ReportMaker з шляхом до папки з файлами.
        :param folder_path: Шлях до папки з файлами start.log, end.log та abbreviations.txt.
        """

        self.start_file = Path(os.path.join(folder_path, "start.log"))
        self.end_file = Path(os.path.join(folder_path, "end.log"))
        self.abbreviations_file = Path(os.path.join(folder_path, "abbreviations.txt"))
        self.drivers = {}

    def get_drivers_info(self) -> None:
        """Зчитує інформацію про гонщиків з файлу abbreviations.txt."""
        with open(self.abbreviations_file) as f:
            lines = f.readlines()
            for line in lines:
                self.drivers[line[:3]] = {
                    "name": line.split("_")[1].strip(),
                    "team": line.split("_")[2].strip(),
                }

    @staticmethod
    def read_log_file(file_path) -> dict[str, str]:
        """Зчитує лог-файл і повертає словник з абревіатурами та часовими мітками.
        :param file_path: Шлях до лог-файлу (start.log або end.log)."""

        result = {}
        with file_path.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                abbreviation = line[:3]
                timestamp = line[3:]
                result[abbreviation] = timestamp
        return result

    def extract_logs(self) -> None:
        """Зчитує лог-файли start.log та end.log, обробляє їх і додає час гонщикам."""
        start_logs = self.read_log_file(self.start_file)
        end_logs = self.read_log_file(self.end_file)

        for abbreviation, start_time in start_logs.items():
            if abbreviation in end_logs:
                end_time = end_logs[abbreviation]
                end_time = datetime.strptime(end_time, "%Y-%m-%d_%H:%M:%S.%f")
                start_time = datetime.strptime(start_time, "%Y-%m-%d_%H:%M:%S.%f")
                timestamp = end_time - start_time
                if start_time >= end_time:
                    timestamp = "failed"
                self.drivers[abbreviation]["time"] = timestamp

    def build_report(self, asc=True) -> list[tuple[str, dict]]:
        """Створює звіт про гонщиків, їх команди та час проходження гонки.
        :param asc: Якщо True, то сортує за зростанням часу, якщо False - за спаданням.
        """
        self.get_drivers_info()
        self.extract_logs()
        sorted_drivers = sorted(
            self.drivers.items(),
            key=lambda item: (
                item[1]["time"] if item[1]["time"] != "failed" else timedelta.max
            ),
            reverse=not asc,
        )
        return sorted_drivers

    def print_report(self, asc=True, driver=None) -> None:
        """Друкує звіт про гонщиків у відсортованому порядку.
        :param asc: Якщо True, то сортує за зростанням часу, якщо False - за спаданням.
        :param driver: Якщо вказано, то друкує інформацію лише про цього гонщика."""

        sorted_drivers = self.build_report(asc)
        if driver:
            for i, (abbr, info) in enumerate(sorted_drivers, start=1):
                if info["name"].lower() == driver.lower():
                    time = (
                        str(info["time"])[:-3] if info["time"] != "failed" else "failed"
                    )
                    print(f"{i:>2}. {info["name"]:<18} | {info['team']:<25} | {time}")
            return
        else:
            for i, (abbr, info) in enumerate(sorted_drivers, start=1):
                time = str(info["time"])[:-3] if info["time"] != "failed" else "failed"
                print(f"{i:>2}. {info['name']:<18} | {info['team']:<25} | {time}")
                if i == 15:
                    print("-" * 64)

            return

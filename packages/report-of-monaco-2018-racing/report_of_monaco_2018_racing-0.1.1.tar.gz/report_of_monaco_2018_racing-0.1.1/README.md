# F1 Monaco 2018 Race Report Generator

A command‑line tool for parsing lap‑time logs and generating a formatted report of the F1 Monaco 2018 Grand Prix.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)

  * [Required Arguments](#required-arguments)
  * [Optional Flags](#optional-flags)
  * [Examples](#examples)
* [Project Structure](#project-structure)
* [License](#license)

## Overview

This Python utility reads three files—`start.log`, `end.log`, and `abbreviations.txt`—to compute each driver’s total lap time for the 2018 Monaco Grand Prix, then prints a sorted leaderboard. You can choose ascending or descending order, and filter by a single driver’s name.

## Features

* Parses timestamped log files and driver abbreviations.
* Calculates total race time for each competitor.
* Supports sorting results in ascending (fastest first) or descending (slowest first) order.
* Optional filtering to display a specific driver’s result.
* Clearly formatted console output with ranking, driver name, team, and time.

## Prerequisites

* Python 3.12 or higher
* Standard library only; no external dependencies

## Installation

1. Clone the repository:

   ```bash
   git clone git@git.foxminded.ua:foxstudent108448/report-of-monaco-2018-racing.git```
   ```
2. Ensure the three input files are placed in a single folder:

   * `start.log`
   * `end.log`
   * `abbreviations.txt`

## Usage

Run the script `main.py` (or whatever you rename `main.py`) with the required `--files` argument pointing to your folder.

```bash
python main.py --files /path/to/logs [--asc] [--desc] [--driver DRIVER_NAME]
```

### Required Arguments

* `--files`
  Path to the directory containing `start.log`, `end.log`, and `abbreviations.txt`.

### Optional Flags

* `--asc`
  Sort the report in ascending order (fastest times first). This is the default if neither `--asc` nor `--desc` is specified.
* `--desc`
  Sort the report in descending order (slowest times first).
* `--driver DRIVER_NAME`
  Only display the result for the driver whose full name matches `DRIVER_NAME` (case‑insensitive).

### Examples

* Generate an ascending leaderboard (default):

  ```bash
  python main.py --files ./data
  ```
* Generate a descending leaderboard:

  ```bash
  python main.py --files ./data --desc
  ```
* Show only Lewis Hamilton’s result:

  ```bash
  python main.py --files ./data --driver "Lewis Hamilton"
  ```

## Project Structure

```
f1‑monaco‑2018‑report/
├── main.py                       # Entry‑point script with argparse
├── report/
│   └── report_maker.py           # Logic to parse logs and build the report
├── data/                         # Example folder containing:
│   ├── start.log
│   ├── end.log
│   └── abbreviations.txt
└── README.md                     # This file
```

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

# prmtools

A toolkit for PRM (Parallel Reaction Monitoring) data analysis in Python.

## Features
- Fragment extraction
- Peak quality assessment
- EIC and MS2 plotting
- Results consolidation
- Command-line interface

## Installation

```bash
pip install .
```

## Usage

```bash
prmtools --input <input_file_or_dir> --output <output_dir>
```

## Structure
- `prmtools/` - Core package modules
- `prmtools/cli.py` - Command-line interface
- `setup.py` - Packaging script

## Requirements
- numpy
- pandas
- matplotlib
- scipy
- openpyxl

## License
MIT

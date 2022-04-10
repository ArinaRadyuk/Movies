# Converter

- Conversion of files from a csv format to a parquet format.
- Conversion of files from a parquet format to a csv format.
- Getting the schema of the parquet file.
- Getting info about convert.py

## Installation

```sh
pip install pandas
pip install pyarrow
```
## Usage
python3 convert.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]

1. --csv2parquet: to convert files from a csv format to a parquet format.
2. --parquet2csv: to convert files from a parquet format to a csv format.
3. --get-schema: to get the schema of the parquet file. 
4. --help: to return this message.


## Example
1. Conversion of files from a csv format to a parquet format.
```sh
python convert.py --csv2parquet dir/src-file.csv dir/dst-file.parquet
```
2. Conversion of files from a parquet format to a csv format.
```sh
python convert.py --parquet2csv dir/src-file.parquet dir/dst-file.csv
```
3. Getting the schema of the parquet file.
```sh
python convert.py --get-schema dir/src-file.parquet 
```
4. Getting info about convert.py
```sh
python convert.py --help
```




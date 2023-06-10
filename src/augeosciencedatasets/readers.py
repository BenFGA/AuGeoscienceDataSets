import re
import pandas as pd
from pathlib import Path

def dmp(file: str,
    
    header_line: int = -1,
    data_line: int = -1,
    unit_line: int = -1,
    code_line: int = -1,
    bdl_line: int = -1,
    accuracy_line: int = -1,
    udl_line: int = -1,
    preferred_line: int = -1,
    mode: str = "file",
    encoding:str='utf-8'):
    """
    simple code to import the MRT file format data into a pd.DataFrame
    https://www.dmp.wa.gov.au/Documents/Geological-Survey/GSWA-MineralExplorationTenements_Guideline.pdf

    """
    parse_string:str
    if mode == 'file':
        # check if we have a file or a string
        if isinstance(file, str):
            file = Path(file)
        # check if the file exists
        if not file.exists():
            raise FileNotFoundError(f"File {file} not found")
        with open(file,encoding=encoding) as ff:
            parse_string = ff.read()

    elif mode == 'string':
        parse_string = file.decode(encoding=encoding)
    else:
        raise ValueError(f"mode must be either 'file' or 'string' not {mode}")

    parse_string:list[str] = parse_string.split('\n')
    data, header_keys = dmp_parser(parse_string,header_line,data_line,unit_line,code_line,bdl_line,accuracy_line,udl_line,preferred_line)
    return data, header_keys

def dmp_parser(

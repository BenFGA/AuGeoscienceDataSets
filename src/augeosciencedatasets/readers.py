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
    parse_string: str,
    header_line: int = -1,
    data_line: int = -1,
    unit_line: int = -1,
    code_line: int = -1,
    bdl_line: int = -1,
    accuracy_line: int = -1,
    udl_line: int = -1,
    preferred_line: int = -1,
) -> pd.DataFrame:
    """
    parses the mrt file format into a pandas dataframe
    """
    reg_header = re.compile("H[0-9]{4}")
    parameter_names = []
    tmp_data = []
    header_keys = {}
    line_offset = []
    last_line = 0
    iters = 0
    start_file = False
    start_data = False
    printed_header = False
    for i in parse_string:
        cur_line = len(i)
        line_offset.append(cur_line + last_line)
        last_line = cur_line + last_line
        tmptext = i.replace('"', "").replace("\r", "").strip("\t").split("\t")
        # check if the first line contains 'H0002' if not break and return
        # warning
        # old files don't start with H0002 but potentially start with H0100
        # so we regexp the first section instead of search for H0002
        # some files have some extra header information so we now keep iterating until the EOF or a header row starting with H[0-9]{3}
        header = reg_header.match(tmptext[0])
        if bool(header) and not start_data:
            start_file = True
            try:
                header_keys.update(
                    {tmptext[0]: {"keys": tmptext[1], "values": tmptext[2:]}}
                )
            except IndexError:
                header_keys.update({tmptext[0]: {"keys": None, "values": None}})
            except Exception:
                pass
        if start_file and not printed_header:
            print(f"HEADER FOUND AT LINE {iters}")
            printed_header = True

        # reading the dmp file format
        # loop over each of the lines and collate the information

        if (tmptext[0] in ["H1000", "H01000"]) or (header_line == iters):
            start_data = True
            parameter_names = tmptext[1:]
            header_keys.update({"H1000": parameter_names})
        if (tmptext[0] in ["H1001", "H01001"]) or (unit_line == iters):
            units = tmptext[1:]
            header_keys.update({"H1001": units})
        if (tmptext[0] in ["H1002", "H01002"]) or (code_line == iters):
            code = tmptext[1:]
            header_keys.update({"H1002": code})

        if (tmptext[0] in ["H1003", "H01003"]) or (bdl_line == iters):
            bdl = tmptext[1:]
            header_keys.update({"H1003": bdl})

        if (tmptext[0] in ["H1004", "H01004"]) or (accuracy_line == iters):
            accuracy = tmptext[1:]
            header_keys.update({"H1004": accuracy})

        if (tmptext[0] in ["H1005", "H01005"]) or (udl_line == iters):
            udl = tmptext[1:]
            header_keys.update({"H1005": udl})
        if (tmptext[0] in ["H1006", "H01006"]) or (preferred_line == iters):
            preferred = tmptext[1:]
            header_keys.update({"H1006": preferred})
        if (tmptext[0] == "D") or (data_line == iters):
            # replace empty strings with None

            tmp_data.append(tmptext[1:])
        iters += 1
    print(iters)
    try:
        clean_parameters = []
        for i, v in enumerate(parameter_names):
            count = parameter_names[:i].count(v)
            if count == 0:
                txt = v
            else:
                txt = f"{v}.{count}"
            clean_parameters.append(txt)
        # occassionally we have weird stuff lets skip those rows
        data = pd.DataFrame(tmp_data, columns=clean_parameters)
    except ValueError:
        n_data = len(tmp_data[0])
        n_cols = len(parameter_names)
        c_cut = min([n_data, n_cols])
        print(f"Permissive Mode Engaged")
        # check that there are the right number of columns
        # if we are short append some to the end
        # if too long cut the end off

        clean_final = []
        for i, row in enumerate(tmp_data):
            r = len(row)
            insert_row = row.copy()
            if r > c_cut:
                insert_row = row[0:c_cut]
            elif r < c_cut:
                n_reps = c_cut - r
                insert_row = row.extend([""] * n_reps)
            elif r == c_cut:
                pass
            if insert_row is not None:
                clean_final.append(insert_row)
        data = pd.DataFrame(clean_final, columns=parameter_names[0:c_cut])
    return data, header_keys

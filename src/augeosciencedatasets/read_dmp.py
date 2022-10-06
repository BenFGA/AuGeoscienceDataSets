import re
import pandas as pd
def read_dmp(file:str)->pd.DataFrame:
    """
    simple code to import the MRT file format data into a pd.DataFrame
    https://www.dmp.wa.gov.au/Documents/Geological-Survey/GSWA-MineralExplorationTenements_Guideline.pdf
    """
    reg_header = re.compile('H[0-9]{4}')
    parameter_names = []
    tmp_data = []
    with open(file) as ff:
        iters = 0
        fileOK = True
        while fileOK:
            i = ff.readline()
            if len(i) == 0:
                fileOK = False
                break
            tmptext = i.replace('\n','').strip('\t').split('\t')
            # check if the first line contains 'H0002' if not break and return 
            # warning
            if iters == 0:
                # old files don't start with H0002 but potentially start with H0100
                # so we regexp the first section instead of search for H0002
                if not bool(reg_header.match(tmptext[0])):
                    fileOK = False
                    print(f'INCORRECT FORMAT {file}')
                    break
            # reading the dmp file format
            # loop over each of the lines and collate the information                
            if tmptext[0] == 'H1000':
                parameter_names = tmptext[1:]
            if tmptext[0] == 'D':
                tmp_data.append(tmptext[1:])
            iters +=1
        print(iters)
    try:
        data = pd.DataFrame(tmp_data,columns=parameter_names)
    except ValueError:
        n_data = len(tmp_data[0])
        n_cols = len(parameter_names)
        c_cut = min([n_data, n_cols])
        print(f'Permissive Mode Engaged {file}')
        data = pd.DataFrame(tmp_data,columns=parameter_names[0:c_cut])
    return data

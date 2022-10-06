import json
import urllib.parse
import urllib.request
from pathlib import Path
import shutil


def download_from_dasc(url: str, outfile: Path):
    """simple program to download from the dmp dasc a single file"""
    user_agent: str = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers: dict[str] = {"User-Agent": user_agent}
    req = urllib.request.Request(url=url, headers=headers)
    if not outfile.exists():
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            with open(outfile, "wb") as file:
                file.write(the_page)
        print(f"{outfile} has been saved!")
    else:
        print(f"{outfile} already exists!")


def download_from_csiro(url:str, basedir:Path, target_files:list[str]):
    # we are going to use the swagger api to get the files from
    # here programatically this first call here is to list all the available files
    url = "https://data.csiro.au/dap/ws/v2/collections/44783v1/data"
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
    # the variable response_text is returned as a json package we are going to parse
    # it with the python json library
    c3dmm_files = json.loads(response_text)
    base_dir = Path("data/")

    # loop over each of the files in the json
    # if you've already downloaded them then we won't download the files again.
    for i in c3dmm_files["file"]:
        # pathlib makes path handling simple I prefer it generally over the os library
        fname = Path(i["filename"])
        url = i["link"]["href"]
        # if the file names is in the list of target files let's download
        if fname.name in target_files:
            outfile = base_dir.joinpath(fname)
            # check if the folder exists if not make it
            if not outfile.parents[0].exists():
                outfile.parent.mkdir(parents=True, exist_ok=True)
            # check if the file exists if it does then don't download
            if not outfile.exists():
                # download the file
                with urllib.request.urlopen(url) as response:
                    response = response.read()
                    with open(outfile, "wb") as file:
                        file.write(response)


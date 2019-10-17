from pathlib import Path
from argparse import ArgumentParser
import urllib.request
import numpy as np
import csv

parser = ArgumentParser(description="Download and rename SDSS images from a CSV file. Can also generate imgparams.csv needed by https://github.com/SEDMORPH/PawlikMorph to analyse images")
req_grp = parser.add_argument_group(title='Required')

req_grp.add_argument("-f", "--file", required=True, type=str, help="CSV file from which files will be downloaded. File should contain the following columns in this order: objId, RA, DEC, run, rerun, camCol, field")
parser.add_argument("-F", "--folder", type=str, help="Folder where files will be saved.")
parser.add_argument("-g", "--generate", action="store_true", help="Generate imgparams.csv file.")

args = parser.parse_args()

file = Path(args.file)
folder = None
if args.folder:
    folder = Path(args.folder)

with open(file) as f:
    obj, ra, dec, run, rerun, camcol, field = np.loadtxt(f, unpack=True, skiprows=1, delimiter=",", dtype='i8,f4,f4,i4,i4,i4,i4')

# Generate imgparams file from given CSV file.
if args.generate:
    if folder:
        paramfile = folder / Path("imgparams.csv")
    else:
        paramfile = Path("imgparams.csv")

    pfile = open(paramfile, "w")
    with open(paramfile, "w") as writer:
        paramwriter = csv.writer(writer, delimiter=",", )
        paramwriter.writerow(['ra', 'dec', 'run', 'rerun', 'camCol', 'field', 'obj'])

        for (r, d, ru, rr, c, f) in zip(ra, dec, run, rerun, camcol, field):
            paramwriter.writerow([r, d, ru, rr, c, f])
    print("Generated imgparams.csv")

print(" ")
print(f"Will download ~{len(run)} files")

# Download images
for (r, rr, c, f) in zip(run, rerun, camcol, field):
    targeturl = f'http://das.sdss.org/cgi-bin/drC?RUN={r}&RERUN={rr}&CAMCOL={c}&FIELD={f}&FILTER=r'

    if folder:
        outfile = folder / f'SDSS_{r}_{rr}_{c}_{f}_r.fits'
    else:
        outfile = f'SDSS_{r}_{rr}_{c}_{f}_r.fits'

    print("Downloading " + targeturl)
    urllib.request.urlretrieve(targeturl, outfile)
    print("Saved in " / outfile)
    print(" ")

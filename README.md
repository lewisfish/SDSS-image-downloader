# SDSS-image-downloader
Small python script to help bulk download SDSS DR7 images for use with [PawlikMorph](https://github.com/SEDMORPH/PawlikMorph)

## Usage:

  sdssDLer.py -f [file] -F [folder] -g
  
  Where:
   - file is the CSV file of objID, RA, DEC, run, rerun, CamCol, field
   - folder is the location where the images will be downloaded
   - g genereates the imgparams.csv file needed by PawlikMorph

## Requires:

 - Python 3.6.5+
 - Numpy

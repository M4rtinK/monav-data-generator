#!/usr/bin/python

# preprocess Monav data
import sys
import subprocess
import os
import zipfile
import shutil

THREADS = 4

if len(sys.argv) < 2:
  print('Error: not enough arguments')
  print('Usage: ./generate.py osm_data_file [output_folder_name]')
  exit(1)

inputFile = sys.argv[1]

# if no output folder name is provided, use the filename
# without extension
if len(sys.argv) == 2:
  outputFolder = os.path.splitext(os.path.basename(inputFile))[0]
  print('## no output folder name provided ##')
  print('## using input filename (without extension) as output folder name: ##')
  print('## %s ##' % outputFolder)
else:
  outputFolder = sys.argv[2]

name = outputFolder


# get current folder
_currentFolder = os.path.dirname(os.path.abspath(__file__))

# create the output folder if it doesn't exist
if not os.path.exists(outputFolder):
  os.mkdir(outputFolder)

def zipdir(path, zipFilename):
  zip = zipfile.ZipFile(zipFilename, 'w', zipfile.ZIP_DEFLATED)
  for root, dirs, files in os.walk(path):
    for file in files:
      zip.write(os.path.join(root, file))
  zip.close()

# create car, bike and foot routing data

# first pass - import data, create address info & generate car routing data
args1 = ['monav-preprocessor', '-di', '-dro="car"', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"',
         '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="motorcar"']
# second pass - generate bike routing data
args2 = ['monav-preprocessor', '-di', '-dro="bike"', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"',
         '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="bicycle"']
# third pass - process pedestrian routing data & delete temporary files
args3 = ['monav-preprocessor', '-di', '-dro="pedestrian"', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"',
         '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="foot"', '-dd']

# convert the arguments to whitespace delimited strings and run them
subprocess.call(reduce(lambda x, y: x + " " + y, args1), shell=True)
subprocess.call(reduce(lambda x, y: x + " " + y, args2), shell=True)
subprocess.call(reduce(lambda x, y: x + " " + y, args3), shell=True)
print('## data processing done ##')

## compress the results
#print('compresing routing data')
#zipdir(outputFolder, "%s.zip" % outputFolder)
#shutil.rmtree(outputFolder)
#print('data compression done')

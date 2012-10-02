#!/usr/bin/python

# preprocess Monav data
import sys
import subprocess
import os
import zipfile
import shutil

THREADS=4

inputFile = sys.argv[1]
outputFolder = sys.argv[2]
name = sys.argv[3]


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
args1 = ['monav-preprocessor', '-di', '-dro="car"', '-da=unicode_tournament_trie', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="motorcar"']
# second pass - generate bike routing data
args2 = ['monav-preprocessor', '-dro="bike"', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="bicycle"']
# third pass - process pedestrian routing data & delete temporary files
args3 = ['monav-preprocessor', '-dro="pedestrian"', '-t=%d' % THREADS, '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="foot"', '-dd']

# convert the arguments to whitespace delimited strings and run them
os.system(reduce(lambda x, y: x+" "+y, args1))
os.system(reduce(lambda x, y: x+" "+y, args2))
os.system(reduce(lambda x, y: x+" "+y, args3))
print('data processing done')

# compress the results
print('compresing routing data')
zipdir(outputFolder, "%s.zip" % outputFolder)
shutil.rmtree(outputFolder)
print('data compression done')

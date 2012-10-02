#!/usr/bin/python

# preprocess Monav data
import sys
import subprocess
import os

inputFile = sys.argv[1]
outputFolder = sys.argv[2]
name = sys.argv[3]

# get current folder
_currentFolder = os.path.dirname(os.path.abspath(__file__))

# create the output folder if it doesn't exist
if not os.path.exists(outputFolder):
	os.mkdir(outputFolder)

# args = ['monav-preprocessor', '-s=settings.ini', '-i=%s' % inputFile, '-o=%s' % outputName, '-n=%s' % outputName, '-pi=OSM Importer', '-pro="Contraction Hierarchies"', '-pg="GPS Grid"', '-pre="OSM Renderer"', '-pa="Unicode Tournament Trie"', '-di', '-dro=Motorcar', '-dre=Online', '-da=Normal', '-dc', '-dd', '-v']

# args = ['monav-preprocessor', '-s=settings.ini', '-i=%s' % inputFile, '-o=%s' % outputName, '-n=%s' % outputName, '-pi=OSM Importer', '-pro=Contraction Hierarchies', '-pg=GPS Grid', '-pre=OSM Renderer', '-pa=Unicode Tournament Trie', '-di', '-d  ro=Motorcar', '-dre=Online', '-da=Normal', '-dc', '-dd', '-v']


# create car, bike and foot routing data

# first pass - import data, create address info & generate car routing data
args1 = ['monav-preprocessor', '-di', '-dro="car"', '-da=unicode_tournament_trie', '-t=4', '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="motorcar"']
# second pass - generate bike routing data
args2 = ['monav-preprocessor', '-dro="bike"', '-t=4', '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="bicycle"']
# third pass - process pedestrian routing data & delete temporary files
args3 = ['monav-preprocessor', '-dro="pedestrian"', '-t=4', '--verbose', '--settings="base.ini"', '--input="%s"' % inputFile, '--output="%s"' % outputFolder, '--name="%s"' % name, '--profile="foot"', '-dd']

a = ""
for i in args1:
	a+=(i + " ")
#print a

print _currentFolder
#env = {'PWD':_currentFolder}
#subprocess.call(args1, env=env)
#subprocess.Popen(args2, env=env)
#subprocess.Popen(args3, env=env)

os.system(reduce(lambda x, y: x+" "+y, args1))
os.system(reduce(lambda x, y: x+" "+y, args2))
os.system(reduce(lambda x, y: x+" "+y, args3))


print "test"
#os.system('monav-preprocessor -di -dro="car" -da=unicode_tournament_trie -t=4 --verbose --settings="base.ini" --input="czech_republic.osm.pbf" --output="cz_20121002" --name="Czech_Republic" --profile="motorcar"')

print('Monav data processing done')

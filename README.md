Monav data generator
====================
This simple script generates modRana compatible Monav routing data packs from OpenStreetMap data files (both plain osm files and pbf are supported).

Dependencies:
-------------
You need to have _monav-preprocessor_ installed (as this script is basically a wrapper around it).
The _monav-preprocessor_ package should be available from the default repositories in Debian, Ubuntu, Fedora and other major distributions.

Usage:
------
./generator.py osm_data_file [output_directory_name]

If no _output_directory_name_ is provided, the filename of the _osm_data_file_ without extension will be used instead.

Example:
--------
./generate.py czech_republic.osm.pbf Czech_Republic_2012

Multiprocessing
---------------
The Monav preprocessor can run a part the conversion in multiple threads, speeding the whole process quite a bit. By default, 4 threads are used.

To set the thread number, just edit the THREADS variable in the _generate.py_ file. The number of threads should roughly correspond to the number of logical processing cores on your machine.

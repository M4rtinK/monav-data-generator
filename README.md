Monav data generator
====================
This simple script generates modRana compatible Monav routing data packs from OpenStreetMap data files (both plain osm files and pbf are supported).

Dependencies:
-------------
You need to have _monav-preprocessor_ installed (as this script is basically a wrapper around it).

Usage:
------
./generator.py osm_data_file output_directory data_pack_name

Example:
--------
./generate.py czech_republic.osm.pbf czech_Republic_2012 Czech_Republic

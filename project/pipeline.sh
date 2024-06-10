#!/bin/bash
python ./pipeline.py

rm ../data/asylum-decisions.csv
rm ../data/GlobalLandTemperaturesByCity.csv
rm ../data/GlobalLandTemperaturesByMajorCity.csv
rm ../data/GlobalLandTemperaturesByState.csv
rm ../data/GlobalTemperatures.csv


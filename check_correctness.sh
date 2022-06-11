#!/bin/bash

# Run this to check that the ILP solution is the same as the PRIM solution (i.e. is correct)

rm ./images/*
python3 ilp.py ./instances/$1.txt 0 --visual
mv ./images/$1.txt.gv.pdf ./images/ILP$1.txt.gv.pdf
python3 prim.py ./instances/$1.txt --visual
mv ./images/$1.txt.gv.pdf ./images/PRIM$1.txt.gv.pdf
rm ./images/$1.gv
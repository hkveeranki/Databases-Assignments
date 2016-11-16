#!/bin/sh
outfile="output/201401145_output"
mkdir output
rm -f $outfile
touch $outfile
python Runner.py "input/1MB_50Percent 5 1048576" >> $outfile # for input_1
python Runner.py "input/100MB_20Percent 5 1048576" >> $outfile # for input_2
# 1MB = 1048576 Bytes 

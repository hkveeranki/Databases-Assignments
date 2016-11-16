#!/bin/sh
outfile="output/201401145_output"
rm -f $outfile
touch $outfile
python Runner.py "input/1MB_50Percent" >> $outfile # for input_1
python Runner.py "input/100MB_20Percent 5 " >> $outfile # for input_2

#!/bin/sh
outfile="output/201401145_output"
mkdir -p output
rm -f $outfile
touch $outfile
python code/Runner.py "input/100MB_20Percent 3 1048576 2" >> $outfile # for input_2
python code/Runner.py "input/100MB_20Percent 3 1048576 1" >> $outfile # for input_2
python code/Runner.py "input/1MB_50Percent 3 1048576 2" >> $outfile # for input_1
python code/Runner.py "input/1MB_50Percent 3 1048576 1" >> $outfile # for input_1
python code/Runner.py "input/100MB_20Percent 5 2097152 2" >> $outfile # for input_2
python code/Runner.py "input/100MB_20Percent 5 2097152 1" >> $outfile # for input_2
python code/Runner.py "input/1MB_50Percent 5 2097152 2" >> $outfile # for input_1
python code/Runner.py "input/1MB_50Percent 5 2097152 1" >> $outfile # for input_1
python code/Runner.py "input/100MB_20Percent 10 104858 2" >> $outfile # for input_2
python code/Runner.py "input/100MB_20Percent 10 104858 1" >> $outfile # for input_2
python code/Runner.py "input/1MB_50Percent 10 104858 2" >> $outfile # for input_1
python code/Runner.py "input/1MB_50Percent 10 104858 1" >> $outfile # for input_1
# 1MB = 1048576 Bytes 

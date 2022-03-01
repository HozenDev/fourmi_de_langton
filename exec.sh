#!/bin/bash

date > log.txt

echo '-----------------' >> log.txt
echo '   python_code   ' >> log.txt
echo '-----------------' >> log.txt

cd ./src/

python3 main.py 2>> ../log.txt

if [ $? -ne 0 ]
then
	echo 'Error in main.py : results in log.txt'
	cd ../log.txt
	exit 1
fi

cd ../

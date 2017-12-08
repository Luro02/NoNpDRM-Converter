@echo off

cd ..
IF EXIST *.tsv del /Q *.tsv
IF EXIST *.csv del /Q *.csv

pause
exit
@echo off

for /d %%i in (*) do (
	echo %%i >> input.txt
)

pause
exit
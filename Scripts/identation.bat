@echo off

cd ..

for %%i in (*.py) do (
autopep8 -i %%i
)

pause
exit
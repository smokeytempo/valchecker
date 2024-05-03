@echo off

cd src
set /P choice="debug [d] consolemode [c] normal [enter]:"
if "%choice%" == "d" (
    python main.py -d
) else if "%choice%" == "c" (
    python main.py -c
) else (
    python main.py
)
pause
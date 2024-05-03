@echo off

echo install requirements
where pip > nul 2>&1 || (
    echo "pip is not installed. Please install pip before running this script."
    pause
    exit /b
)
pip install -r requirements.txt > nul
echo install requirements done

set /P choice="Do you want to run the program now? (y/n): "

if "%choice%" == "y" (
    set /P consolemode=""Do you want to run the program in console mode? (y/n): "
    if "%consolemode%" == "y" (
        cd src
        python main.py -c
    ) else (
        cd src
        python main.py
    )
) else (
    echo You can run the program by typing 'python main.py' in the terminal
)

pause
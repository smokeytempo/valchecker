@echo off

echo install requirements
pip install -r requirements.txt > nul
echo install requirements done

set /P choice="Do you want to run the program now? (y/n): "

if "%choice%" == "y" (
        python main.py
    )
) else (
    echo You can run the program by typing 'python main.py' in the terminal
)

pause
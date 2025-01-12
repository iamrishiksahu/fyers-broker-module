@echo off

:: Step 1: Create a virtual environment if it doesn't exist
if not exist "fyers\Scripts\activate.bat" (
    python -m venv fyers
    echo Virtual environment 'fyers' created.
) else (
    echo Virtual environment 'fyers' already exists.
)

:: Step 2: Activate the virtual environment
call fyers\Scripts\activate.bat

:: Step 3: Check if packages are already installed
pip freeze > installed_requirements.txt
findstr /i /g:requirements.txt installed.txt > nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
) else (
    echo Required packages are already installed.
)

:: Step 4: Run the project
echo Running the project...
python -m fyers

:: Check if the command ran successfully
if %errorlevel% neq 0 (
    echo There was an error running the project.
) else (
    echo The project ran successfully.
)


:: Deactivate the virtual environment
deactivate

:: Keep the window open
echo.
echo Press any key to exit...
pause > nul
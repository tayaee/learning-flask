@echo off
setlocal enabledelayedexpansion

if exist setenv.bat (
    call setenv.bat > NUL 2>&1
    echo %~nx0 line 6 DEBUG setenv.bat: FINDSTR_REGEX_FOR_PATH=!FINDSTR_REGEX_FOR_PATH!
    echo %~nx0 line 7 DEBUG setenv.bat: PATH_TO_BASE_PYTHON=!PATH_TO_BASE_PYTHON!
    echo "%PATH%" | findstr /r "!FINDSTR_REGEX_FOR_PATH!" > NUL 2>&1 || set "PATH=!PATH_TO_BASE_PYTHON!;%PATH%"
)

python -V 2>NUL | findstr /i /c:"Python 3" > NUL && (
    echo %~nx0 line 12 DEBUG Found base Python 3.x
) || (
    echo %~nx0 line 14 ERROR Python 3 is not available in PATH, exit.
    goto :eof
)

if .%1. == .. (
    if exist setenv.bat (
        call setenv.bat > NUL 2>&1
        echo %~nx0 line 21 DEBUG setenv.bat: APPNAME=!APPNAME!
    ) else (
        for %%a in ("%CD%") do set APPNAME=%%~nxa
    )
    for /f "usebackq tokens=1-2" %%a in (`python -V`) do set PYTHON_VER=%%b
    set VENV_DIR=%userprofile%\.venvs\!PYTHON_VER!.!APPNAME!
) else (
    set VENV_DIR=%1
)
echo %~nx0 line 30 DEBUG Using VENV_DIR=!VENV_DIR!
if exist !VENV_DIR! (
    echo %~nx0 line 32 DEBUG Found !VENV_DIR!
    if exist !VENV_DIR!\Scripts\activate.bat (
        echo %~nx0 line 34 DEBUG Found !VENV_DIR!\Scripts\activate.bat
        call !VENV_DIR!\Scripts\activate.bat
    )
) else (
    echo %~nx0 line 38 DEBUG Creating !VENV_DIR!
    echo %~nx0 line 39 DEBUG python -m venv !VENV_DIR!
    python -m venv !VENV_DIR! && (
        echo %~nx0 line 41 DEBUG Created !VENV_DIR!
        if exist !VENV_DIR!\Scripts\activate.bat (
            echo %~nx0 line 43 DEBUG Found !VENV_DIR!\Scripts\activate.bat
            call !VENV_DIR!\Scripts\activate.bat
        )
        echo %~nx0 line 46 DEBUG python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
        python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
    ) || (
        echo %~nx0 line 49 ERROR python -m venv !VENV_DIR!
        exit /b 1
    )
)

(
    echo @echo off
    echo set "VENV_DIR=!VENV_DIR!"
    echo set "ACTIVATE_BAT=!VENV_DIR!\Scripts\activate.bat"
    echo set "PYTHON_EXE=!VENV_DIR!\Scripts\python.exe"
) > tmp.venv.bat

if exist requirements.txt (
    echo %~nx0 line 62 DEBUG Found requirements.txt
    echo %~nx0 line 63 DEBUG Checking installed packages...
    python -c "import pkg_resources; pkg_resources.require(open('requirements.txt', mode='r'))" > NUL 2>&1 && (
        echo %~nx0 line 65 DEBUG requirements.txt OK
    ) || (
        echo %~nx0 line 67 DEBUG pip install --ignore-installed -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
        pip install --ignore-installed -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
    )
)

echo %~nx0 line 72 DEBUG !VENV_DIR!\Scripts\python.exe is ready.
endlocal & call %VENV_DIR%\Scripts\activate.bat

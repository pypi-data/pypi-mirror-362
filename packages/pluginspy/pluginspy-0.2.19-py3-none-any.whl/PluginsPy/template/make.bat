@ECHO OFF

pushd %~dp0

REM Command file for ALogAnalyze

if "%1" == ""         goto all
if "%1" == "all"      goto all
if "%1" == "cmd"      goto cmd

echo.
echo.usage:
echo.	make
echo.	make all
echo.	make qt
echo.

goto end

:all
python3 main.py qt
goto end

:cmd
python3 main.py
goto end

:end
popd

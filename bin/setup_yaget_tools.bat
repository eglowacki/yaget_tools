echo off
echo Copyright 2021 (c) by yaget
echo This will add yaget tool folder '%~dp0' to system path. The folder contains following files:
dir /B
::echo Current Path [%path%]
echo Add this path (y/n)?
set /p choice= 
if /I "%choice%"=="y" GOTO add
if /I "%choice%"=="n" GOTO end

:add
echo %path% > old_path.txt

:: echo -setx path "%path%;%~dp0"
echo Added '%~dp0' path (old and new path are saved in old_path.txt and new_path.txt files respectively).
echo %path% > new_path.txt
GOTO quit

:end
echo No Changes to path.

:quit

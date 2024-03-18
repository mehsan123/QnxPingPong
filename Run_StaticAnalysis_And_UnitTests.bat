@echo off
setlocal enableextensions enabledelayedexpansion
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 12/03/2024                                      |
rem |                                                             |
rem |    Copyright (C) 2024 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_ldra_toolsuite\1021_final
set TLP=C:\_ldra_toolsuite\1021_final\Compiler_spec\Qnx\Qnx_momentics8_arm64\
set PRJ=QNX_PingingSemaphores
set COMPILER=QNX Momentics v8 ARM64
set PATH=%TBED%;%PATH%
set ROOT=%~dp0
set CONFIG_DIR=%ROOT%Configuration

rem Configure relative paths 
rem ========================
set SRC_FILES=%ROOT%..\%PRJ%.tcf
set WORK=C:\_ldra_workarea\1021_final\%PRJ%_tbwrkfls

set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Profile="C/C++ %COMPILER%"
if exist "%TBED%\contestbed.exe" (
  set TOOL=start "ldra" /wait /min contestbed
  set RUN=start "ldra" /wait /min contbrun
) else (
  set TOOL=start "ldra" /wait /min conunit
  set RUN=start "ldra" /wait /min ldraconunit
)


@echo Set the compiler
%TBI% COMPILER_SELECTED="%COMPILER%"
%TBS% METFILE=%CONFIG_DIR%\Metpen.dat
rem %TBS% BUILD_OPTIONS_FILE="%TESTBEDINI%"
rem %TBS% TBRUN_BUILD_OPTIONS_FILE="%TBRUNINI%"


@echo Delete Existing Results
%TOOL% /delete_set=%PRJ%
if exist %WORK% rmdir /s /q %WORK%

@echo Run Analysis
%TOOL% %SRC_FILES% /112a34q


set TESTS=0
set TCF_ROOT=%ROOT%TestCases
for %%i in ("%TCF_ROOT%\*.tcf") do set /A TESTS=TESTS+1

@echo Regressing !TESTS! TCFs
set TEST=0
for %%i in ("%TCF_ROOT%\*.tcf") do (
  set /A TEST=TEST+1
  %RUN% %SRC_FILES% -tcf=%%i -tcf_mode=retain -regress -quit
  set status=!errorlevel!
  if !status! == 0 echo !TEST! : [32mPass %%i[0m
  if !status! == 64 echo !TEST! : [31mFail %%i Invalid command line[0m
  if !status! == 65 echo !TEST! : [31mFail %%i Input data incorrect[0m
  if !status! == 70 echo !TEST! : [31mFail %%i Internal software limitation[0m
  if !status! == 73 echo !TEST! : [31mFail %%i Can't create output file or directory[0m
  if !status! == 80 echo !TEST! : [31mFail %%i Main static analysis phase incomplete[0m
  if !status! == 81 echo !TEST! : [31mFail %%i Instrumentation failed[0m
  if !status! == 82 echo !TEST! : [31mFail %%i Dynamic coverage failed[0m
  if !status! == 83 echo !TEST! : [31mFail %%i Other analysis failed[0m
  if !status! == 84 echo !TEST! : [31mFail %%i Build failed[0m
  if !status! == 85 echo !TEST! : [31mFail %%i Execution of instrumented program failed[0m
  if !status! == 90 echo !TEST! : [31mFail %%i Regression failure[0m
  if !status! == 91 echo !TEST! : [31mFail %%i Build failure[0m
  if !status! == 92 echo !TEST! : [31mFail %%i Failed to execute[0m
  if !status! == 93 echo !TEST! : [31mFail %%i Execution timed out[0m
  if !status! == 94 echo !TEST! : [31mFail %%i Validation failure[0m
  if !status! == 95 echo !TEST! : [31mFail %%i Validation failure[0m
  if !status! == 103 echo !TEST! : [31mFail %%i Licensing error[0m
)


@echo Dynamic Data Flow Coverage
%TOOL% %SRC_FILES% /325q

@echo Generate Test Manager Report
%TOOL% %SRC_FILES% /generate_overview_rep

@echo Open Test Manager Report
if exist "%WORK%\%PRJ%_reports\%PRJ%.ovs.htm" "%WORK%\%PRJ%_reports\%PRJ%.ovs.htm"
if exist "%WORK%\%PRJ%.ovs.htm" "%WORK%\%PRJ%.ovs.htm"

pause

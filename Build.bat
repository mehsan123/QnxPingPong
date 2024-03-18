@echo off
rem =========================================
set Q_PATH=C:\Users\Ehsan\qnx800\
set Q_UNIX_PATH=%Q_PATH:\=/%
set Q_PLATFORM=aarch64le
rem =========================================

set PATH=%Q_PATH%host\win64\x86_64\usr\bin;%PATH%
set MAKEFLAGS=-I%Q_UNIX_PATH%target/qnx/usr/include
set QNX_HOST=%Q_UNIX_PATH%host/win64/x86_64
set QNX_TARGET=%Q_UNIX_PATH%target/qnx
set HOME=%Q_UNIX_PATH%

@echo on

if exist *.btf del /F *.btf
if exist *.ptf del /F *.ptf

make -j8 clean
make -j8 all

if errorlevel 1 pause

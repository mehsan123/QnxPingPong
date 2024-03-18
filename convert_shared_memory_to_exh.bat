@echo off
set tbed=C:\_ldra_toolsuite\1021_final
set tlp=C:\_ldra_toolsuite\1021_final\Compiler_spec\Qnx\Qnx_momentics8_arm64\
if exist %tbed%\Utils\Python\Lib\xmllib.py (
  set python_path=%TBED%\Utils\Python
) else (
  set python_path=C:\Python27
)
set path=%tbed%;%path%
if not exist "%python_path%\python.exe" (
  @echo Can't find python.exe in %python_path%
  pause
  exit
)

"%python_path%\python.exe" "%tlp%convert_shared_memory_to_exh.py" theSharedMemory.dat

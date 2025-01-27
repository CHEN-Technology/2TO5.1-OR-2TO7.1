@echo off
REM 提示用户可能需要管理员权限
echo 请注意：此脚本可能需要管理员权限才能正确运行。

REM 检测操作系统并选择合适的激活命令
if "%OS%"=="Windows_NT" (
    set ACTIVATE_SCRIPT=.\venv\Scripts\activate
) else (
    set ACTIVATE_SCRIPT=source venv/bin/activate
)

REM 激活虚拟环境
call %ACTIVATE_SCRIPT%

REM 运行主程序，并添加错误处理
python ./main.py || goto :error

goto :end

:error
echo 发生错误，请检查日志并尝试重新运行脚本。
pause
exit /b 1

@echo off

REM 运行主程序，并添加错误处理
.\python\python main.py || goto :error

goto :end

:error
echo 发生错误，请检查日志并尝试重新运行脚本。
pause
exit /b 1
@echo off

REM ���������򣬲���Ӵ�����
.\python\python main.py || goto :error

goto :end

:error
echo ��������������־�������������нű���
pause
exit /b 1
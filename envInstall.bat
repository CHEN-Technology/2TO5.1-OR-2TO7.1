@echo off

REM ���������򣬲���Ӵ�����
.\python\python -m pip install -r requirements.txt || goto :error

goto :end

:error
echo ��������������־�������������нű���
pause
exit /b 1
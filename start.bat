@echo off
REM ��ʾ�û�������Ҫ����ԱȨ��
echo ��ע�⣺�˽ű�������Ҫ����ԱȨ�޲�����ȷ���С�

REM ������ϵͳ��ѡ����ʵļ�������
if "%OS%"=="Windows_NT" (
    set ACTIVATE_SCRIPT=.\venv\Scripts\activate
) else (
    set ACTIVATE_SCRIPT=source venv/bin/activate
)

REM �������⻷��
call %ACTIVATE_SCRIPT%

REM ���������򣬲���Ӵ�����
python ./main.py || goto :error

goto :end

:error
echo ��������������־�������������нű���
pause
exit /b 1

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
python -m venv venv

REM �������⻷��
call %ACTIVATE_SCRIPT%

REM ��װ������������Ӵ�����
pip install pydub pySoundFile ffmpeg || goto :error
curl -O https://www.ghproxy.cn/https://github.com/facebookresearch/demucs/archive/refs/tags/v4.0.1.zip
unzip -n v4.0.1.zip -d v4.0.1
cd v4.0.1/demucs-4.0.1
pip install .
cd ../../
del v4.0.1.zip
rmdir /Q /S v4.0.1
pip install torch torchvision torchaudio --index-url https://mirror.sjtu.edu.cn/pytorch-wheels/cu124 || goto :error

goto :end

:error
echo ��������������־�������������нű���
pause
exit /b 1

:end
echo ������װ��ɡ�
pause
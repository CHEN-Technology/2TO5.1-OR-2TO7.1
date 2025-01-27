@echo off
REM 提示用户可能需要管理员权限
echo 请注意：此脚本可能需要管理员权限才能正确运行。

REM 检测操作系统并选择合适的激活命令
if "%OS%"=="Windows_NT" (
    set ACTIVATE_SCRIPT=.\venv\Scripts\activate
) else (
    set ACTIVATE_SCRIPT=source venv/bin/activate
)

REM 创建虚拟环境
python -m venv venv

REM 激活虚拟环境
call %ACTIVATE_SCRIPT%

REM 安装依赖包，并添加错误处理
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
echo 发生错误，请检查日志并尝试重新运行脚本。
pause
exit /b 1

:end
echo 环境安装完成。
pause
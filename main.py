import shutil
import subprocess
import os
import sys
import gc
from pydub import AudioSegment
from tkinter import Tk, filedialog


def update_progress(current_step, total_steps):
    done = int(100 * current_step / total_steps)
    progress_bar = f"{'=' * done}{' ' * (100 - done)}"
    print(f"\r混音进度: [{progress_bar}] {done}%", end="")
    sys.stdout.flush()


def finally_del(output_file, output_directory, channel_count):
    shutil.rmtree(os.path.join(output_directory, "htdemucs_ft"))

    print(f"\n音频已混音为 {channel_count}.1 通道并保存为 {output_file}")


def remix_channels(input_dir, output_file, channel_count):
    print(f"开始混音为 {channel_count}.1 通道，由 {input_dir} 到 {output_file}")

    total_steps = 5
    current_step = 0

    # 定义声道文件列表
    channels = ["vocals", "bass", "drums", "other"]
    mono_segments = []

    for channel in channels:
        channel_file = os.path.join(input_dir, f"{channel}.wav")
        if os.path.isfile(channel_file):
            audio = AudioSegment.from_file(channel_file)
            if channel_count == 5:
                if f"{channel}.wav" == "vocals.wav":
                    # 如果是 vocals 文件，直接使用
                    mono_segments.append(audio.set_channels(1))
                elif f"{channel}.wav" == "bass.wav":
                    mono_segments.append(audio.set_channels(1))
                else:
                    if audio.channels == 2:  # 如果是立体声文件
                        left_channel = audio.split_to_mono()[0]
                        right_channel = audio.split_to_mono()[1]

                        mono_segments.append(left_channel)
                        mono_segments.append(right_channel)
                    else:
                        # 如果已经是单声道文件，直接使用
                        mono_segments.append(audio.set_channels(1))
            elif channel_count == 7:
                if f"{channel}.wav" == "vocals.wav":
                    # 如果是 vocals 文件，直接使用
                    mono_segments.append(audio.set_channels(1))
                elif f"{channel}.wav" == "bass.wav":
                    mono_segments.append(audio.set_channels(1))
                else:
                    if audio.channels == 2:  # 如果是立体声文件
                        left_channel = audio.split_to_mono()[0]
                        right_channel = audio.split_to_mono()[1]

                        mono_segments.append(left_channel)
                        mono_segments.append(right_channel)
                    else:
                        # 如果已经是单声道文件，直接使用
                        mono_segments.append(audio.set_channels(1))
        else:
            print(f"文件 {channel_file} 不存在，跳过处理")
            mono_segments.append(AudioSegment.silent(
                duration=0, frame_rate=48000))

    current_step += 1
    update_progress(current_step, total_steps)

    # 调整音频文件的采样率
    for i, segment in enumerate(mono_segments):
        mono_segments[i] = segment.set_frame_rate(48000)

    current_step += 1
    update_progress(current_step, total_steps)

    # 创建一个静音的声道音频对象（采样率 48kHz）
    silence = AudioSegment.silent(
        duration=len(mono_segments[0]), frame_rate=48000)

    current_step += 1
    update_progress(current_step, total_steps)

    # 混音为指定声道格式
    if channel_count == 5:
        mono_segments = [
            mono_segments[2],  # 左前
            mono_segments[3],  # 右前
            mono_segments[0],  # 中置
            mono_segments[1],  # 低音
            mono_segments[4],  # 左后
            mono_segments[5],  # 右后
        ]
    elif channel_count == 7:
        mono_segments = [
            mono_segments[2],  # 左前
            mono_segments[3],  # 右前
            mono_segments[0],  # 中置
            mono_segments[1],  # 低音
            mono_segments[4],  # 左后
            mono_segments[5],  # 右后
            mono_segments[4],  # 左后环绕
            mono_segments[5],  # 右后环绕
        ]

    current_step += 1
    update_progress(current_step, total_steps)

    mixed_audio = AudioSegment.from_mono_audiosegments(
        *mono_segments).set_channels(channel_count + 1)

    current_step += 1
    update_progress(current_step, total_steps)
    print()

    # 导出为多声道音频文件
    mixed_audio.export(output_file, format="flac")

    # 删除分离的音频文件
    for file in ["vocals.wav", "bass.wav", "drums.wav", "other.wav"]:
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"删除分离的音频文件: {file_path}")

    gc.collect()


def separate_audio(input_file, output_dir, real_output_directory, hardware_choice):
    print(f"分离音频文件: {input_file} 到 {output_dir}")
    os.environ["TORCH_HOME"] = "./model"
    if hardware_choice == "1":
        os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"] = "0"
        args = [".\\Python\\python", "-m", "demucs", "-n", "htdemucs_ft", "-o",
                output_dir, input_file, "--float32"]
    elif hardware_choice == "2":
        args = [".\\Python\\python", "-m", "demucs", "-n", "htdemucs_ft", "-o",
                output_dir,  input_file, "--float32", "-d", "cpu"]
    print(f"执行命令: {' '.join(args)}")
    result = subprocess.run(args, check=True)
    print(f"音频文件已分离到: {real_output_directory}")

    gc.collect()


def main():
    print("立体声转5.1声道&7.1声道混音工具 v1.0 by 陈缘科技")
    print()

    segment = "8"

    hardware_choice = input("请选择处理模式：\n1 .GPU (3G 以上显存推荐)\n2 .CPU\n> ")
    if hardware_choice not in ["1", "2"]:
        print("\n输入错误，请重新输入")
        main()

    choice = input("请选择混音模式：\n1. 2 TO 5.1\n2. 2 TO 7.1\n> ")
    if choice not in ["1", "2"]:
        print("\n输入错误，请重新输入")
        main()

    # 创建Tk实例并隐藏主窗口
    root = Tk()
    root.withdraw()

    print("请选择需要转换的音频文件所在目录")
    input_directory = filedialog.askdirectory(
        title="选择音频文件所在目录", initialdir=".")
    print("请选择输出目录")
    output_directory = filedialog.askdirectory(title="选择输出目录", initialdir=".")

    for filename in os.listdir(input_directory):
        real_output_directory = os.path.join(
            output_directory, "htdemucs_ft", filename.split(".")[0])

        isfull = False

        print(f"正在处理文件: {filename}")
        for sound in ["vocals.wav", "bass.wav", "drums.wav", "other.wav"]:
            if os.path.isfile(os.path.join(real_output_directory, sound)):
                isfull = True
                print(f"{filename} 分离音频文件 {sound} 已存在，跳过分离")

        if not isfull:
            separate_audio(os.path.join(input_directory, filename),
                           output_directory, real_output_directory, hardware_choice)

        if choice == "1":
            output_file = os.path.join(
                output_directory, filename.split(".")[0] + "_5.1.flac")
            if not os.path.isfile(output_file):
                remix_channels(real_output_directory, output_file, 5)
            else:
                print(f"\n5.1混音已存在，请查看输出文件 {output_file}")
                continue
            finally_del(output_file, output_directory, 5)
        elif choice == "2":
            output_file = os.path.join(
                output_directory, filename.split(".")[0] + "_7.1.flac")
            if not os.path.isfile(output_file):
                remix_channels(real_output_directory, output_file, 7)
            else:
                print(f"\n7.1混音已存在，请查看输出文件 {output_file}")
                continue
            finally_del(output_file, output_directory, 7)

        gc.collect()


if __name__ == '__main__':
    main()

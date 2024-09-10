from PIL import Image, GifImagePlugin


def process_gif(input_path, output_path):
    # 打开GIF动图
    with Image.open(input_path) as img:
        # 确保文件是一个GIF
        if img.format != "GIF":
            raise ValueError("输入文件不是GIF格式")

            # 将GIF的每一帧提取出来并处理
        frames = []
        durations = []

        for frame_number in range(img.n_frames):
            # 将文件指针移动到该帧
            img.seek(frame_number)

            # 复制当前帧
            frame = img.copy()

            # 将黑色替换成透明色块
            # 假设黑色是 (0, 0, 0)
            datas = frame.getdata()
            print(datas)
            new_data = []
            for item in datas:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    # 将黑色替换为透明（保持alpha通道为0表示透明）
                    new_data.append((255, 255, 255, 0))
                else:
                    # 保持原样（添加alpha通道255表示不透明）
                    new_data.append((item[0], item[1], item[2], 255))

                    # 更新帧数据
            frame.putdata(new_data)

            # 保存帧和它的持续时间
            frames.append(frame)
            # 获取每一帧的持续时间（以毫秒为单位）
            durations.append(img.info['duration'] if 'duration' in img.info else 100)  # 默认100ms

        # 保存处理后的GIF
        # 第一个帧，其余的帧追加在后面，durations用来设置每帧的持续时间
        output_gif = frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=durations, loop=0)

    # 使用示例


input_gif_path = "input.gif"
output_gif_path = "output.gif"
process_gif(input_gif_path, output_gif_path)
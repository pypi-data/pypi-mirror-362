from nailfold_image_enhance import enhance_video


def progress_callback(percent):
    print(f"处理进度：{percent}%", end="\r")


# 增强视频并显示实时进度
enhance_video(
    input_path=r"D:\Users\16672\Desktop\jsdj\src\PJZB\videos\compare_lab\group1\proposal.mp4",
    output_path=r"D:\Users\16672\Desktop\jsdj\src\PJZB\videos\compare_lab\group1\enhanced_video.mp4",
    progress_callback=progress_callback
)

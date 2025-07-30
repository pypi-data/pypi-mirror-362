from nailfold_image_enhance import enhance_images_in_folder


def progress_callback(current: int, total: int):
    """
    正确的进度回调函数：仅接受current和total两个参数
    """
    # 计算进度百分比（当前/总数*100）
    progress_percent = (current / total) * 100 if total > 0 else 0
    print(f"Processing {current + 1}/{total} images: {progress_percent:.1f}% complete", end="\r", flush=True)


# 批量处理整个文件夹
enhance_images_in_folder(
    input_path=r"F:\甲襞小组\周斌\数据集\2024.8.28",
    output_path=r"F:\甲襞小组\周斌\数据集\enhance",
    suffix="_enhanced",
    progress_callback=progress_callback  # 此时参数匹配，黄线消失
)
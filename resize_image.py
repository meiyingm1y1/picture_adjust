#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片大小调整工具 - 命令行模块

功能：
- 单张图片调整大小
- 批量调整目录中所有图片
- 支持保持宽高比
- 支持多种图片格式

作者：魅影m1y1
"""

import os
import sys
from pathlib import Path
from PIL import Image

# 支持的图片格式
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
# 默认输出质量
DEFAULT_QUALITY = 95
# 默认重采样滤波器
DEFAULT_RESAMPLE_FILTER = Image.Resampling.LANCZOS


def resize_image(input_path, output_path, width, height, maintain_aspect=False, quality=DEFAULT_QUALITY):
    """
    调整图片大小并保存到指定路径。

    参数：
        input_path (str): 输入图片的路径。
        output_path (str): 输出图片的路径。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
        maintain_aspect (bool): 是否保持宽高比。
        quality (int): 输出图片质量 (1-100)，仅对 JPEG 有效。
    
    返回：
        bool: 成功返回 True，失败返回 False。
    """
    try:
        # 验证输入文件
        if not os.path.exists(input_path):
            print(f"错误：输入文件不存在 - {input_path}")
            return False
        
        # 打开图片
        with Image.open(input_path) as img:
            original_size = img.size
            original_mode = img.mode
            print(f"原始图片: {original_size[0]}x{original_size[1]}, 模式: {original_mode}")
            
            # 处理特殊图片类型
            if img.mode in ('P', 'PA'):
                img = img.convert('RGBA')
            elif img.mode == 'CMYK':
                img = img.convert('RGB')
            
            # 调整大小
            if maintain_aspect:
                # 保持宽高比，自适应调整
                img.thumbnail((width, height), DEFAULT_RESAMPLE_FILTER)
                print(f"保持宽高比调整: {img.size[0]}x{img.size[1]}")
            else:
                # 强制调整到指定尺寸
                img = img.resize((width, height), DEFAULT_RESAMPLE_FILTER)
                print(f"强制调整: {width}x{height}")
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 准备保存参数
            save_kwargs = {}
            output_ext = os.path.splitext(output_path)[1].lower()
            
            if output_ext in ('.jpg', '.jpeg'):
                # JPEG 不支持透明度，转换为 RGB
                if img.mode in ('RGBA', 'LA', 'PA', 'IA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                save_kwargs['quality'] = quality
                save_kwargs['format'] = 'JPEG'
            elif output_ext == '.png':
                save_kwargs['format'] = 'PNG'
            elif output_ext == '.webp':
                save_kwargs['quality'] = quality
                save_kwargs['format'] = 'WEBP'
            
            # 保存图片
            img.save(output_path, **save_kwargs)
            print(f"图片已成功调整大小并保存到 {output_path}")
            return True
            
    except ValueError as e:
        print(f"数值错误: {e}")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False


def batch_resize_images(input_dir, output_dir, width, height, maintain_aspect=False, quality=DEFAULT_QUALITY):
    """
    批量调整目录中的所有图片大小。

    参数：
        input_dir (str): 输入图片所在目录。
        output_dir (str): 输出图片保存目录。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
        maintain_aspect (bool): 是否保持宽高比。
        quality (int): 输出图片质量 (1-100)。
    
    返回：
        tuple: (成功数量, 失败数量)
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    skipped_count = 0
    
    print(f"\n开始批量处理...")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"目标尺寸: {width}x{height}")
    print("-" * 40)
    
    try:
        # 遍历输入目录中的所有文件
        for filename in sorted(os.listdir(input_dir)):
            input_path = os.path.join(input_dir, filename)
            
            # 检查是否为图片文件
            if os.path.isfile(input_path) and Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS:
                output_path = os.path.join(output_dir, filename)
                if resize_image(input_path, output_path, width, height, maintain_aspect, quality):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                skipped_count += 1
        
        print("-" * 40)
        print(f"处理完成: 成功 {success_count}, 失败 {fail_count}, 跳过 {skipped_count}")
        return success_count, fail_count
        
    except Exception as e:
        print(f"批量调整图片时发生错误: {e}")
        return success_count, fail_count + 1


def get_image_info(image_path):
    """
    获取图片信息。
    
    参数：
        image_path (str): 图片路径。
    
    返回：
        dict: 图片信息字典。
    """
    try:
        with Image.open(image_path) as img:
            file_size = os.path.getsize(image_path)
            return {
                'path': image_path,
                'width': img.size[0],
                'height': img.size[1],
                'mode': img.mode,
                'format': img.format,
                'file_size': file_size
            }
    except Exception as e:
        return {'path': image_path, 'error': str(e)}


def format_file_size(bytes_size):
    """格式化文件大小显示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


if __name__ == "__main__":
    print("=" * 50)
    print("       图片大小调整工具")
    print("=" * 50)
    print()
    
    # 选择模式
    print("请选择模式:")
    print("1. 单张图片调整")
    print("2. 批量调整")
    print("3. 查看图片信息")
    
    mode = input("请输入模式 (1/2/3): ").strip()
    
    if mode == '1':
        # 单张图片模式
        input_path = input("请输入输入图片路径: ").strip().strip('"\'')
        output_path = input("请输入输出图片路径 (留空则自动生成): ").strip().strip('"\'')
        
        if not output_path:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_resized{ext}"
        
        try:
            width = int(input("请输入调整后的宽度: "))
            height = int(input("请输入调整后的高度: "))
        except ValueError:
            print("错误：请输入有效的整数")
            sys.exit(1)
        
        maintain_aspect = input("是否保持宽高比? (y/n): ").strip().lower() == 'y'
        quality_input = input("JPEG质量 (1-100, 默认95): ").strip()
        quality = int(quality_input) if quality_input.isdigit() else DEFAULT_QUALITY
        
        resize_image(input_path, output_path, width, height, maintain_aspect, quality)
        
    elif mode == '2':
        # 批量处理模式
        input_dir = input("请输入输入图片所在目录: ").strip().strip('"\'')
        output_dir = input("请输入输出图片保存目录: ").strip().strip('"\'')
        
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(input_dir), "resized_output")
        
        try:
            width = int(input("请输入调整后的宽度: "))
            height = int(input("请输入调整后的高度: "))
        except ValueError:
            print("错误：请输入有效的整数")
            sys.exit(1)
        
        maintain_aspect = input("是否保持宽高比? (y/n): ").strip().lower() == 'y'
        quality_input = input("JPEG质量 (1-100, 默认95): ").strip()
        quality = int(quality_input) if quality_input.isdigit() else DEFAULT_QUALITY
        
        batch_resize_images(input_dir, output_dir, width, height, maintain_aspect, quality)
        
    elif mode == '3':
        # 查看图片信息
        image_path = input("请输入图片路径: ").strip().strip('"\'')
        info = get_image_info(image_path)
        
        if 'error' in info:
            print(f"错误: {info['error']}")
        else:
            print(f"\n图片信息:")
            print(f"  路径:   {info['path']}")
            print(f"  尺寸:   {info['width']}x{info['height']}")
            print(f"  模式:   {info['mode']}")
            print(f"  格式:   {info['format']}")
            print(f"  大小:   {format_file_size(info['file_size'])}")
            
    else:
        print("无效的模式选择")
        sys.exit(1)
    
    print("\n" + "=" * 50)

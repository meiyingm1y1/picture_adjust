import os
from PIL import Image

def resize_image(input_path, output_path, width, height):
    """
    调整图片大小并保存到指定路径。

    参数：
        input_path (str): 输入图片的路径。
        output_path (str): 输出图片的路径。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 调整大小
            resized_img = img.resize((width, height))
            # 保存图片
            resized_img.save(output_path)
            print(f"图片已成功调整大小并保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def batch_resize_images(input_dir, output_dir, width, height):
    """
    批量调整目录中的所有图片大小。

    参数：
        input_dir (str): 输入图片所在目录。
        output_dir (str): 输出图片保存目录。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
    """
    try:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 遍历输入目录中的所有文件
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # 检查是否为图片文件
            if os.path.isfile(input_path) and filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                resize_image(input_path, output_path, width, height)
    except Exception as e:
        print(f"批量调整图片时发生错误: {e}")

if __name__ == "__main__":
    # 示例用法
    input_dir = input("请输入输入图片所在目录: ")
    output_dir = input("请输入输出图片保存目录: ")
    width = int(input("请输入调整后的宽度: "))
    height = int(input("请输入调整后的高度: "))

    batch_resize_images(input_dir, output_dir, width, height)
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def resize_image(input_path, output_path, width, height):
    """
    调整图片大小并保存到指定路径。

    参数：
        input_path (str): 输入图片的路径。
        output_path (str): 输出图片的路径。
        width (int): 调整后的宽度。
        height (int): 调整后的高度。
    """
    with Image.open(input_path) as img:
        resized_img = img.resize((width, height))
        resized_img.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取表单数据
        width = int(request.form['width'])
        height = int(request.form['height'])
        file = request.files['file']

        if file:
            # 保存上传的文件
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            # 调整图片大小
            output_path = os.path.join(OUTPUT_FOLDER, file.filename)
            resize_image(input_path, output_path, width, height)

            return redirect(url_for('download', filename=file.filename))

    return render_template('index.html')

@app.route('/outputs/<filename>')
def serve_file(filename):
    """
    提供输出目录中的文件下载。
    """
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

@app.route('/download/<filename>')
def download(filename):
    return f'<h1>图片已调整大小</h1><a href="/outputs/{filename}" download>点击这里下载图片</a>'

if __name__ == '__main__':
    app.run(debug=True)
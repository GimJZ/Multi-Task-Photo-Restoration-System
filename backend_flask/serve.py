import resnet50
import io
import torch
import cv2
import numpy as np
import os

from io import BytesIO
from Restormer import restormer
from flask import Flask, request
from PIL import Image
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

# flask框架
app = Flask(__name__, template_folder='./templates')
CORS(app, support_credentials=True)  # 解决跨域问题

#判断类型
@app.route("/predict", methods=["POST"])
@cross_origin(support_credentials=True)
@torch.no_grad()
def predict():
    image = request.files["file"]
    img_bytes = image.read()
    # 将字节流转换为 Pillow 中的 Image 对象
    img = Image.open(io.BytesIO(img_bytes))
    lable = resnet50.get_prediction(img)
    return lable

#自定义处理
@app.route("/process", methods=["POST"])
@cross_origin(support_credentials=True)
@torch.no_grad()
def process():
    choose = request.args.get('data')
    image = request.files["file"]
    img_bytes = image.read()
    # 将字节流转换为 Pillow 中的 Image 对象
    img = Image.open(io.BytesIO(img_bytes))
    # 压缩图像的分辨率
    w, h = img.size
    scale_percent = 30     # 定义缩放比例
    new_h = int(h * scale_percent / 100)  # 计算缩放后的高
    new_w = int(w * scale_percent / 100)  # 计算缩放后的宽
    dim = (new_w, new_h)    # 将宽高组成元组
    np_image = np.array(img)
    resized_img = cv2.resize(np_image, dim, interpolation=cv2.INTER_AREA)
    # 获取处理类型
    task = restormer.get_type(choose)
    # 图像处理
    restore = restormer.process(task, resized_img)
    output_img = cv2.cvtColor(restore, cv2.COLOR_RGB2BGR)
    # 将`output_img`转换为`PIL.Image`
    output_img = Image.fromarray(output_img)
    # 将图片保存到本地
    save_path = os.path.join('processed_image', 'saved.jpeg')
    output_img.save(save_path)
    # 将保存的图片转换成数据流的格式传出
    img = Image.open(save_path)
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

#一键处理
@app.route("/auto_process", methods=["POST"])
@cross_origin(support_credentials=True)
@torch.no_grad()
def auto_process():
    image = request.files["file"]
    img_bytes = image.read()
    # 将字节流转换为 Pillow 中的 Image 对象
    img = Image.open(io.BytesIO(img_bytes))
    # 先用resnet50获取图片类型choose
    choose = resnet50.get_prediction(img)

    # 压缩图像的分辨率
    w, h = img.size
    scale_percent = 30     # 定义缩放比例
    new_h = int(h * scale_percent / 100)  # 计算缩放后的高
    new_w = int(w * scale_percent / 100)  # 计算缩放后的宽
    dim = (new_w, new_h)    # 将宽高组成元组
    np_image = np.array(img)
    resized_img = cv2.resize(np_image, dim, interpolation=cv2.INTER_AREA)
    # 获取处理类型
    task = restormer.get_type(choose)
    # 图像处理
    restore = restormer.process(task, resized_img)
    output_img = cv2.cvtColor(restore, cv2.COLOR_RGB2BGR)
    # 将`output_img`转换为`PIL.Image`
    output_img = Image.fromarray(output_img)
    # 将图片保存到本地
    save_path = os.path.join('processed_image', 'saved.jpeg')
    output_img.save(save_path)
    # 将保存的图片转换成数据流的格式传出
    img = Image.open(save_path)
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

# 设置路由
@app.route('/', methods=['GET', "POST"])
def root():
    return ('hello jz')

# 启动app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
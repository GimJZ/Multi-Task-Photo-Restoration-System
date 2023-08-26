import os
import json
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np

weights_path = "./checkpoint/model.pth"
class_json_path = "./class_indices.json"
idx_to_labels = np.load('./idx_to_labels.npy', allow_pickle=True).item()
assert os.path.exists(weights_path), "weights path does not exist..."
assert os.path.exists(class_json_path), "class json path does not exist..."

# select device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# load class info
json_file = open(class_json_path, 'rb')
class_indict = json.load(json_file)

idx_to_labels = np.load('./idx_to_labels.npy', allow_pickle=True).item()


# # **ResNet-50目标检测结果**

model = torch.load('./checkpoint/model.pth')
model = model.eval().to(device)


# 图像预处理函数
from torchvision import transforms
# 测试集图像预处理-RCTN：缩放、裁剪、转 Tensor、归一化
transform_image = transforms.Compose([transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], 
                    std=[0.229, 0.224, 0.225])
                    ])


# 图像预测函数

def get_prediction(image_bytes):
    try:
        input_img = transform_image(image_bytes)
        input_img = input_img.unsqueeze(0).to(device)
        # 执行前向预测，得到所有类别的 logit 预测分数
        pred_logits = model(input_img) 
        # 对 logit 分数做 softmax 运算
        pred_softmax = F.softmax(pred_logits, dim=1)
        # 找最大值及其所在的索引
        max_value, max_idx = torch.max(pred_softmax, dim=1)  
        value_list = list(idx_to_labels.values())

        return_info = value_list[max_idx]
    except Exception as e:
        return_info = {"result": [str(e)]}
    return return_info
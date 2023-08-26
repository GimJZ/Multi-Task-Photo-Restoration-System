import os
import torch
import torch.nn.functional as F
import numpy as np
import cv2

from PIL import Image
from runpy import run_path
from skimage import img_as_ubyte



def get_type(choose):
    if choose == 'Real_Denoising':
        task = 'Real_Denoising'
    if choose == 'defoucs_blur':
        task = 'Single_Image_Defocus_Deblurring'
    if choose == 'motion_blur':
        task = 'Motion_Deblurring'
    if choose == 'rain':
        task = 'Deraining'
    return task


def get_weights_and_parameters(task, parameters):
    if task == 'Motion_Deblurring':
        weights = os.path.join('models', 'motion_deblurring.pth')
    elif task == 'Single_Image_Defocus_Deblurring':
        weights = os.path.join('models', 'single_image_defocus_deblurring.pth')
    elif task == 'Deraining':
        weights = os.path.join('models', 'deraining.pth')
    elif task == 'Real_Denoising':
        weights = os.path.join('models', 'real_denoising.pth')
        parameters['LayerNorm_type'] =  'BiasFree'
    return weights, parameters


# Get model weights and parameters
def process(task, image_bytes):
    parameters = {'inp_channels':3, 'out_channels':3, 'dim':48, 'num_blocks':[4,6,6,8], 'num_refinement_blocks':4, 'heads':[1,2,4,8], 'ffn_expansion_factor':2.66, 'bias':False, 'LayerNorm_type':'WithBias', 'dual_pixel_task':False}
    weights, parameters = get_weights_and_parameters(task, parameters)

    load_arch = run_path(os.path.join('Restormer','basicsr', 'models', 'archs', 'restormer_arch.py'))
    model = load_arch['Restormer'](**parameters)
    model.cuda()

    checkpoint = torch.load(weights)
    model.load_state_dict(checkpoint['params'])
    model.eval()

    img_multiple_of = 8

    with torch.no_grad():
        torch.cuda.ipc_collect()
        torch.cuda.empty_cache()
        np_image = np.array(image_bytes)
        img = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
        input_ = torch.from_numpy(img).float().div(255.).permute(2,0,1).unsqueeze(0).cuda()

        # Pad the input if not_multiple_of 8
        h,w = input_.shape[2], input_.shape[3]
        H,W = ((h+img_multiple_of)//img_multiple_of)*img_multiple_of, ((w+img_multiple_of)//img_multiple_of)*img_multiple_of
        padh = H-h if h%img_multiple_of!=0 else 0
        padw = W-w if w%img_multiple_of!=0 else 0
        input_ = F.pad(input_, (0,padw,0,padh), 'reflect')

        restored = model(input_)
        restored = torch.clamp(restored, 0, 1)

        # Unpad the output
        restored = restored[:,:,:h,:w]

        restored = restored.permute(0, 2, 3, 1).cpu().detach().numpy()
        restored = img_as_ubyte(restored[0])
        # cv2.imwrite(os.path.join(out_dir, filename),cv2.cvtColor(restored, cv2.COLOR_RGB2BGR))

        print("task is: ", task)
        return restored
import base64
import contextlib
import time

import numpy as np
import torch
from safetensors import safe_open
import matplotlib.pyplot as plt
from torchvision.transforms import functional as F


def tensor_to_heatmap(tensor, save_path, target_size=(8192, 8192), cmap_name='custom_div_cmap'):
    """
    将1D或2D的tensor或numpy数组可视化为热力图，并保存为图像文件。
    所有输入都会被缩放到指定的目标尺寸 (默认: 8192x8192)

    参数:
        tensor (torch.Tensor or np.ndarray): 输入的1D或2D张量/数组
        save_path (str): 图像保存路径（如 'heatmap.png'）
        target_size (tuple): 目标图像尺寸 (height, width)
        cmap_name (str): 自定义颜色映射名称

    返回:
        None: 图像将被保存到指定路径
    """
    # 转换为numpy数组
    if isinstance(tensor, torch.Tensor):
        if tensor.dtype in (torch.bfloat16, torch.float16):
            tensor = tensor.float()
        tensor = tensor.detach().cpu().numpy()

    assert len(tensor.shape) in (1, 2), "输入必须是1D或2D张量"

    # 如果是1D张量，转为2D图像形式
    if len(tensor.shape) == 1:
        length = tensor.shape[0]
        size = int(np.ceil(np.sqrt(length)))
        new_shape = (size, size)
        padded = np.zeros(new_shape, dtype=tensor.dtype)
        padded.flat[:length] = tensor
        tensor = padded

    # 转换为PyTorch tensor以使用 interpolate 函数
    tensor = torch.from_numpy(tensor).unsqueeze(0).unsqueeze(0)  # [1, 1, H, W]

    # 插值缩放到目标大小
    resized_tensor = F.resize(tensor, size=target_size, interpolation=F.InterpolationMode.BILINEAR)

    # 去掉多余的维度，回到2D数组
    resized_array = resized_tensor.squeeze().numpy()

    # 创建自定义颜色映射（红-白-蓝）
    def _make_cmap():
        colors = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]  # 红 -> 白 -> 蓝
        return plt.matplotlib.colors.LinearSegmentedColormap.from_list(cmap_name, colors)

    cmap = _make_cmap()

    # 设置图像大小：每个像素对应一个数据点（dpi=1）
    height, width = resized_array.shape

    fig, ax = plt.subplots(figsize=(width, height), dpi=1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # 去除空白边距
    ax.imshow(resized_array, cmap=cmap, interpolation='none', aspect='auto')  # 不插值，自动宽高比
    ax.axis('off')  # 关闭坐标轴

    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=1)
    plt.close(fig)


class Safetensors:
    def __init__(self):
        ...

    def load(self, path: str, device='cpu'):
        """
        Load a safetensors file from the given path.
        :param path: Path to the safetensors file.
        :return: Loaded data.
        """
        name = base64.b64encode(path.encode()).decode().replace('/', '_').replace('\\', '_')
        output_list = []
        with safe_open(path, framework="pt", device=device) as f:
            for k in f.keys():
                print(f"Loading tensor: {k}, shape: {f.get_tensor(k).shape}, dtype: {f.get_tensor(k).dtype}")
                output_list.append(f"{k}.png")
                tensor_to_heatmap(f.get_tensor(k), cmap_name='custom_div_cmap', save_path=output_list[-1])


if __name__ == '__main__':
    ST = Safetensors()
    print(ST.load(r"Z:\WH\backup\hive-0-0706-15000-sft\model-00001-of-00014.safetensors"))

from magicgui import magic_factory
from napari.layers import Image, Labels
from cellpose import models

@magic_factory(
    call_button="Run Cellpose",
    model_type={"choices": ["cyto3", "cyto2", "cyto", "nuclei"]},
    channel_first={"choices": [0, 1, 2]},
    channel_second={"choices": [0, 1, 2]}
)
def run_cellpose(image: Image, model_type: str = "cyto3", diameter: float = 30.0,
               channel_first: int = 0, channel_second: int = 0) -> Labels:
    """
    使用 Cellpose 模型对图像进行细胞分割。

    参数：
        image: 输入的图像层。
        model_type: 模型类型，可以是 "cyto" 或 "nuclei"。
        diameter: 细胞直径的估计值。
        channel_first: 第一个通道的索引（0-2）。
        channel_second: 第二个通道的索引（0-2）。

    返回：
        分割后的标签层。
    """
    # 加载 Cellpose 模型
    model = models.Cellpose(gpu=True, model_type=model_type)
    
    # 运行 Cellpose 模型进行分割
    masks, _, _, _ = model.eval(image.data, diameter=diameter, channels=[channel_first, channel_second])
    
    # 返回分割结果作为 Napari 的标签层
    return Labels(masks, name=f"Cellpose {model_type} Segmentation")
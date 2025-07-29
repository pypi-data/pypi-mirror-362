from magicgui import magic_factory
from napari.utils.notifications import show_info
from napari.layers import Labels, Layer
import numpy as np
import pandas as pd
import pathlib

@magic_factory(call_button="SAVE")
def save_selected_labels(layers: list[Layer], filename=pathlib.Path.cwd()):
    """
    Save all visible Labels layers into a single CSV file.
    Args:
        layers: List of visible layers in the viewer.
        filename: Path to save the CSV file.
    """
    combined_data = pd.DataFrame(data=[], columns=pd.Index(["x", "y"]))

    for layer in layers:
        # Check if it is a Labels layer
        if isinstance(layer, Labels):
            # Get the corresponding layer name
            layer_name = layer.name.replace(' ', '_')
            # Get non-zero coordinates
            coords = np.column_stack(np.where(layer.data != 0))
            coords_list = list(zip(coords[:, 0], coords[:, 1]))
            # Get the corresponding values
            values = np.array([layer.data[x, y] for x, y in coords_list])
            layer_df = pd.DataFrame(coords, columns=pd.Index(["x", "y"]))
            # Add a column for layer values
            layer_df[layer_name] = values
            combined_data = pd.merge(combined_data, layer_df, on=["x", "y"], how="outer")  # 合并数据
    combined_data.fillna(0, inplace=True)

    filename = str(filename) + "/labels_data.csv"
    combined_data.to_csv(filename, index=False)
    show_info("Save Successful")
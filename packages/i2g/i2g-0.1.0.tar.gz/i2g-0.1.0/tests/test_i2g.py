import numpy as np
import networkx as nx
from PIL import Image
from i2g import ImageGraphConverter


def test_image_graph_creation(tmp_path):
    # Create a simple 3x3 grayscale image array and save as PNG
    img_array = np.array(
        [
            [100, 150, 200],
            [50, 100, 150],
            [0, 50, 100],
        ],
        dtype=np.uint8,
    )

    img_path = tmp_path / "test_image.png"

    # Save image
    img = Image.fromarray(img_array)
    img.save(img_path)

    # Run converter
    converter = ImageGraphConverter(str(img_path), connectivity="4")
    G, img_loaded = converter.convert()

    # Check graph created
    assert G is not None
    assert isinstance(G, nx.Graph)
    assert img_loaded.shape == (3, 3)

    # Check nodes and edges
    num_nodes, num_edges = converter.info()
    assert num_nodes == 9  # 3x3 pixels
    assert num_edges > 0

    # Check shape method
    shape = converter.shape()
    assert shape == (3, 3)

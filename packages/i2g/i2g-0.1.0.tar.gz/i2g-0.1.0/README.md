
# 🖼️ i2g — Image to Graph Converter

[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI - Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Convert grayscale images into graph structures using NetworkX.  
Each pixel becomes a node, connected to its neighbors (4- or 8-connectivity), with pixel intensity stored as a feature.

---

## 🚀 Features

- ✅ Convert any grayscale image into a `networkx` graph.
- ✅ Choose 4- or 8-neighborhood connectivity.
- ✅ Each node stores:
  - `intensity`: pixel grayscale value (0-255)
  - `pos`: (x, y) coordinate for plotting.
- ✅ Easily query the graph’s shape, number of nodes, and edges.

---

## 🛠️ Installation

Clone this repository and install in editable mode:

```bash
git clone https://github.com/DIM-Corp/i2g.git
cd i2g
pip install -e .
```

Requires: `numpy`, `pillow`, `networkx`.

---

## ✍️ Example usage

```python
from i2g import ImageGraphConverter

# Create a converter for your image
converter = ImageGraphConverter("my_image.png", connectivity='8')

# Convert the image to a graph
graph, img_array = converter.convert()

# Query information
shape = converter.shape()  # returns (height, width)
num_nodes, num_edges = converter.info()

print(f"Image shape: {shape}")
print(f"Graph has {num_nodes} nodes and {num_edges} edges.")
```

---

## 🚀 Running tests

This project uses [pytest](https://pytest.org).

Run the tests with:

```bash
pytest
```

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## 💪 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you’d like to change.

---

## ⭐ Acknowledgements

- Built on top of amazing libraries: [NetworkX](https://networkx.org/), [Pillow](https://python-pillow.org/), [NumPy](https://numpy.org/)


## ⭐ Contacts 
info@dimcorp237.com
mdieffi@gmail.com
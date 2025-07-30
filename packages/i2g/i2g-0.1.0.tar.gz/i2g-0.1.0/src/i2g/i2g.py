# i2g.py
from PIL import Image
import networkx as nx
import numpy as np


class ImageGraphConverter:
    def __init__(self, image_path, connectivity="8"):
        """
        Initializes the ImageGraphConverter.

        Args:
            image_path (str): Path to the grayscale image.
            connectivity (str): '4' or '8' for 8-connectivity.
        """
        self.image_path = image_path
        self.connectivity = connectivity
        self.img_array = None
        self.graph = None

    def convert(self):
        """
        Converts the image into a graph structure.

        After running, self.graph and self.img_array will be populated.

        Returns:
            tuple: (networkx.Graph, numpy.ndarray)
        """
        try:
            img = Image.open(self.image_path).convert("L")
        except FileNotFoundError:
            print(f"Error: Image not found at {self.image_path}")
            return None, None
        except Exception as e:
            print(f"Error loading or processing image: {e}")
            return None, None

        self.img_array = np.array(img)
        height, width = self.img_array.shape

        G = nx.Graph()

        # Add nodes with intensity and position
        print(f"Creating nodes for image of size {width}x{height}...")
        for r in range(height):
            for c in range(width):
                pixel_id = (r, c)
                intensity = self.img_array[r, c]
                G.add_node(pixel_id, intensity=intensity, pos=(c, -r))

        # Define neighbor offsets
        if self.connectivity == "4":
            neighbors_offsets = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
            ]
        elif self.connectivity == "8":
            neighbors_offsets = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
        else:
            raise ValueError("Connectivity must be '4' or '8'.")

        # Add edges
        print(f"Adding edges with {self.connectivity}-connectivity...")
        for r in range(height):
            for c in range(width):
                for dr, dc in neighbors_offsets:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width:
                        G.add_edge((r, c), (nr, nc))

        self.graph = G
        return self.graph, self.img_array

    def shape(self):
        """
        Returns the shape of the image / graph grid as (height, width).

        Returns:
            tuple: (height, width)
        """
        if self.img_array is not None:
            return self.img_array.shape
        print("Error: No image loaded yet.")
        print("Call convert() first.")
        return None

    def info(self):
        """
        Returns the number of nodes and edges in the graph.

        Returns:
            tuple: (num_nodes, num_edges)
        """
        if self.graph is not None:
            return self.graph.number_of_nodes(), self.graph.number_of_edges()
        print("Error: Graph not created yet.")
        print("Call convert() first.")
        return None

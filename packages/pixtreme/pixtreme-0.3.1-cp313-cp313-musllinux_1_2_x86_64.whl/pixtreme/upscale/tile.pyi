from __future__ import annotations
import builtins as __builtins__
import cupy as cp
from pixtreme.utils.dtypes import to_float32
__all__ = ['add_padding', 'cp', 'create_gaussian_weights', 'merge_tiles', 'tile_image', 'to_float32']
def add_padding(input_image: cp.ndarray, patch_size: int = 128, overlap: int = 16) -> cp.ndarray:
    ...
def create_gaussian_weights(size: int, sigma: int) -> cp.ndarray:
    """
    
        Create a Gaussian weight map for tile blending.
    
        Parameters
        ----------
        size : int
            Size of the weight map.
        sigma : int
            Standard deviation for the Gaussian distribution.
    
        Returns
        -------
        cp.ndarray
            Gaussian weight map in the shape (size, size, 1).
        
    """
def merge_tiles(tiles: list[cp.ndarray], original_shape: tuple[int, int, int], padded_shape: tuple[int, int, int], scale: int, tile_size: int = 128, overlap: int = 16) -> cp.ndarray:
    ...
def tile_image(input_image: cp.ndarray, tile_size: int = 128, overlap: int = 16) -> tuple[list[cp.ndarray], tuple]:
    """
    
        Split the input image into overlapping tiles.
    
        Parameters
        ----------
        input_image : cp.ndarray
            Input image in the shape (height, width, channel) in RGB format.
        tile_size : int, optional
            Size of each tile, by default 128.
        overlap : int, optional
            Overlap between tiles, by default 16.
    
        Returns
        -------
        list[cp.ndarray]
            List of image tiles, each in the shape (tile_size, tile_size, channel) in RGB format.
        
    """
__test__: dict = {}

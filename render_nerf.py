from typing import Callable

import numpy as np


def render_nerf_pixel(
    direction: np.ndarray,
    start_point: np.ndarray,
    dist: float,
    model: Callable,
    depth_discretization,
) -> np.ndarray:
    """
    Use the rendering equation to calculate the color of a single pixel.
    Args:
        direction: The direction of the pixel.
        start_point: The start point of the ray.
        dist: The distance of the pixel.
        model: The model to use for rendering.
        depth_discretization: Number of points to integrate above
    Returns:
        The color of the pixel.
    """
    unit_direction = direction / np.linalg.norm(direction)
    dx_dist = dist / depth_discretization
    dx_vec = unit_direction * (dx_dist)
    x = np.array([start_point + i * dx_vec for i in range(depth_discretization)])
    sigmas = np.zeros(x.shape[0])
    colors = np.zeros((x.shape[0], 3))
    for i, x_i in enumerate(x):
        sigma, color = model(x_i, unit_direction)
        sigmas[i] = sigma
        colors[i, :] = color
    # normalize sigmas
    # sigmas = sigmas / np.sum(sigmas) if np.sum(sigmas) > 0 else sigmas
    transmittance = np.exp(-np.cumsum(sigmas * dx_dist))
    # print(transmittance.shape)
    # print(sigmas.shape)
    final_color = np.sum(
        colors.T * transmittance * (1 - np.exp(-sigmas * dx_dist)), axis=1
    )  # 3d vec for color
    return final_color

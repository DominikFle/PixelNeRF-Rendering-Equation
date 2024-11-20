import math
import numpy as np


def compute_ray_map(W, H, fx, fy, cx, cy):
    #     +x: Points to the right in the image plane.
    # +y+y: Points downward in the image plane.
    # +z+z: Points forward, out of the camera (into the scene).
    # Create pixel grid
    u, v = np.meshgrid(np.arange(W), np.arange(H))

    # Normalize pixel coordinates
    x = (u - cx) / fx
    y = (v - cy) / fy

    # Create ray directions
    rays = np.stack([x, y, np.ones_like(x)], axis=-1)

    # Normalize rays to unit vectors
    norm = np.linalg.norm(rays, axis=-1, keepdims=True)
    rays_normalized = rays / norm

    return rays_normalized


def rotate_ray_map_by_center_ray(ray_map, target_ray):
    """
    Rotate the ray map such that the target_ray is at the center.
    Args:
        ray_map: The ray map to rotate.
        target_ray: The ray to move to the center.
    Returns:
        The rotated ray map.
    """
    target_ray /= np.linalg.norm(target_ray)
    H, W = ray_map.shape[:2]
    center_ray = ray_map[H // 2, W // 2]

    angle_between_center_and_target = np.arccos(np.dot(center_ray, target_ray))
    axis = np.cross(center_ray, target_ray)
    axis /= np.linalg.norm(axis)

    R = rotation_matrix(axis, angle_between_center_and_target)
    rotated_ray_map = np.tensordot(ray_map, R, axes=([2], [1]))
    return rotated_ray_map


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )

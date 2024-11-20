from matplotlib import pyplot as plt
import numpy as np
from get_view_directions import compute_ray_map, rotate_ray_map_by_center_ray
from render_nerf import render_nerf_pixel
from stub_model.CubeModel import CubeModel
from vis.vis_ray_map import vis_ray_map


cube_model = CubeModel(
    center=np.array([0.5, 0.5, 0.5]), side_length=1.0, light_pos=None
)
c = render_nerf_pixel(
    direction=np.array([-1, -1, -1]),
    start_point=np.array([1, 1, 1]),
    dist=2,
    model=cube_model,
    depth_discretization=10000,
)
# Example parameters (change as needed)
W, H = 100, 100  # Image width and height
fx, fy = 30, 30  # Focal lengths
cx, cy = W / 2, H / 2  # Principal point at the image center

ray_map = compute_ray_map(W, H, fx, fy, cx, cy)
ray_map = rotate_ray_map_by_center_ray(ray_map, target_ray=np.array([-1.0, -1.0, -1.0]))
# vis_ray_map(ray_map, path="ray_map.png")
img = np.zeros((H, W, 3))
for i in range(W):
    for j in range(H):
        c = render_nerf_pixel(
            direction=ray_map[i, j],
            start_point=np.array([1.5, 1.5, 1.5]),
            dist=2,
            model=cube_model,
            depth_discretization=100,
        )
        img[i, j] = c
plt.imshow(img)
plt.show()
plt.imsave("cube.png", img)

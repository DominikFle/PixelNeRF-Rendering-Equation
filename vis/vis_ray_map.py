from matplotlib import pyplot as plt
import numpy as np


def vis_ray_map(ray_map, path=""):
    H, W = ray_map.shape[:2]
    # Origins of the rays
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    Z = np.zeros_like(X)  # Start all rays at Z=0 (camera center)

    # Directions of the rays
    U = ray_map[..., 0]  # X-direction
    V = ray_map[..., 1]  # Y-direction
    W = ray_map[..., 2]  # Z-direction

    # Create 3D quiver plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Quiver plot
    ax.quiver(0, 0, 0, U, V, W, length=0.1, normalize=True)

    # Labels and view adjustments
    ax.set_title("3D Quiver Plot of Ray Map")
    ax.set_xlabel("Image X-axis")
    ax.set_ylabel("Image Y-axis")
    ax.set_zlabel("Camera Z-axis")
    ax.view_init(elev=20, azim=30)  # Adjust view angle
    plt.show()
    plt.savefig(path)

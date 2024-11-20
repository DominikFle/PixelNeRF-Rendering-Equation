import numpy as np


class CubeModel:
    def __init__(self, center: np.ndarray, side_length: float, light_pos=None):
        """
        coordiante system:
        x-y ground plane
        z is up
        """
        self.center = center
        self.side_length = side_length
        if not light_pos:
            light_pos = center + np.array([0, 0, side_length])
        self.light_pos = light_pos
        self.cube_color = np.array([0, 0, 0.5])

    def __call__(self, x: np.ndarray, unit_direction: np.ndarray) -> np.ndarray:

        light_ray = self.light_pos - self.center / np.linalg.norm(
            self.light_pos - self.center
        )
        # closest_normal = self.get_closest_normal(x)
        if x[2] > self.center[2] + self.side_length / 2 * 0.92:
            closest_normal = np.array([0, 0, 1])
            color_factor = np.max(np.dot(closest_normal, light_ray), 0)
        else:
            closest_normal = light_ray
            color_factor = 0.8
        if self.is_in_cube(x):
            sigma = 1
        else:
            sigma = 0
        color = self.cube_color * color_factor
        return sigma, color

    def is_in_cube(self, x):
        for i in range(len(x)):
            x_in = (
                x[i] < self.center[i] + self.side_length / 2
                and x[i] > self.center[i] - self.side_length / 2
            )
            if not x_in:
                return False
        return True

    def get_closest_normal(self, x):
        normal = np.zeros(3)
        closest_dist = 0
        sides = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
        for side in sides:
            dist = np.linalg.norm(self.center + np.array(side) * self.side_length - x)
            if dist < closest_dist:
                closest_dist = dist
                normal = np.array(side)
        return normal

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
        self.cube_color = np.array([0, 0, 1])

    def __call__(self, x: np.ndarray, unit_direction: np.ndarray) -> np.ndarray:
        # TODO change color depending on unit_dir
        if self.is_in_cube(x):
            sigma = 1
        else:
            sigma = 0
        return sigma, self.cube_color

    def is_in_cube(self, x):
        for i in range(len(x)):
            x_in = (
                x[i] < self.center[i] + self.side_length / 2
                and x[i] > self.center[i] - self.side_length / 2
            )
            if not x_in:
                return False
        return True

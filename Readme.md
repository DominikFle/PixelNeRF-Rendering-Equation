## PixelNeRF Rendering Equation vs. 3D Gaussian Splatting Rendering 
This project aims to visualize and understand the way of rendering a 3D Model using PixelNeRF Rendering Equation and 3D Gaussian Splatting Rendering. The project is divided into two parts:

1. PixelNerF Rendering Equation
2. 3D Gaussian Splatting Rendering

### PixelNeRF Rendering Equation

The rendering equation is used to predict the RGB color $\mathbf{c} \in [0,1]^{3}$ of a pixel in a camera view. The pixel position is described via the given 3D point of the camera $\mathbf{o}$ and the normalized viewing direction $\mathbf{d}$. 
A MLP $f_{\theta}$ represents the 3D scene and can be queried at any 3D point $\mathbf{x}$ to get the local RGB color $\mathbf{c}$ $c$ and the absorption density $\sigma$ of the scene at that point.

The rendering equation renders the color $\mathbf{C}_ {i}$ for every pixel with direction $\mathbf{d}_ {i}$ in the camera view. The rendering equation is given by:

$$\mathbf{C}_ {i} = \mathbf{C}(\mathbf{o},\mathbf{d}_ {i}) = \int_ {0}^{\infty} \sigma\left(\mathbf{x}(t),\mathbf{d}_ {i}\right)e^{-\int_ {0}^{t}\sigma(\mathbf{x}(\hat{t}),\mathbf{d}) d\hat{t}} \mathbf{c\left(\mathbf{x}(t),\mathbf{d}_ {i}\right)} dt$$

where $\mathbf{x}(t) = \mathbf{o} + t\mathbf{d}$ is the 3D point along the ray and $\sigma(\mathbf{x}(t),\mathbf{d}_ {i})$ is the density of the scene at that point. The term 
$e^{-\int_ {0}^{t}\sigma(\mathbf{x}(\hat{t}),\mathbf{d}) d\hat{t}} = T(t)$ is derived from the absorption equation 

$$\frac{dI(s)}{ds} = -\sigma(s) I(s)$$

 with $I(s)$ the light intensity. $T(t) \in [0,1]$ is the transmittance of the light from the camera to the 3D point $\mathbf{x}(t)$.
The rendering equation can be further simplified to the following form:

$$\mathbf{C}_ {i} = \mathbf{C}(\mathbf{o},\mathbf{d}_ {i}) = \int_ {0}^{\infty} T(t) \mathbf{c\left(\mathbf{x}(t),\mathbf{d}_ {i}\right)} dt$$

Assuming piecewise constant color the rendering equation can be further simplified to [[1]]((https://arxiv.org/abs/2310.20685)):
$$\mathbf{C}(\mathbf{o},\mathbf{d}) = \sum_ {j=1}^{N} \left( \int_ {t_ {j}}^{t_ {j+1}} T(u) \sigma(u) du \right)\mathbf{c}_ {j}$$
using the differentiation trick one can rewrite

$$ \int_ {t_ {j}}^{t_ {j+1}} T(u) \sigma(u) du =  \int_ {t_ {j}}^{t_ {j+1}} \sigma(u) e^{-\int_ {0}^{u}\sigma(\mathbf{x}({t}),\mathbf{d}) d{t}} du = \\ \int_ {t_ {j}}^{t_ {j+1}} - \frac{d}{du} e^{-\int_ {0}^{u}\sigma(\mathbf{x}({t}),\mathbf{d}) d{t}} du = \\ -e^{-\int_ {0}^{t_ {j+1}}\sigma(\mathbf{x}({t}),\mathbf{d}) d{t}} + e^{-\int_ {0}^{t_ {j}}\sigma(\mathbf{x}({t}),\mathbf{d}) d{t}} = T(t_ {j}) - T(t_ {j+1}) = \\
 T(t_ {j}) - T(t_ {j+1}) = T(t_ {j})(1-e^{-\int_ {t_ {j}}^{t_ {j+1}}\sigma(\mathbf{x}({t}), \mathbf{d})dt})$$

After discretizing the rendering equation the equation from [[2]](https://arxiv.org/pdf/2003.08934):

$$\mathbf{C}(\mathbf{o},\mathbf{d}) = \sum_ {j=1}^{N} T_ {j}(1-e^{-\sigma(\mathbf{x}({t}), \mathbf{d})(t_ {j+1}-t_ {j})})\mathbf{c}_ {j}.$$

The transmittance $T(t_ {j})$ is discretized to:

$$T_j = e^{-\sum_{k=0}^{k = j}\sigma(\mathbf{x}({t}),\mathbf{d}) (t_ {k+1}-t_ {k})}.$$

Though [1] criticizes the discretization of the rendering equation as it leads to quadrature instability, it is used in this work.

[1] [NeRF Revisited: Fixing Quadrature Instability in
Volume Rendering](https://arxiv.org/abs/2310.20685)

[1] [NeRF: Representing Scenes as
Neural Radiance Fields for View Synthesis](https://arxiv.org/pdf/2003.08934)

### Rendering a Cube

As an example a cube is rendered where $\sigma$ and $\mathbf{c}$ are analytically known. In particular the function for the absorption density $\sigma$ is given by:

$$
\sigma(\mathbf{x}) = \begin{cases}
1 & \text{if } \mathbf{x} \in [0,1]^3 \\
0 & \text{otherwise}
\end{cases}
$$

additionally the color is an arbitrary function in $ \mathbf{x} \in \mathbb{R}^3$. For example a gradient function is:

$$
\mathbf{c}(\mathbf{x}) = \begin{cases}
\mathbf{x} & \text{if } \mathbf{x} \in [0,1]^3 \\
\mathbf{0} & \text{otherwise}
\end{cases}
$$

Rendering the cube with lighting on one side:

<img src="cube.png" width="300" height="300">

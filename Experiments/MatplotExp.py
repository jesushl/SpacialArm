import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

class MatplotExp():
    def __init__(self):
        pass
    def axes(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        theta = np.linspace(-2 * np.pi, 4 * np.pi, 200)
        z = np.linspace(-2, 2, 200)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        ax.plot(x, y, z, label='parametric curve')
        ax.legend()

        plt.show()

if __name__ == "__main__":
    mpe = MatplotExp()
    mpe.axes()

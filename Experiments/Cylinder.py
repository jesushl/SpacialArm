import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D

class Cylinder():
    def __init__(self, radius = 0, altura = 0 , x_center  = 0, y_center = 0, elevation = 0 ):
         self.radius            =   radius
         self.height            =   altura
         self.x_center          =   x_center
         self.y_center          =   y_center
         self.elevation         =   elevation
         self.resolution        =  100
    def getCylinderLinspace(self):
        linspace = {'x' : None, 'y' : None, 'z' : None}
        x = np.linspace((self.x_center - self.radius) , self.x_center + self.radius ,  self.resolution)
        z = np.linspace(self.elevation, (self.elevation + self.height) , self.resolution)

        X,Z =   np.meshgrid(x,z)
        Y =     2 * np.sqrt(self.radius ** 2 - (X - self.x_center)**2 + self.y_center )

        linspace['x'] = X
        linspace['y'] = Y
        linspace['z'] = Z
        return linspace
        

if __name__ == '__main__':
    fig     = plt.figure()
    ax      = Axes3D(fig, azim = 30, elev= 30)
    cilinder = Cylinder(3, 10, 0,0, 0, )
    linspace = cilinder.getCylinderLinspace()
    ax.plot_surface(linspace['x'],  linspace['y'], linspace['z'])
    ax.plot_surface(linspace['x'], ( - linspace['y']), linspace['z'])
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')
    plt.show()

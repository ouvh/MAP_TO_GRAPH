import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_sphere_points(num_points):
    phi = np.linspace(0, np.pi, num_points)
    theta = np.linspace(0, 2 * np.pi, num_points)
    
    phi, theta = np.meshgrid(phi, theta)
    
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    
    return x, y, z

def plot_sphere(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='b', alpha=0.2, edgecolors='k')
    ax.set_box_aspect([1, 1, 1])
    plt.show()

# Adjust the number of points based on the desired resolution
num_points = 100
x, y, z = generate_sphere_points(num_points)
plot_sphere(x, y, z)

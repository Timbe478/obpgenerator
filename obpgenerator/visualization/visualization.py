import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib import widgets

def visualize_part(part):
    vis = Visualization()
    z_pos = 0
    for layer in part.layers:
        contour_paths = []
        for shape in layer.shapes:
            if type(shape.paths) is list:
                contour_paths = contour_paths + shape.paths
            else:
                contour_paths.append(shape.paths)
        vis.add_paths(contour_paths,z_pos)
        z_pos = z_pos + part.layer_height
    vis.show()


class Visualization:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    contours = []

    def add_paths(self,paths,z_level,color='red'):
        layer = []
        for path in paths:
            layer.append(self.ax.plot(path.vertices[:, 0], path.vertices[:, 1], len(path.vertices[:, 1])*[z_level], color=color))
        self.contours.append(layer)
    def show(self):
        def change_status_of_layer(layer,visability=True):
            for path in layer:
                path[0].set_visible(visability)

        def filter_layers(val):
            for i in range(0,int(val[0])):
                change_status_of_layer(self.contours[i],visability=False)
            for i in range(int(val[0]),int(val[1])+1):
                change_status_of_layer(self.contours[i],visability=True)
            for i in range(int(val[1])+1,len(self.contours)):
                change_status_of_layer(self.contours[i],visability=False)
        numb_of_layers = len(self.contours)-1
        rax = plt.axes([0.05, 0.2, 0.05, 0.6])
        layer_slider = widgets.RangeSlider(rax,'Layers',0,numb_of_layers,valstep=1,orientation='vertical',valinit=(0,numb_of_layers))
        layer_slider.on_changed(filter_layers)

        plt.show()
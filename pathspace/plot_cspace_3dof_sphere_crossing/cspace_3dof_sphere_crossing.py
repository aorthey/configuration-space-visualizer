import sys
import numpy as np
from cspace_visualizer import *
from matplotlib.patches import Circle, PathPatch

import mpl_toolkits.mplot3d.art3d as art3d

import matplotlib.pyplot as plt

font_size = 35
zoffset = -3

fname3D = "../data/spheres/cspace_robot_Robot3D.samples"
fname2D = "../data/spheres/cspace_robot_Robot2D.samples"

fname1 = "../data/spheres/path_03D_disk_crossing_1.xml"
fname2 = "../data/spheres/path_03D_disk_crossing_2.xml"
fname3 = "../data/spheres/path_03D_disk_crossing_3.xml"
fname4 = "../data/spheres/path_03D_disk_crossing_4.xml"

[P1,P2,P3] = generateSamples(fname3D)
fig = plt.figure(0,figsize = [-1,1])
fig.patch.set_facecolor('white')
ax = fig.add_subplot(111, projection = '3d')
plotCSpace3DGreyValid(ax, P1, P2, P3)

[P1, P2] = generateSamplesTwoDim(fname2D)
#2D
plotCSpace3DAll(ax, P1, P2, zoffset*np.ones(P1.shape))
ax.axis('off')
plotRectangle(ax, zoffset)
plotCube(ax)
plotAxes(ax, -1, -1, 0, zoffset, zorderAx = 10)

plotPath3D(fname1, 'm')
# plotPath3D(fname2, 'm')
plotPath3D(fname3, 'm', zorder=7)
plotPath3D(fname4, 'm', zorder=7)

plotPathXYProjection(fname1, 'm', zoffset)
# plotPathXYProjection(fname2, 'm', zoffset)
plotPathXYProjection(fname3, 'm', zoffset)
plotPathXYProjection(fname4, 'm', zoffset)

# fig = plt.figure(1,figsize = [-1,1])
# fig.patch.set_facecolor('white')
# ax = fig.add_subplot(111, projection = '3d')
# ax.axis('off')
# plotCube(ax)
# plotSpheres(ax, 0.08)
# plotAxesXYZ(ax, -1, -1, -1)

# plt.subplots_adjust(top=0.7)
# ax.view_init(elev = 25, azim = -60)
# plt.savefig(fname+".svg", bbox_inches='tight', format='svg')
plt.show()


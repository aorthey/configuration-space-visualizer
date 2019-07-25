import sys
import numpy as np
from cspace_visualizer import *
import matplotlib.pyplot as plt


font_size = 45

fname = "../data/car/cspace_robot_car.samples"
fname1 = "../data/car/path_car_backward_bottom.xml"
fname2 = "../data/car/path_car_backward_top.xml"
fname3 = "../data/car/path_car_forward_bottom.xml"
fname4 = "../data/car/path_car_forward_top.xml"

#PlotSamples3D(fname)


[C1,C2,C3] = generateInfeasibleSamplesThreeDim(fname, dim1=0, dim2=1, dim3=2)

################################################################################
### CSPACE 3D
################################################################################
fig = plt.figure(1,figsize = [8,8])
fig.patch.set_facecolor('white')

ax = fig.add_subplot(111, projection = '3d')

zlow = -21
zhigh = -5
y = -1
x = -2
maximumEdgeLength = 0.19
maximumEdgeLength2 = 0.16
#X can't be 0!
plotCSpace3DGrey(ax, C1,C2,C3, fname1,fname2,fname3,fname4,X = 0.4,zorder = 3,maximumEdgeLength = maximumEdgeLength)
plotCSpace3DGrey(ax, C1,C2,C3, fname1,fname2,fname3,fname4,X = -0.4,zorder=1,maximumEdgeLength = maximumEdgeLength)
plotCSpaceXYProjection(ax, C1,C2,C3,fname1,fname2,fname3,fname4, Z = zlow, maximumEdgeLength=maximumEdgeLength2)
plotAxes(ax, x, y, zhigh, zlow)

ax.axis('off')
plt.subplots_adjust(top=0.7)
ax.view_init(elev = 25, azim = -60)

# plt.savefig(csname, bbox_inches='tight')
fig.tight_layout()
plt.show()


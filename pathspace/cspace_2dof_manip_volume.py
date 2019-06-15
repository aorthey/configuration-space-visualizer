import sys
import numpy as np
from cspace_visualizer import *
import matplotlib.pyplot as plt

font_size = 45

fname = "data/manip/cspace_robot_2dof.samples"
PlotSamples(fname)
# fname = "data/car/cspace_robot_car.samples"
# PlotSamples3D(fname)

# Q = np.array(getPoints(fname))
# feasible = np.array(Q[:,0])
# print(feasible)

[C1,C2] = generateInfeasibleSamplesTwoDim(fname, dim1=0, dim2=1)

################################################################################
### CSPACE
################################################################################
fig = plt.figure(1)
fig.patch.set_facecolor('white')
ax = fig.gca()
# ax.set_xlabel(r'\theta_1',fontsize=font_size)
# ax.set_ylabel(r'\theta_2',rotation=1.57,fontsize=font_size)
ax.tick_params(axis='both', which='major', pad=15)
plt.axis([-3.14,3.14,-1.57,1.57])
plotCSpaceDelaunayGrey(C1,C2,0.3)
# plt.savefig(csname, bbox_inches='tight')
plt.show()

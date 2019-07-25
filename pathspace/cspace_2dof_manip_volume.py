import sys
import numpy as np
from cspace_visualizer import *
import matplotlib.pyplot as plt

font_size = 45

fname = "data/manip/cspace_robot_2dof.samples"
fname1 = "data/manip/path_02D_manipulator_1.xml"
fname2 = "data/manip/path_02D_manipulator_2.xml"
fname3 = "data/manip/path_02D_manipulator_3.xml"
PlotSamples(fname)
# fname = "data/car/cspace_robot_car.samples"
#PlotSamples3D(fname)

# Q = np.array(getPoints(fname))
# feasible = np.array(Q[:,0])
# print(feasible)

[C1,C2] = generateInfeasibleSamplesTwoDim(fname, dim1=0, dim2=1)

################################################################################
### CSPACE 2D
################################################################################
fig = plt.figure(1)
fig.patch.set_facecolor('white')
ax = fig.gca()
ax.set_xlabel(r'\theta_1',fontsize=font_size)
ax.set_ylabel(r'\theta_2',rotation=1.57,fontsize=font_size)
ax.tick_params(axis='both', which='major', pad=15)
plt.axis([-3.14,3.14,-1.57,1.57])
plotCSpaceDelaunayGrey(fname1,fname2,fname3,C1,C2,0.3)

##plotCSpaceCylindricalProjection(C1,C2)
## plt.savefig(csname, bbox_inches='tight')
plt.show()


################################################################################
### CSPACE 3D
################################################################################
fig = plt.figure(1)
fig.patch.set_facecolor('white')

ax = fig.add_subplot(111, projection = '3d')
ax.set_xlabel(r'',fontsize=font_size)
ax.set_ylabel(r'',rotation=1.57,fontsize=font_size)
ax.set_zlabel(r'',fontsize=font_size)
#ax.tick_params(axis='both', which='major', pad=15)
#plt.axis([3.14,-3.14,-1.57,1.57,-1.57,1.57])
#plotCSpaceDelaunay3D(fname1,fname2,fname3,C1,C2,0.3)

C1 = C1.astype(float)
C2 = C2.astype(float)
#plotCSpaceDelaunay(C1,C2)
plotCSpaceCylindricalProjection(C2,C1,fname1,fname2,fname3)
# plt.savefig(csname, bbox_inches='tight')
plt.show()


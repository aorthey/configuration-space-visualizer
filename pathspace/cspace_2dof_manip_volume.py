import sys
import numpy as np
from cspace_visualizer import *
import matplotlib.pyplot as plt

font_size = 45

output_name = "2dof_manip"
folder_name = "data/"
csname = folder_name+output_name+"_cspace.png"
csname_samples = folder_name+output_name+"_cspace_volumes.png"

# qfname = folder_name+"cspace_robot_2dof_inner.samples"
fname = folder_name+"cspace_robot_2dof.samples"

PlotSamples(fname)
# Q = np.array(getPoints(fname))
# feasible = np.array(Q[:,0])
# print(feasible)

#[C1,C2] = generateInfeasibleSamplesTwoDim(cfname, dim1=0, dim2=1)

################################################################################
### CSPACE
################################################################################
#fig = plt.figure(1)
#fig.patch.set_facecolor('white')
#ax = fig.gca()
## ax.set_xlabel(r'\theta_1',fontsize=font_size)
## ax.set_ylabel(r'\theta_2',rotation=1.57,fontsize=font_size)
#ax.tick_params(axis='both', which='major', pad=15)
#plt.axis([-3.14,3.14,-1.57,1.57])
#plotCSpaceDelaunayGrey(C1,C2,0.2)
## plt.savefig(csname, bbox_inches='tight')
#plt.show()

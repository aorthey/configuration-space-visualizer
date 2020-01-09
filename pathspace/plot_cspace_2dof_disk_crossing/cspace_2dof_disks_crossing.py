import sys
import numpy as np
from cspace_visualizer import *
import matplotlib.pyplot as plt

font_size = 35

fname = "../data/disks/cspace_robot_disk1.samples"
fname1 = "../data/disks/path_02D_disk_crossing_braid1.xml"
fname2 = "../data/disks/path_02D_disk_crossing_braid2.xml"

[C1,C2] = generateInfeasibleSamplesTwoDim(fname, dim1=0, dim2=3)

# PlotSamples(fname)


################################################################################
### CSPACE 2D
################################################################################
fig = plt.figure(1)
fig.patch.set_facecolor('white')
ax = fig.gca()
ax.set_xlabel(r'$x_1$',fontsize=font_size)
ax.set_ylabel(r'$x_2$',rotation=1.57,fontsize=font_size)
ax.tick_params(axis='both', which='major', pad=15)
offset=0.05
plt.axis([-1-offset,+1+offset,-1-offset,+1+offset])
plotPath(fname1, ax, "green", 0.3, xarrowoffset=0.3, yarrowoffset=-0.15, name=r'$p_1$')
plotPath(fname2, ax, "green", 0.2, xarrowoffset=-0.2, yarrowoffset=+0.15, name=r'$p_2$')
Qu = np.array(getPath(fname1))

# plt.scatter(Qu[0,1], Qu[0,4], marker = "o", s=10, linewidths = 1, color = "green")
plotCSpaceDelaunayGrey(fname1,fname2,C1,C2,0.3)

x1 = float(Qu[0,1])
y1 = float(Qu[0,4])
x2 = float(Qu[-1,1])
y2 = float(Qu[-1,4])
# plt.scatter([x1,x2], [y1,y2], "og")
plt.plot(x1,y1,'og', markersize=20)
plt.plot(x2,y2,'or', markersize=20)

fig.tight_layout()
plt.savefig(fname+".svg", bbox_inches='tight', format='svg')
print(fname)

plt.show()


################################################################################
### CSPACE 3D
################################################################################
#fig = plt.figure(1,figsize = [6,7.8])
##fig.patch.set_facecolor('white')

#ax = fig.add_subplot(111, projection = '3d')
#ax.axis('off')
#ax.view_init(elev = 25, azim = -90)
#plt.subplots_adjust(top=1)
##ax.set_xlabel(r'',fontsize=font_size)
##ax.set_ylabel(r'',rotation=1.57,fontsize=font_size)
##ax.set_zlabel(r'',fontsize=font_size)
#C1 = C1.astype(float)
#C2 = C2.astype(float)
#plotCSpaceCylindricalProjection(C2,C1,fname1,fname2,fname3,ax)
#plt.subplots_adjust(top=0.9)
#fig.tight_layout()
#plt.savefig(fname+".svg", bbox_inches='tight', format='svg')
#plt.show()


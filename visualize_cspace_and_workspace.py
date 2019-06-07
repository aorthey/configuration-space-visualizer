import sys
import numpy as np
from src.cspace_visualizer import *
import os
if not os.path.exists("images"):
  os.makedirs("images")
from worlds import manipulator_2dof as World
from matplotlib.ticker import MaxNLocator

world = World.Manipulator2dof()
worldName = world.getName()
N = 200

c1 = (0.9,0.9,0.9)
c2 = (0.7,0.7,0.7)
c3 = (0.5,0.5,0.5)
q1 = np.linspace(-np.pi,np.pi,N)
q2 = np.linspace(-np.pi,np.pi,N)
P1 = []
P2 = []
M = np.zeros((q1.shape[0], q2.shape[0]))
for i in range(q1.shape[0]):
  for j in range(q2.shape[0]):
    q = np.array((q1[i],q2[j]))
    if not world.isFeasible(q):
      M[i,j] = 1
      P1 = np.append(P1,q1[i])
      P2 = np.append(P2,q2[j])

infeasibleColumns = np.sum(M,axis=1)>=N
Q1 = []
Q2 = []
for i in range(q1.shape[0]):
  for j in range(q2.shape[0]):
    q = np.array((q1[i],q2[j]))
    if infeasibleColumns[i]:
      Q1 = np.append(Q1,q1[i])
      Q2 = np.append(Q2,q2[j])

font_size = 25
offset = 0.5
p1 = np.array([0.5,2.57])
p2 = np.array([-1.57,-0.9])
p3 = np.array([2.5,-1.2])
symbol='x'
greyshade = 0.75

x1loc= (p1[0]-offset,p1[1]-offset)
x2loc= (p2[0]-offset,p2[1]-offset)
x3loc= (p3[0]-offset,p3[1]-offset)
###########################################################
fig = plt.figure(0)
fig.patch.set_facecolor('white')
ax = fig.gca()
ax.set_xlabel(r'x',fontsize=font_size)
ax.set_ylabel(r'y',rotation=1.57,fontsize=font_size)
ax.tick_params(axis='both', which='major', pad=15)
lim=1.1
plt.axis([-lim,lim,-lim,lim])

world.COLOR = c1
world.plotRobotAtConfig(ax,p1)
world.COLOR = c2
world.plotRobotAtConfig(ax,p2)
world.COLOR = c3
world.plotRobotAtConfig(ax,p3)

w1 = world.getEndeffectorPositions(p1)
w2 = world.getEndeffectorPositions(p2)
w3 = world.getEndeffectorPositions(p3)
yoffset = np.array((0.0,0.1))
xoffset = np.array((0.1,0.0))

ax.annotate(r''+symbol+'_1', w1+yoffset)
ax.annotate(r''+symbol+'_2', w2-2*yoffset-2*xoffset)
ax.annotate(r''+symbol+'_3', w3+yoffset)
world.plotObstacles(ax)
plt.savefig("images/"+worldName+"_workspace.png", bbox_inches='tight')

############################################################
fig = plt.figure(1)
fig.patch.set_facecolor('white')
ax = fig.gca()
ax.set_xlabel(r'\theta_1',fontsize=font_size)
ax.set_ylabel(r'\theta_2',rotation=1.57,fontsize=font_size)
ax.tick_params(axis='both', which='major', pad=15)

lim=3.14
plt.axis([-lim,lim,-lim,lim])
ax.annotate(r''+symbol+'_1', x1loc)
ax.annotate(r''+symbol+'_2', x2loc)
ax.annotate(r''+symbol+'_3', x3loc)
plt.plot(p1[0],p1[1],'o',color='black',markersize=10)
plt.plot(p2[0],p2[1],'o',color='black',markersize=10)
plt.plot(p3[0],p3[1],'o',color='black',markersize=10)

plotCSpaceDelaunayGrey(P1,P2,0.15)
plt.savefig("images/"+worldName+"_configuration_space.png", bbox_inches='tight')
plt.show()


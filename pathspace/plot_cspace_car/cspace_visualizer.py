import pickle as pk

import sys
import numpy as np


from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('font', family='serif', size=28)

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

pointsize = 20

#plots the 2D triangulated space with all infeasible points in grey and three possible paths in different colors
def plotCSpace3DGrey(ax,P1,P2,P3,fname1,fname2,fname3,fname4,X=0.01,zorder=2,maximumEdgeLength=0.2, shade=0.8):
  points2D=np.vstack([P2,P3]).T
  tri = Delaunay(points2D)
  # print tri.simplices.shape, '\n', tri.simplices[0]
  zorderPath = 0.5
  zorderText = 11
  plotPath3D(fname1, 'magenta', zorder = zorderPath)
  ax.text(1,0,-5,r'$p_1$',zorder = zorderText)
  plotPath3D(fname2, 'magenta', zorder = zorderPath)
  #use, when not showing theta-x and theta-y planes
  #ax.text(0,-0.2,1,r'$p_2$',zorder = 11)
  ax.text(-0.7,-0.5,0.8,r'$p_2$',zorder = zorderText)
  plotPath3D(fname3, 'magenta', zorder = zorderPath)
  ax.text(0.2,-1,0.5,r'$p_3$', zorder = zorderText)
  plotPath3D(fname4, 'magenta', zorder = zorderPath)
  ax.text(1.3,0.3,0,r'$p_4$', zorder = zorderText)
  plotStartGoal3D(fname1)

  xpp = -0.4
  zorderMiddle = 4
  plotPathPart3D(fname1, 'magenta',xpp,zorder = zorderMiddle)
  plotPathPart3D(fname2, 'magenta',xpp,zorder = zorderMiddle)
  plotPathPart3D(fname3, 'magenta',xpp,zorder = zorderMiddle)
  plotPathPart3D(fname4, 'magenta',xpp,zorder = zorderMiddle)
  
  xpp = 0.4
  zorderEnd = 10
  plotPathPart3D(fname1, 'magenta',xpp,zorder = zorderEnd)
  plotPathPart3D(fname2, 'magenta',xpp,zorder = zorderEnd)
  plotPathPart3D(fname3, 'magenta',xpp,zorder = zorderEnd)
  plotPathPart3D(fname4, 'magenta',xpp,zorder = zorderEnd)

  triangles = np.empty((0,3),dtype=int)

  for i in range(0, tri.simplices.shape[0]):
    simplex = tri.simplices[i]
    x = tri.points[simplex[0]]
    y = tri.points[simplex[1]]
    z = tri.points[simplex[2]]
    d0 = np.sqrt(np.dot(x-y,x-y))
    d1 = np.sqrt(np.dot(x-z,x-z))
    d2 = np.sqrt(np.dot(z-y,z-y))
    max_edge = max([d0, d1, d2])
    if max_edge <= maximumEdgeLength:
      triangles = np.vstack((triangles, simplex))

  Px = np.linspace(X+0.00000001,X-0.00000001, P2.size)
  ax.plot_trisurf(Px,P2, P3, triangles=triangles, alpha=1, color = "whitesmoke", facecolors = "grey", zorder = zorder)
  
def plotCSpaceXYProjection(ax,P1,P2,P3,fname1,fname2,fname3,fname4,Z=0,maximumEdgeLength=0.2, shade=0.8):

  plotPathXYProjection(fname1, 'magenta', Z)
  #ax.text(1.5,-0.8,Z,r'$\pi(p_1),\pi(p_3)$')
  plotPathXYProjection(fname2, 'magenta', Z)
  #ax.text(1.5,0.3,Z,r'$\pi(p_2),\pi(p_4)$')
  plotPathXYProjection(fname3, 'magenta', Z)
  plotPathXYProjection(fname4, 'magenta', Z)
  plotStartGoalXYProjection(fname1, Z)
  project = Arrow3D([0,0],[0,0],[-8,-15], color = 'black', zorder = 0.05, linewidth= '3', arrowstyle = "-|>", mutation_scale = 20, label = "project")
  ax.add_artist(project)

  #remove points in xy, that are not for all theta feasible
  P1s = []
  P2s = []
  innerbound = 0.48
  outerbound = 0.64
  for i in range(P1.size):
      #if P1[i] not in range(0.7, 0.8):
      if P2[i] < - outerbound or P2[i]>outerbound or (P2[i] > - innerbound and P2[i] < innerbound):
          P1s.append(P1[i])
          P2s.append(P2[i])
  P1s = np.asarray(P1s)
  P2s = np.asarray(P2s)
  
  points2D=np.vstack([P1s,P2s]).T
  tri = Delaunay(points2D)

  triangles = np.empty((0,3),dtype=int)

  for i in range(0, tri.simplices.shape[0]):
    simplex = tri.simplices[i]
    x = tri.points[simplex[0]]
    y = tri.points[simplex[1]]
    z = tri.points[simplex[2]]
    d0 = np.sqrt(np.dot(x-y,x-y))
    d1 = np.sqrt(np.dot(x-z,x-z))
    d2 = np.sqrt(np.dot(z-y,z-y))
    max_edge = max([d0, d1, d2])
    if max_edge <= maximumEdgeLength:
      triangles = np.vstack((triangles, simplex))
 
  Pz = np.linspace(Z+0.00000001,Z-0.00000001, P2s.size)
  ax.plot_trisurf(P1s ,P2s, Pz, triangles=triangles, color = "silver")

def plotStartGoal3D(fname):
  Qu = np.array(getPath(fname))
  startx = Qu[0,1].astype(float)
  starty = Qu[0,2].astype(float)
  startz = Qu[0,3].astype(float)
  goalx = Qu[- 1,1].astype(float)
  goaly = Qu[- 1,2].astype(float)
  goalz = Qu[- 1,3].astype(float)
  plt.plot([startx], [starty], [startz], marker = "o", markersize = pointsize/2, color = "chartreuse")
  plt.plot([goalx], [goaly], [goalz], marker = "o", markersize = pointsize/2, color = "red")
        
def plotStartGoalXYProjection(fname, z):
  Qu = np.array(getPath(fname))
  startx = Qu[0,1].astype(float)
  starty = Qu[0,2].astype(float)
  startz = z
  goalx = Qu[- 1,1].astype(float)
  goaly = Qu[- 1,2].astype(float)
  goalz = z
  plt.plot([startx], [starty], [startz], marker = "o", markersize = pointsize/2, color = "chartreuse")
  plt.plot([goalx], [goaly], [goalz], marker = "o", markersize = pointsize/2, color = "red")

def plotPathXYProjection(fname, colour, Z):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,1]
  p2 = Qu[:,2]
  p3a = Z
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  plt.plot(p1, p2, p3a, linewidth=2.5, color= colour)
  
def plotPath3D(fname, colour, zorder = 0.3):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,1]
  p2 = Qu[:,2]
  p3a = Qu[:,3]
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  p3a = p3a.astype(float)
  #for the first path, so it doesn't jump from pi to -pi
  for i in range(p3a.size):
      if p3a[i] == 3.14118:
          p3a[i:p3a.size] = -p3a[i:p3a.size]
  plt.plot(p1, p2, p3a, linewidth=3, alpha = 1, color= colour, zorder = zorder)
  
def plotPathPart3D(fname, colour, x, zorder = 3):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,1].astype(float)
  p2 = Qu[:,2].astype(float)
  p3a = Qu[:,3].astype(float)
  #for the first path, so it doesn't jump from pi to -pi
  for i in range(p3a.size):
      if p3a[i] == 3.14118:
          p3a[i:p3a.size] = -p3a[i:p3a.size]
  #start path from x, create additional point slightly behind x 
  #without that, if there is no sample point nearby, plot will plot
  #a straight line to the last point which may look really strange
  l1, l2, l3 = [], [],[]
  for i in range(p3a.size):
    if p1[i] >= x:
        l1.append(p1[i])
        l2.append(p2[i])
        l3.append(p3a[i])
  p1 = np.asarray(l1)
  p2 = np.asarray(l2)
  p3a = np.asarray(l3)
  p1b = np.ndarray(p1.size+1)
  p2b = np.ndarray(p2.size+1)
  p3b = np.ndarray(p3a.size+1)
  p1b[0] = x + 0.01
  p1b[1:p1b.size] = p1
  p2b[0] = p2[0]
  p2b[1:p2b.size] = p2
  p3b[0] = p3a[0]
  p3b[1:p3b.size] = p3a
  
  plt.plot(p1b, p2b, p3b, linewidth=3, alpha = 1, color= colour, zorder = zorder)
  
def plotAxes(ax, x, y, zhigh, zlow, zorderAx = 10):
  #plot axes and their labels
  xaxis = Arrow3D([x,x+1],[y,y],[zlow,zlow], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "xaxis", zorder = zorderAx)
  ax.text(x+1,y-0.5,zlow,r'x')
  ax.add_artist(xaxis)
  xaxishigh = Arrow3D([x,x+1],[y,y],[zhigh,zhigh], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "xaxis", zorder = zorderAx)
  ax.text(x+1,y-0.5,zhigh,r'x')
  ax.add_artist(xaxishigh)

  yaxis = Arrow3D([x,x],[y-0.02,y+0.6],[zlow,zlow], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "yaxis", zorder = zorderAx)
  ax.text(x-0.4,y+0.7,zlow,r'y')
  ax.add_artist(yaxis)
  yaxishigh = Arrow3D([x,x],[y,y+0.6],[zhigh,zhigh], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "yaxis", zorder = zorderAx)
  ax.text(x-0.4,y+0.7,zhigh,r'y')
  ax.add_artist(yaxishigh)

  zaxis =Arrow3D([x+0.03,x+0.03],[y,y],[zhigh,zhigh + 5], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "zaxis", zorder = zorderAx)
  ax.text(x,y-0.1,zhigh+5,r'$\theta$')
  ax.add_artist(zaxis)
  
  
  #plot coordinate planes
  xlin = np.linspace(-x,x, 50)
  ylin = np.linspace(-y,y, 50)
  zlin = np.linspace(-zhigh,zhigh,50)
  
  Xlin1, Ylin1 = np.meshgrid(xlin,ylin)
  Xlin2, Zlin1 = np.meshgrid(xlin,zlin)
  Ylin2, Zlin2 = np.meshgrid(ylin,zlin)
  
  #xy
  ax.plot_wireframe(Xlin1,Ylin1,zlow,rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)
  ax.plot_wireframe(Xlin1,Ylin1,zhigh,rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)

  #thetax
  ax.plot_wireframe(Xlin2, -y, Zlin2, rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)
  
  #thetay
  ax.plot_wireframe(x, Ylin2,Zlin2, rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)


def long_edges(x, y, triangles, radio=22):
  out = []
  for points in triangles:
    #print points
    a,b,c = points
    d0 = np.sqrt( (x[a] - x[b]) **2 + (y[a] - y[b])**2 )
    d1 = np.sqrt( (x[b] - x[c]) **2 + (y[b] - y[c])**2 )
    d2 = np.sqrt( (x[c] - x[a]) **2 + (y[c] - y[a])**2 )
    max_edge = max([d0, d1, d2])
    #print points, max_edge
    if max_edge > 0.25:
      out.append(True)
    else:
      out.append(False)
      #if max_edge < 0.1:
      #  out.append(True)
      #else:
      #  out.append(False)
  return out


def getPoints(fname, maxElements = float('inf')):
  ### output: [feasible {True,False}, sufficient {True,False}, open_ball_radius
  ### {real}, number_of_states {int}, states {vector of real}]

  import xml.etree.ElementTree
  root = xml.etree.ElementTree.parse(fname).getroot()
  Q = list()
  ctr = 0
  for child in root.findall('state'):
    if ctr > maxElements:
      return Q
    sufficient = child.get('sufficient')
    feasible = child.get('feasible')
    open_ball_radius = child.get('open_ball_radius')
    state = child.text
    state = state.split(" ")

    if feasible=='yes':
      feasible = True
    else:
      feasible = False
    if sufficient=='yes':
      sufficient = True
    else:
      sufficient = False
    q = list()
    q.append(feasible)
    q.append(sufficient)
    q.append(open_ball_radius)

    for s in state:
      if s != '':
        q.append(s)

    Q.append(q)
    ctr += 1
  return Q

def getPath(fname, maxElements = float('inf')):
  import xml.etree.ElementTree
  root = xml.etree.ElementTree.parse(fname).getroot()
  Q = list()
  ctr = 0
  for child in root.findall('state'):
    if ctr > maxElements:
      return Q
    state = child.text
    state = state.split(" ")
    q = list()
  
    for s in state:
      if s != '':
          q.append(s)

    Q.append(q)
    ctr += 1
  
  return Q
  
def generateInfeasibleSamplesOneDim(fname, dim1=0, maxElements = float('inf')):
  Q = getPoints(fname)
  theta = np.linspace(-np.pi,np.pi,100)
  P1 = []
  P2 = []
  ctr = 0
  for q in Q:
    feasible = q[0]
    #sufficient = q[1]
    #ball_radius = q[2]
    #num_states = q[3]
    x = q[4+dim1]
    if not feasible:
      ctr += 1
      for j in range(theta.shape[0]):
        P1 = np.append(P1,x)
        P2 = np.append(P2,theta[j])
    if ctr > maxElements:
      break
  # np.save('tmp_QS_dense_1',P1)
  # np.save('tmp_QS_dense_2',P2)
  return [P1,P2]

def generateInfeasibleSamplesTwoDim(fname, dim1=0, dim2=1, maxElements = float('inf')):
  Q = getPoints(fname)
  P1 = []
  P2 = []
  ctr = 0
  for q in Q:
    feasible = q[0]
    #sufficient = q[1]
    #ball_radius = q[2]
    #num_states = q[3]
    x = q[4+dim1]
    y = q[4+dim2]
    if not feasible:
      ctr += 1
      P1 = np.append(P1,x)
      P2 = np.append(P2,y)
    if ctr > maxElements:
      break
  return [P1,P2]

def generateInfeasibleSamplesThreeDim(fname, dim1=0, dim2=1, dim3=2, maxElements = float('inf')):
  Q = getPoints(fname)
  #print(Q)
  P1 = []
  P2 = []
  P3 = []
  ctr = 0
  for q in Q:
    feasible = q[0]
    #sufficient = q[1]
    #ball_radius = q[2]
    #num_states = q[3]
    x = float(q[4+dim1])
    y = float(q[4+dim2])
    z = float(q[4+dim3])
    if not feasible:
      if x < 1 and x > -1 and y < 1.3 and y > -1.3 and z < 4 and z > -4:
        if z > 2:
          z = z - np.pi * 2
        ctr += 1
        P1 = np.append(P1,x)
        P2 = np.append(P2,y)
        P3 = np.append(P3,z)
    if ctr > maxElements:
      break
  
  return [P1,P2,P3]

def plotSamplesOneDim(fname, dim1=0, maxElements = float('inf')):
  Q = getPoints(fname, maxElements)
  for q in Q:
    feasible = q[0]
    sufficient = q[1]
    d = float(q[2])
    x = float(q[4+dim1])
    if not feasible:
      plt.axvline(x, color='k', linewidth=1)
    elif sufficient:
      plt.axvspan(x-d, x+d, alpha=0.5, hatch="/")
    else:
      delta=0.05
      plt.fill([x-d, x+d, x+d, x-d], [-delta,-delta,+delta,+delta], fill=False, hatch='\\')

def PlotSamples(fname, dim1=4, dim2=5, maxElements=float('inf')):
  Q = np.array(getPoints(fname))
  feasible = np.array(Q[:,0]).astype(bool)
  notFeasible = ~feasible

  t1 = Q[np.where(feasible),dim1].flatten()
  t2 = Q[np.where(feasible),dim2].flatten()
  t1 = t1.astype(float)
  t2 = t2.astype(float)

  t3 = Q[np.where(notFeasible),dim1].flatten()
  t4 = Q[np.where(notFeasible),dim2].flatten()
  t3 = t3.astype(float)
  t4 = t4.astype(float)

  plt.scatter(t1,t2, marker='x', color='green')
  plt.scatter(t3,t4, marker='o', color='red')
  
  plt.show()

def PlotSamples3D(fname, dim1=4, dim2=5, dim3=6, maxElements=float('inf')):
  Q = np.array(getPoints(fname))
  feasible = np.array(Q[:,0]).astype(bool)
  notFeasible = ~feasible

  t1 = Q[np.where(feasible),dim1].flatten()
  t2 = Q[np.where(feasible),dim2].flatten()
  t3 = Q[np.where(feasible),dim3].flatten()
  t1 = t1.astype(float)
  t2 = t2.astype(float)
  t3 = t3.astype(float)

  t4 = Q[np.where(notFeasible),dim1].flatten()
  t5 = Q[np.where(notFeasible),dim2].flatten()
  t6 = Q[np.where(notFeasible),dim3].flatten()
  t4 = t4.astype(float)
  t5 = t5.astype(float)
  t6 = t6.astype(float)

  #print(t3)

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  ax.scatter(t1, t2, t3, marker='x', color='green')
  #ax.view_init(azim = 0, elev = 90)
  #ax.set_yticks([-0.65, 0.6, -0.55, 0, 0.55, 0.6, 0.65])
  # ax.set_xlabel('X')
  # ax.set_ylabel('Y')
  # ax.set_zlabel(r'$\theta$')
  #plt.scatter(t4, t5, t6, marker='o', color='red')
  plt.show()

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
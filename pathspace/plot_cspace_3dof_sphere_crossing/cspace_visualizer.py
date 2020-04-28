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
from matplotlib import cm

from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d import proj3d

pointsize = 20

def plotRectangle(ax, zoffset):
  v1=[-1,-1,zoffset]
  v2=[+1,-1,zoffset]
  v3=[+1,+1,zoffset]
  v4=[-1,+1,zoffset]

  pts = np.array([v1,v2,v3,v4]).T
  ptsEnd = np.roll(pts,-1,1)

  for i in range(4):
    ax.plot([pts[0,i], ptsEnd[0,i]],
            [pts[1,i],ptsEnd[1,i]],
            zs=[pts[2,i],ptsEnd[2,i]], color='k', linestyle='--')

def plotCube(ax):
  plotRectangle(ax, -1)
  plotRectangle(ax, +1)

  plotZAxisLine(ax, -1, -1)
  plotZAxisLine(ax, -1, +1)
  plotZAxisLine(ax, +1, -1)
  plotZAxisLine(ax, +1, +1)

def plotSphere(ax, x, y, z, R, color='g'):
  N=20
  stride=1
  u = np.linspace(0, 2 * np.pi, N)
  v = np.linspace(0, np.pi, N)
  x = np.outer(np.cos(u), R*np.sin(v)) + x
  y = np.outer(np.sin(u), R*np.sin(v)) + y
  z = np.outer(np.ones(np.size(u)), R*np.cos(v)) +z
  ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride,
      color=color)

def plotSpheres(ax, R):
  plotLine(ax, [0,-1,0], [0,+1,0])
  plotSphere(ax, 0, -1, 0, R, 'g')
  plotSphere(ax, 0, +1, 0, R, 'r')

  plotLine(ax, [-1,0,0], [+1,0,0])
  plotSphere(ax, -1, 0, 0, R, 'g')
  plotSphere(ax, +1, 0, 0, R, 'r')

  plotLine(ax, [0,0,-1], [0,0,+1])
  plotSphere(ax, 0, 0, -1, R, 'g')
  plotSphere(ax, 0, 0, +1, R, 'r')

def plotLine(ax, v1, v2):
    ax.plot(
        [v1[0],v2[0]],
        [v1[1],v2[1]],
        zs=[v1[2],v2[2]],
        color='k', linewidth=2, linestyle='-')

def plotZAxisLine(ax, x, y):
  ax.plot([x, x], [y, y], [-1, 1], color='k', linestyle='--')


def plotCSpace3DAll(ax, P1, P2, P3):
  triangles = np.empty((0,3),dtype=int)

  pts = np.array([P1,P2,P3]).T
  hull = ConvexHull(pts, qhull_options="QJ")
  for i in range(0, hull.simplices.shape[0]):
    simplex = hull.simplices[i]
    triangles = np.vstack((triangles, simplex))

  ax.plot_trisurf(P1, P2, P3, triangles=triangles, zorder=10, alpha=0.5, linewidth=0, edgecolor='none',
      cmap=cm.gray, facecolors = 'grey')
  
def updateTriangles(triangles, P1, P2, P3, idx_valid):
  P1I = P1[idx_valid]
  P2I = P2[idx_valid]
  P3I = P3[idx_valid]

  pts = np.array([P1I,P2I,P3I]).T
  hull = ConvexHull(pts, qhull_options="QJ")
  for i in range(0, hull.simplices.shape[0]):
    simplex = hull.simplices[i]
    simplex = idx_valid[simplex]
    triangles = np.vstack((triangles, simplex))

  return triangles

def plotCSpace3DGreyValid(ax, P1, P2, P3):
  triangles = np.empty((0,3),dtype=int)

  dist = 0.20

  idx_valid = np.array(np.where( (abs(P1)<=dist) & (abs(P2)<=dist))).flatten()
  triangles = updateTriangles(triangles, P1, P2, P3, idx_valid)

  idx_valid = np.array(np.where( (abs(P2)<=dist) & (abs(P3)<=dist))).flatten()
  triangles = updateTriangles(triangles, P1, P2, P3, idx_valid)

  idx_valid = np.array(np.where( (abs(P1)<=dist) & (abs(P3)<=dist))).flatten()
  triangles = updateTriangles(triangles, P1, P2, P3, idx_valid)

  ax.plot_trisurf(P1, P2, P3, triangles=triangles, alpha=0.5, zorder=1, linewidth=0, edgecolor='none',
      facecolors = 'grey', 
      cmap=cm.gray)

def plotCSpaceXYProjection(ax,P1,P2,P3,fname1,fname2,fname3,fname4,Z=0,maximumEdgeLength=0.2, shade=0.8):

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
  p2 = Qu[:,5]
  p3a = Z
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  plt.plot(p1, p2, p3a, linewidth=2.5, color= colour)
  
def plotPath3D(fname, colour, zorder = 3):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,1]
  p2 = Qu[:,5]
  p3a = Qu[:,9]
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  p3a = p3a.astype(float)
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
  
def plotAxesXYZ(ax, x, y, z):
  zorderAx = 10
  #plot axes and their labels
  xaxis = Arrow3D([x,x+1],[y,y],[z,z], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "xaxis", zorder = zorderAx)
  ax.text(x+1,y-0.5,z,r'$x$', zorder=zorderAx)
  ax.add_artist(xaxis)

  yaxis = Arrow3D([x,x],[y-0.02,y+1],[z,z], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "yaxis", zorder = zorderAx)
  ax.text(x-0.4,y+0.7,z,r'$y$', zorder=zorderAx)
  ax.add_artist(yaxis)

  zaxis =Arrow3D([x,x],[y,y],[z,z + 1], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "zaxis", zorder = zorderAx)
  ax.text(x-0.3,y-0.3,z+1,r'$z$', zorder=zorderAx)
  ax.add_artist(zaxis)

def plotAxes(ax, x, y, zhigh, zlow, zorderAx = 10):
  #plot axes and their labels
  xaxis = Arrow3D([x,x+1],[y,y],[zlow,zlow], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "xaxis", zorder = zorderAx)
  ax.text(x+1,y-0.5,zlow,r'$x_1$', zorder=zorderAx)
  ax.add_artist(xaxis)
  xaxishigh = Arrow3D([x,x+1],[y,y],[zhigh,zhigh], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "xaxis", zorder = zorderAx)
  ax.text(x+1,y-0.5,zhigh,r'$x_1$', zorder=zorderAx)
  ax.add_artist(xaxishigh)

  yaxis = Arrow3D([x,x],[y-0.02,y+1],[zlow,zlow], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "yaxis", zorder = zorderAx)
  ax.text(x-0.4,y+0.7,zlow,r'$x_2$', zorder=zorderAx)
  ax.add_artist(yaxis)
  yaxishigh = Arrow3D([x,x],[y,y+1],[zhigh,zhigh], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "yaxis", zorder = zorderAx)
  ax.text(x-0.4,y+0.7,zhigh,r'$x_2$', zorder=zorderAx)
  ax.add_artist(yaxishigh)

  zaxis =Arrow3D([x,x],[y,y],[zhigh,zhigh + 1], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "zaxis", zorder = zorderAx)
  ax.text(x-0.3,y-0.3,zhigh+1,r'$x_3$', zorder=zorderAx)
  ax.add_artist(zaxis)
  
  #plot coordinate planes
  xlin = np.linspace(-x,x, 50)
  ylin = np.linspace(-y,y, 50)
  zlin = np.linspace(zhigh-1,zhigh+1,50)
  
  Xlin1, Ylin1 = np.meshgrid(xlin,ylin)
  Xlin2, Zlin1 = np.meshgrid(xlin,zlin)
  Ylin2, Zlin2 = np.meshgrid(ylin,zlin)

  Zlow = zlow*np.ones(Xlin1.shape)
  Zhigh = zhigh*np.ones(Xlin1.shape)
  
  #xy
  ax.plot_wireframe(Xlin1,Ylin1,Zlow,rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)
  ax.plot_wireframe(Xlin1,Ylin1,Zhigh,rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)

  Y = -y*np.ones(Xlin2.shape)
  X = x*np.ones(Xlin2.shape)
  #thetax
  ax.plot_wireframe(Xlin2, -Y, Zlin2, rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)
  
  #thetay
  ax.plot_wireframe(X, Ylin2, Zlin2, rstride = 10, cstride = 10, zorder = 0.1, color = "silver", alpha = 0.2)


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
  

def generateSamplesTwoDim(fname, dim1=0, dim2=4, maxElements = float('inf')):
  Q = getPoints(fname)
  P1 = []
  P2 = []
  ctr = 0
  for q in Q:
    feasible = q[0]
    x = float(q[4+dim1])
    y = float(q[4+dim2])
    if not feasible:
      ctr += 1
      P1 = np.append(P1,x)
      P2 = np.append(P2,y)
    if ctr > maxElements:
      break
  return [P1,P2]

def generateSamples(fname, dim1=0, dim2=4, dim3=8, maxElements = float('inf')):
  Q = getPoints(fname)
  #print(Q)
  P1 = []
  P2 = []
  P3 = []
  ctr = 0
  for q in Q:
    feasible = q[0]
    x = float(q[4+dim1])
    y = float(q[4+dim2])
    z = float(q[4+dim3])
    if not feasible:
      ctr += 1
      P1 = np.append(P1,x)
      P2 = np.append(P2,y)
      P3 = np.append(P3,z)
    if ctr > maxElements:
      break
  
  return [P1,P2,P3]


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

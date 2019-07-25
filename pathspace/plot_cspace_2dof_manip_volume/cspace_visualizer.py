import pickle as pk

import sys
import numpy as np
import math
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('font', family='serif', size=30)

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

pointsize = 20

#plots the 2D triangulated space with all infeasible points in grey and three possible paths in different colors
def plotCSpaceDelaunayGrey(fname1,fname2,fname3,P1,P2,maximumEdgeLength=0.2, shade=0.8):
  points2D=np.vstack([P1,P2]).T
  tri = Delaunay(points2D)
  # print tri.simplices.shape, '\n', tri.simplices[0]

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

  plotPath(fname1, "magenta")
  plotPath(fname2, "magenta")
  plotPath(fname3, "magenta")
  Qu = np.array(getPath(fname1))
  
  plt.scatter(Qu[0,0], Qu[0,1], marker = "o", s=20, linewidths = 5, color = "green")
  plt.scatter(Qu[Qu.size/2 - 1,0], Qu[Qu.size/2 - 1,1], marker = "x", s=50, linewidths = 5, color = "red")
  
  zFaces = np.ones(triangles.shape[0])
  cmap = colors.LinearSegmentedColormap.from_list("", [(shade,shade,shade),"grey","grey"])
  plt.tripcolor(P1, P2, triangles, cmap=cmap, facecolors=zFaces,edgecolors='none')
  
def plotPath(fname, colour):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,0]
  p2 = Qu[:,1]
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  plt.plot(p1, p2, linewidth=2.5, color= colour)
  
def plotPathCylindrical(fname, colour):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,0]
  pz = Qu[:,1]
  p1 = p1.astype(float)
  pz = pz.astype(float)
  px = np.cos(p1)
  py = np.sin(p1)

  plt.plot(px, py, pz, linewidth = 4,color = colour)
  
def plotPathProjection(fname, z, ax):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,0]
  pz = Qu[:,1]
  p1 = p1.astype(float)
  px = np.cos(p1)
  py = np.sin(p1)
  pz = z

  plt.plot(px,py,pz, linewidth = 4, color = "magenta", zorder = 1)

def plotStartGoal(fname):
  Qu = np.array(getPath(fname))
  startx = np.cos(Qu[0,0].astype(float))
  starty = np.sin(Qu[0,0].astype(float))
  startz = Qu[0,1].astype(float)
  goalx = np.cos(Qu[Qu.size/2 - 1,0].astype(float))
  goaly = np.sin(Qu[Qu.size/2 - 1,0].astype(float))
  goalz = Qu[Qu.size/2 - 1,1].astype(float)
  #plt.scatter(math.cos(Qu[0,1]), math.sin(Qu[0,1]), Qu[0,0], marker = "o", s=20, linewidths = 5, color = "green")
  #plt.scatter(math.cos(Qu[Qu.size/2 - 1,1]), math.sin(Qu[Qu.size/2 - 1,1]), Qu[Qu.size/2 - 1,0], marker = "x", s=50, linewidths = 5, color = "red")
  plt.plot([startx], [starty], [startz], marker = "o", markersize = pointsize/2, color = "chartreuse")
  plt.plot([goalx], [goaly], [goalz], marker = "o", markersize = pointsize/2, color = "red")
      
def plotStartGoalProjection(fname, z):
  Qu = np.array(getPath(fname))
  startx = np.cos(Qu[0,0].astype(float))
  starty = np.sin(Qu[0,0].astype(float))
  startz = z
  goalx = np.cos(Qu[Qu.size/2 - 1,0].astype(float))
  goaly = np.sin(Qu[Qu.size/2 - 1,0].astype(float))
  goalz = z
  #plt.scatter(math.cos(Qu[0,1]), math.sin(Qu[0,1]), Qu[0,0], marker = "o", s=20, linewidths = 5, color = "green")
  #plt.scatter(math.cos(Qu[Qu.size/2 - 1,1]), math.sin(Qu[Qu.size/2 - 1,1]), Qu[Qu.size/2 - 1,0], marker = "x", s=50, linewidths = 5, color = "red")
  plt.plot([startx], [starty], [startz], marker = "o", markersize = pointsize/2, color = "chartreuse")
  plt.plot([goalx], [goaly], [goalz], marker = "o", markersize = pointsize/2, color = "red")
      

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

def plotCSpaceCylindricalProjection(PX,PT,fname1,fname2,fname3,ax):

  xs, ys, Z = [],[],[]
  for i in range(0,PX.size):
      if PX[i] <= 1.5 and PX[i] >= -1.5 and PX[i] != 1 and PX[i] != -1:
          Z.append(PX[i])
          xs.append(np.cos(PT[i]))
          ys.append(np.sin(PT[i]))

  xs, ys, Z = np.asarray(xs),np.asarray(ys),np.asarray(Z)
  rad = np.linalg.norm(xs)
  zen = np.arccos(Z/1.51)
  azi = np.arctan2(ys,xs)

  tris = mtri.Triangulation(zen, azi)

  mask = long_edges(zen,azi, tris.triangles, 0.2)
  tris.set_mask(mask)

  #print len(tris.triangles)
  #print len(tris.triangles)
  #print len(tris.edges)
  #plt.triplot(tris, 'bo-', lw=1)
  #plt.show()

  #fig = plt.figure(1)
  #fig.patch.set_facecolor('white')
  #ax  = fig.add_subplot(111, projection='3d')
  #ax.axis('off')
  
  #plot own axes
  #plt.plot([1,1],[0,0], [-2,2], color = 'black', linewidth = '2')
  ta = np.linspace(26*np.pi/50,np.pi,50)
  xa = np.cos(ta)
  ya = -np.sin(ta)
  plt.plot(xa,ya,-1.57*np.ones(50), color = 'black', linewidth = '2')
  theta2 = Arrow3D([-1,-1],[0,0],[-1.57,2.3], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = 'theta1')
  ax.add_artist(theta2)
  theta1 = Arrow3D([-0.01,0.01],[-1,-1],[-1.57,-1.57], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "theta2", zorder = 3)
  plt.plot([-1,-1],[0,0],[-1.57,2], color = 'black', linewidth = '2')
  ax.add_artist(theta1)
  ax.text(-1.3,0,2.2, r'${\theta}_2$')
  ax.text(-1.1,-1.2,-1.57, r'${\theta}_1$')
  
  #ax.text(1,0,0, '1', 'x')
  #ax.text(0,1,0, '2', 'y')
  #ax.text(0,0,1, '3', 'z')
  
  
  ax.plot_trisurf(xs,ys,Z, \
      triangles=tris.get_masked_triangles(),color = "0.75", alpha = 1, \
       linewidth=0, antialiased=False)
  
  
  # ax.set_xlabel(r'r')
  # ax.set_ylabel(r'\phi')
  # ax.set_zlabel(r'z')
  
  plotPathCylindrical(fname1, "magenta")
  x1,y1,z1 = np.cos(np.pi/4), -np.sin(np.pi/4), -1.3
  ax.text(x1+0.1,y1,z1, r'$p_1$')
  plotPathCylindrical(fname2, "magenta")
  x2,y2,z2 = np.cos(np.pi/2), -np.sin(np.pi/2), 1.05
  ax.text(x2,y2,z2, r'$p_2$')
  plotPathCylindrical(fname3, "magenta")
  x3,y3,z3 = -np.cos(np.pi/4), np.sin(np.pi/4), 0.9
  ax.text(x3,y3,z3, r'$p_3$')
  plotStartGoal(fname1)

  #plot projection to circle
  z = -7
  plotPathProjection(fname1, z, ax)
  plotPathProjection(fname2, z, ax)
  plotPathProjection(fname3, z, ax)
  plotStartGoalProjection(fname1, z)
  project = Arrow3D([0,0],[0,0],[-4,-7], alpha = 1 ,color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "theta2")
  ax.add_artist(project)
  plt.plot(xa,ya,z*np.ones(50), color = 'black', linewidth = '2')
  theta3 = Arrow3D([-0.01,0.01],[-1,-1],[z,z], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "theta2")
  plt.plot([0,0],[0,0],[-4,-6.6], color ='black', linewidth = '2.5')
  ax.add_artist(theta3)
  ax.text(-1,-1.2,z, r'${\theta}_1$')
  
  #plot Cylinder
  x=np.linspace(-1, 1, 100)
  z=np.linspace(-1.57, 1.57, 100)
  Xc, Zc=np.meshgrid(x, z)
  Yc = np.sqrt(1-Xc**2)

  rstride = 20
  cstride = 10
  ax.plot_wireframe(Xc, Yc, Zc, alpha=0.4, rstride=rstride, cstride=cstride, color = "silver",zorder = 0.1)
  ax.plot_wireframe(Xc, -Yc, Zc, alpha=0.4, rstride=rstride, cstride=cstride, color = "silver", zorder = 0.1)

  #ax.set_xlabel('')
  #ax.set_ylabel('')
  #ax.set_zlabel('')
  #ax.tick_params(axis='both', which='major', pad=15)
  
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
          if s != '2':
             q.append(s)

    Q.append(q)
    ctr += 1
  
  return Q
        


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

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
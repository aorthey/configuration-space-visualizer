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
rc('text', usetex=False)
rc('font', family='serif', size=30)

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

pointsize = 20

def readVerticesFromFile(fname):
  fh = open(fname, "r")

  file_string = fh.read()
  file_list = file_string.split('\n')
  q = []

  for line in file_list:
    config = line.split('\t')
    if(len(config)>1):
      qq = config[1].split(' ')
      q.append(qq)
  q = np.array(q)
  return q

def plotCSpacePath(pathX,pathT):
  plt.plot(pathX,pathT,'-k',linewidth=5)
  plt.plot(pathX[0],pathT[0],'ok',markersize=pointsize)
  plt.plot(pathX[-1],pathT[-1],'ok',markersize=pointsize)

def plotCSpaceDelaunay(PX,PT, maximumEdgeLength = 0.25, continuous=True):
  points2D=np.vstack([PX,PT]).T
  tri = Delaunay(points2D)
  print(tri.simplices.shape, '\n', tri.simplices[0])

  triangles = np.array((tri.simplices[0]))
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

  #plt.triplot(PX,PT, triangles, edgecolor='red')#tri.simplices.copy())
  #centers = np.sum(pts[triangles], axis=1, dtype='int')/3.0

  cx = np.sum(PX[triangles],axis=1)/3.0
  ct = np.sum(PT[triangles],axis=1)/3.0

  colors = np.array([ (x-1)**2 for x,y in np.vstack((cx,ct)).T])

  fig = plt.figure(0)
  ax = fig.add_subplot(111)
  plt.tripcolor(PX,PT,triangles, cmap=plt.cm.Spectral_r, facecolors=colors, edgecolors='none')
  plt.xlabel('x')
  fig.autofmt_xdate()
  #plt.ylabel('q',rotation=0)
  # plt.ylabel(r'\theta',rotation=0)
  dxax=0.45
  dyax=0.05
  fig.patch.set_facecolor('white')
  if continuous:
    plt.text(dxax, 0-dyax,r'$\gg$',transform=ax.transAxes, fontsize=50)
    plt.text(dxax, 1-dyax,r'$\gg$',transform=ax.transAxes, fontsize=50)

  ax.tick_params(axis='both', which='major', pad=15)

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

  plotPath(fname1, "red")
  plotPath(fname2, "green")
  plotPath(fname3, "blue")
  Qu = np.array(getPath(fname1))
  
  plt.scatter(Qu[0,0], Qu[0,1], marker = "o", s=20, linewidths = 5, color = "green")
  plt.scatter(Qu[Qu.size//2 - 1,0], Qu[Qu.size//2 - 1,1], marker = "x", s=50, linewidths = 5, color = "red")
  
  zFaces = np.ones(triangles.shape[0])
  cmap = colors.LinearSegmentedColormap.from_list("", [(shade,shade,shade),"grey","grey"])
  plt.tripcolor(P1, P2, triangles, cmap=cmap, facecolors=zFaces,edgecolors='none')
  
def plotPath(fname, colour):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,0]
  p2 = Qu[:,1]
  p1 = p1.astype(float)
  p2 = p2.astype(float)
  #for theta in p2:
    #  theta = math.cos(theta)
  #plt.plot(Qu[:,0], Qu[:,1])
  plt.plot(p1, p2, linewidth=2.5, color= colour)
  
def plotPathCylindrical(fname, colour):
  Qu = np.array(getPath(fname))
  p1 = Qu[:,0]
  pz = Qu[:,1]
  p1 = p1.astype(float)
  pz = pz.astype(float)
  #px = np.ndarray(pz.size)
  #py = np.ndarray(pz.size)
  
  px = np.cos(p1)
  py = np.sin(p1)
  #i = 0
  #for theta in p1:
  #   px[i] = math.cos(theta)
  #   py[i] = math.sin(theta)
  #   i = i + 1
  #plt.plot(Qu[:,0], Qu[:,1])
  plt.plot(px, py, pz, linewidth = 4, color = colour)
  

def plotCSpaceDelaunay3D(fname1,fname2,fname3,P1,P2,maximumEdgeLength=0.25):
  points2D=np.vstack([P1,P2]).T
  tri = Delaunay(points2D)
  # print tri.simplices.shape, '\n', tri.simplices[0]

  fig = plt.figure()
  ax = fig.gca(projection = '3d')
  triangles = np.array((tri.simplices[0]))
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
  
  #Qu = np.array(getPath(fname1))
  #plotCSpacePathCylindricalProjection(Qu[:,1].astype(float), Qu[:,0].astype(float))
  
  #Qu = np.array(getPath(fname2))
  #plotCSpacePathCylindricalProjection(Qu[:,1].astype(float), Qu[:,0].astype(float))
  
  #Qu = np.array(getPath(fname3))
  #plotCSpacePathCylindricalProjection(Qu[:,1].astype(float), Qu[:,0].astype(float))
  
  plotPathCylindrical(fname1, "red")
  plotPathCylindrical(fname2, "green")
  plotPathCylindrical(fname3, "blue")
  plotStartGoal(fname1)

  u = np.linspace(0,3.14,100)
  v = np.linspace(-1.5,1.5,100)
  x = np.cos(u)
  y = np.sin(u)
  z = v
  ax.plot_trisurf(triangles)
  ax.show()
  zFaces = np.ones(triangles.shape[0])
  cmap = colors.LinearSegmentedColormap.from_list("", [(0.8,0.8,0.8),"grey","grey"])
  #plt.tripcolor(P1, P2, triangles, cmap=cmap, facecolors=zFaces,edgecolors='none')
  #plt.tripcolor(P1, P2, triangles, facecolors=zFaces,edgecolors='none')
  
    

def plotStartGoal(fname):
  Qu = np.array(getPath(fname))
  startx = np.cos(Qu[0,0].astype(float))
  starty = np.sin(Qu[0,0].astype(float))
  startz = Qu[0,1].astype(float)
  goalx = np.cos(Qu[Qu.size//2 - 1,0].astype(float))
  goaly = np.sin(Qu[Qu.size//2 - 1,0].astype(float))
  goalz = Qu[Qu.size//2 - 1,1].astype(float)
  #plt.scatter(math.cos(Qu[0,1]), math.sin(Qu[0,1]), Qu[0,0], marker = "o", s=20, linewidths = 5, color = "green")
  #plt.scatter(math.cos(Qu[Qu.size/2 - 1,1]), math.sin(Qu[Qu.size/2 - 1,1]), Qu[Qu.size/2 - 1,0], marker = "x", s=50, linewidths = 5, color = "red")
  plt.plot([startx], [starty], [startz], marker = "o", markersize = pointsize/2, color = "green")
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

def plotCSpacePathCylindricalProjection(pathX,pathT):
  X = np.cos(pathT)
  Y = np.sin(pathT)
  Z = pathX
  plt.plot(X,Y,Z,'-k',linewidth=5)
  #plt.scatter(X[0],Y[0],Z[0],c='k',s=pointsize)
  plt.plot([X[0]], [Y[0]], [Z[0]], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=pointsize/2)
  plt.plot([X[-1]], [Y[-1]], [Z[-1]], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=pointsize/2)
  #plt.scatter(X[-1],Y[-1],Z[-1],s=20,c='k')

def plotCSpaceCylindricalProjection(PX,PT,fname1,fname2,fname3):
  #X = np.cos(PT)
  #Y = np.sin(PT)
  xs, ys, Z = [],[],[]
  for i in range(0,PX.size):
      if PX[i] <= 1.5 and PX[i] >= -1.5 and PX[i] != 1 and PX[i] != -1:
          Z.append(PX[i])
          xs.append(np.cos(PT[i]))
          ys.append(np.sin(PT[i]))

  #print(xs.size,ys.size,Z.size)
  xs, ys, Z = np.asarray(xs),np.asarray(ys),np.asarray(Z)
  rad = np.linalg.norm(xs)
  zen = np.arccos(Z/1.51)
  azi = np.arctan2(ys,xs)

  #rad = 1
  #zen = X
  #azi = Y

  
  tris = mtri.Triangulation(zen, azi)

  mask = long_edges(zen,azi, tris.triangles, 0.2)
  tris.set_mask(mask)

  #print len(tris.triangles)
  #print len(tris.triangles)
  #print len(tris.edges)
  #plt.triplot(tris, 'bo-', lw=1)
  #plt.show()

  fig = plt.figure(1)
  fig.patch.set_facecolor('white')
  ax  = fig.add_subplot(111, projection='3d')
  ax.axis('off')
  
  #plot own axes
  #plt.plot([1,1],[0,0], [-2,2], color = 'black', linewidth = '2')
  ta = np.linspace(np.pi/2,np.pi,50)
  xa = np.cos(ta)
  ya = -np.sin(ta)
  plt.plot(xa,ya,-1.57*np.ones(50), color = 'black', linewidth = '2')
  theta1 = Arrow3D([-1,-1],[0,0],[-1.57,2], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = 'theta1')
  theta1.set_label("theta1")
  #ax.add_artist(theta1)
  theta2 = Arrow3D([-0.01,0.01],[-1,-1],[-1.57,-1.57], color = 'black', linewidth= '2', arrowstyle = "-|>", mutation_scale = 20, label = "theta2")
  ax.add_artist(theta2)
  
  #ax.plot_trisurf(X,Y,Z, \
  #    triangles=tris.get_masked_triangles(),cmap=plt.cm.Spectral, \
  #     linewidth=0, antialiased=False)
  ax.plot_trisurf(xs,ys,Z, \
      triangles=tris.get_masked_triangles(),color = "grey", \
       linewidth=0, antialiased=False)
  
  
  # ax.set_xlabel(r'r')
  # ax.set_ylabel(r'\phi')
  # ax.set_zlabel(r'z')
  
  plotPathCylindrical(fname1, "magenta")
  plotPathCylindrical(fname2, "magenta")
  plotPathCylindrical(fname3, "magenta")
  plotStartGoal(fname1)
  #plotCylinder()
  
  x=np.linspace(-1, 1, 100)
  z=np.linspace(-1.57, 1.57, 100)
  Xc, Zc=np.meshgrid(x, z)
  Yc = np.sqrt(1-Xc**2)

  rstride = 20
  cstride = 10
  ax.plot_wireframe(Xc, Yc, Zc, alpha=0.4, rstride=rstride, cstride=cstride, linestyles = "dashed")
  ax.plot_wireframe(Xc, -Yc, Zc, alpha=0.4, rstride=rstride, cstride=cstride, linestyles = "dashed")

  ax.set_xlabel('')
  ax.set_ylabel('')
  ax.set_zlabel('')
  ax.tick_params(axis='both', which='major', pad=15)


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

  print(t3)

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  ax.scatter(t1, t2, t3, marker='x', color='green')

  # ax.set_xlabel('X')
  # ax.set_ylabel('Y')
  # ax.set_zlabel(r'$\theta$')
  # plt.scatter(t4, t5, t6, marker='o', color='red')
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

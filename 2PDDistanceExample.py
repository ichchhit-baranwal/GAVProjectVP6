import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from HalfMunkres import HalfMunkres
from multiprocessing import pool
import time

def calc_dist(l):
  x = l[0]
  y = l[1]
  z = [y[0],y[1],y[2],round(y[3],5),round(y[4],5),x[0],x[1],x[2],y[5],x[5]]
  return z

"""### geometric_dist(p) = :px,py,pz,pbirth,pdeath """


def calc(points_time):
  time_i =[]
  l = []
  for i in range(len(points_time)):
    # l = []
    if i%2 == 0:
      l.append(points_time[i])
      l.append(points_time[i+1])
      x = calc_dist(l)
      time_i.append(x)
      pairs.append(l)
      l = []
  return time_i


def d_lift_v(p,q,v,coeff):
  d = []

  d.append(abs(p[3] - q[3]))  # dBirth
  d.append(abs(p[4] - q[4]))  # dDeath
  d.append(abs(p[0] - q[0]))  # dx
  d.append(abs(p[1] - q[1]))  # dy
  d.append(abs(p[2] - q[2]))  # dz
  
  val = [i**v for i in d]
  val = [(coeff[i] * val[i]) for i in range(len(val))]
  val = sum(val)
  val = val ** (1/v)
  return val


# diagonal projection distance 
def d_lift_diag_v(p,v,coeff):
  d = []
  
  d.append(abs(p[3]))  # dBirth
  d.append(abs(p[4]))  # dDeath
  d.append(abs(p[0] - p[5]))  # dx
  d.append(abs(p[1] - p[6]))  # dy
  d.append(abs(p[2] - p[7]))  # dz

  val = [i**v for i in d]
  val = [(coeff[i] * val[i]) for i in range(len(val))]
  val = sum(val)
  val = val ** (1/v)
  return val

"""## creating 2d matrix
called via `create_matrix(v,t,t+1)` <br>

* `v` = value parameter of wasserestein formula
* `t` = persistence diagram of timestep t 
* `t+1` = persistence diagram of timestep t+1 
"""

def create_matrix(geometric_dist,v,first,second):
  coeff_max = [0.1,1,1,1,1]
  coeff_min = [1,1,0.1,.1,.1]
  coeff = []
  matrix = []
  for i in range(len(geometric_dist[first])+1):
    l = []
    for j in range(len(geometric_dist[second])+1):
      if i < len(geometric_dist[first]):
        if j == len(geometric_dist[second]):
          l.append(1e9)
          continue
        if geometric_dist[first][i][8] == 3:
          # print("true")
          coeff = coeff_max
        else:
          coeff = coeff_min
        x = d_lift_v(geometric_dist[first][i],geometric_dist[second][j],v,coeff) - d_lift_diag_v(geometric_dist[first][i],v,coeff)
        l.append(x)
      else:
        for j in range(len(geometric_dist[second])+1):
          if j == len(geometric_dist[second]):
            l.append(1e9)
            continue
          else:
            if geometric_dist[second][j][8] == 3:
              coeff = coeff_max
            else:
              coeff = coeff_min
            d_lift_diag_v(geometric_dist[second][j],v,coeff)
    matrix.append(l)
  return np.asarray(matrix)


def runHalfMunkres(mat):
    mun = HalfMunkres()
    mun.setInput(mat.shape[0],mat.shape[1],mat.tolist())
    mun.runHalf()
    M = np.asarray(mun.M)[:-1,:-1]
    return M

if __name__ == "__main__":
#     cost_matrix = np.asarray([[0,0.6990517588680104,0.44944136424030695,0.44812356003077025,0.5923895618380786,0.6810639299777742,1,0.7071068518972327],
#                               [0.4629852034047768,0.2409984257889994,0.18636274158902033,0.25844196244361284,0.25461832767914877,0.3261554146036505,0.7217512712007513,0.24498150826974038],
#                               [0.11848439663039696,0.5814338135671198,0.3346321867602997,0.3408615039597376,0.4776644531490696,0.5666667406832987,0.8996899895364477,0.5925003821848875],
#                               [0.5404672515226532,0.1606160449580717,0.16641585285999422,0.23715708715448358,0.1742939044532183,0.233552386014459,0.6313346896735735,0.17612988598477225],
#                               [0.2865678222449675,0.4249554475631567,0.16649091180232356,0.18640033101257594,0.3090221409404061,0.39810928448090244,0.7460297228970032,0.4404611782761515],
#                               [0.326868336092368,0.3986996051417062,0.12294185194148456,0.1410980075135191,0.2660018911901734,0.35497453465491435,0.7002124850490343,0.41227835725243167],
#                               [0.36585481758672017,0.3674781245734106,0.0838829190915545,0.11020494390457679,0.22693312705456645,0.3159175958048944,0.6648106259113182,0.3782999523977278],
#                               [0.5347972555703674,0.22359281931808095,0.09318837593792177,0.14587990813527307,0.07587595096687916,0.1585160816216442,0.5448795391868503,0.21349017985757854],
#                               [0.40696664924771975,0.39272940644329846,0.08496244866895779,0.04130901008037452,0.20149289780386834,0.28483383879347285,0.599885304720375,0.38154757489090935],
#                               [0.5021301414216127,0.30563295639348925,0.06283229169829811,0.06939580483933828,0.0961139881541946,0.1810393571811471,0.5264464095046784,0.27729670233440784],
#                               [0.5779229048675276,0.2692929313000883,0.13157329494962236,0.14101097567116475,0.02960373008608516,0.10491843671724238,0.4653400721716929,0.20757810262738846],
#                               [0.5875723520820048,0.2811425339025114,0.14417994105254386,0.1458846833825802,0.040948312941841966,0.09985281803445636,0.449480974633552,0.20671866157591046],
#                               [0.7288262084606083,0.2473067436614894,0.2796340397118104,0.29239361823152865,0.1365683096048767,0.047861336339440015,0.3685941295867368,0.06469743138148906],
#                               [0.8770159120691002,0.517802657917606,0.46855112941454546,0.4380746740373182,0.354786057445701,0.292219973601972,0.12319472952704527,0.082212774314889],
#                               [1,0.6054379322043522,0.5891472696383039,0.5609360797744197,0.46901985237167154,0.39781059387336537,0,7.071068518972326e-8],
#                               [0.7071068518972327,0.015517141621053908,0.30666250657719707,0.3464058131944313,0.182425636112346,0.10820747622512995,7.071068518972326e-8,0]
#                             ])

 
    pairs = []
    geometric_dist = []
    path = 'F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_{}.csv'
#     data0 = pd.read_csv('F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_0.csv')
#     data1 = pd.read_csv('F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_1.csv')
#     print(data0.columns)
#     print(data0.max(), data0.min())
#     plt.bar(data0["Points:0"],data0["Points:1"],width=0.001)
#     plt.show()
#     print(data0.head())
#     print(data1.head())
#     points_0 = data0[['Coordinates:0','Coordinates:1','Coordinates:2','Points:0','Points:1','CriticalType']]
#     points_1 = data1[['Coordinates:0','Coordinates:1','Coordinates:2','Points:0','Points:1','CriticalType']]
#     print(points_0.head())
#     points_0 = points_0.values.tolist()
#     points_1 = points_1.values.tolist()
#     print(points_0[0:5])
    #timestep 1
#     dist = calc(points_0)
#     geometric_dist.append(dist)
    # timestep 2
#     dist = calc(points_1)
#     geometric_dist.append(dist)
    output_path = "F:\\MTechCourse\\Graphics And Visualization\\Project\\Matchings\\{}_{}.npy"
    persistence_diagrams = [pd.read_csv(path.format(index))[['Coordinates:0','Coordinates:1','Coordinates:2',\
                                                             'Points:0','Points:1','CriticalType']] for index in range(102)]
    geometric_dist = [calc(pdiag.values.tolist()) for pdiag in persistence_diagrams]
    
    print(len(geometric_dist))
    # distnce metric between persistence pairs p and q
    
#     print(len(points_0), len(points_1))
      
    cost_matrices = [create_matrix(geometric_dist,2,index,index+1) for index in range(len(geometric_dist) - 1)]
#     print("cost_matrix computation completed")
#     p = pool.Pool(processes=4)
#     matchings = p.map(runHalfMunkres,cost_matrices)
#     p.close()
#     p.join()
#     print(len(matchings))   
    
    for index in range(24):
        st_time = time.time()
        runHalfMunkres(cost_matrices[index])
        print("step :: {} time taken :: {}".format(index, time.time()-st_time))
     
#     cost_mat = create_matrix(geometric_dist,2,0,1)
#     M = runHalfMunkres(cost_mat)
#     for index in range(len(matchings)):
#         np.save(output_path.format(index, index + 1), matchings[index])
#     print(len(geometric_dist[0]),len(geometric_dist[1]), cost_matrix.shape, M.shape) 
#     plt.imshow(M, cmap="gray")
#     plt.tight_layout()
#     plt.show()
    #942, 285

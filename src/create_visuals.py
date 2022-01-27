'''
Created on 07-Dec-2021

@author: ichch
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
from skimage.measure import marching_cubes_lewiner
import pyvista as pv
import geopandas as gpd
from shapely.geometry import Point, LineString

def write_vtk(lineDf,file_name=None):
    #create emtpy dict to store the partial unstructure grids
    lineTubes = {}
    
    #iterate over the points


    #iterate over the points
    for index, values in lineDf.iterrows():
        coords = np.asarray(list(values.geometry.coords))
#         print(coords)
#         exit()
#         cellSec = []
#         linePointSec = []
#      
#         #iterate over the geometry coords
#         zipObject = list(values.geometry.coords)
#         for linePoint in zipObject:
#             linePointSec.append([linePoint[0],linePoint[1],linePoint[2]])
#      
#         #get the number of vertex from the line and create the cell sequence
#         nPoints = len(list(lineDf.loc[index].geometry.coords))
#         cellSec = [nPoints] + [i for i in range(nPoints)]
#      
#         #convert list to numpy arrays
#         cellSecArray = np.array(cellSec)
#         cellTypeArray = np.array([4])
#         linePointArray = np.array(linePointSec)
#      
#         partialLineUgrid = pv.UnstructuredGrid(cellSecArray,cellTypeArray,linePointArray)
        direction = coords[1] - coords[0]
        mag = np.linalg.norm(direction)
        if mag == 0:
            mag = 1
        direction/=mag 
        partialLineUgrid =  pv.Cylinder(center=(coords[1] + coords[0])/2, direction=direction,\
                                                 height=mag, radius =values.radius)#0.25
#         #we can add some values to the point
        partialLineUgrid.cell_data["data"] = values.label
        lineTubes[str(index)] = partialLineUgrid
    
    #merge all tubes and export resulting vtk
    lineBlocks = pv.MultiBlock(lineTubes)
    lineGrid = lineBlocks.combine()
    lineGrid.plot()
#     lineGrid.save(file_name,binary=False)


diag_1= 0
diag_2= 1
tbl_0 = pd.read_csv("F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_{}.csv".format(diag_1))
tbl_1 = pd.read_csv("F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_{}.csv".format(diag_2))
matching = np.load(r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\{}_{}.npy".format(diag_1,diag_2))
print(tbl_0.columns)
print(tbl_1.columns)
print(matching.shape)
fig = plt.figure(figsize=(16,16))
# fig2 = plt.figure(figsize=(16,16))
ax = fig.gca(projection="3d")
# ax2 = fig2.gca(projection="3d")
# fig3 = plt.figure(figsize=(16,16))
# ax3 = fig3.gca(projection="3d")
# fig1 = plt.figure(figsize=(16,8))
# ax2 = fig1.gca(projection="3d")
print(tbl_0.shape[0])

timestep_distabce =1
radius_diag=0.025
radius_match=0.025
persistant_matching_lines = []
radius = []

for index in range(0,tbl_0.shape[0],2):
    ax.plot([8+diag_1*40,8+diag_1*40],tbl_0["Points:0"][index:index+2],\
             tbl_0["Points:1"][index:index+2], linewidth=5, marker="o")
    
    
    persistant_matching_lines.append(zip([8+diag_1*timestep_distabce,8+diag_1*timestep_distabce],tbl_0["Points:0"][index:index+2],\
             tbl_0["Points:1"][index:index+2]))
    radius.append(radius_diag)

# print(tbl_0["Points:0"].iloc[[0,-2]])
ax.plot([8+diag_1*40,8+diag_1*40],tbl_0["Points:0"].iloc[[0,-2]], tbl_0["Points:1"].iloc[[0,-2]])



persistant_matching_lines.append(zip([8+diag_1*timestep_distabce,8+diag_1*timestep_distabce],tbl_0["Points:0"].iloc[[0,-2]],\
             tbl_0["Points:1"].iloc[[0,-2]]))
radius.append(radius_diag)
labels = [0] * len(persistant_matching_lines)


for index in range(0,tbl_1.shape[0],2):
    ax.plot([8+diag_2*40,8+diag_2*40],tbl_1["Points:0"][index:index+2],\
             tbl_1["Points:1"][index:index+2],linewidth = 5, marker="o")
    
    
    
    persistant_matching_lines.append(zip([8+diag_2*timestep_distabce,8+diag_2*timestep_distabce],tbl_1["Points:0"][index:index+2],\
             tbl_1["Points:1"][index:index+2]))
    radius.append(radius_diag)

ax.plot([8+diag_2*40,8+diag_2*40],tbl_1["Points:0"].iloc[[0,-2]], tbl_1["Points:1"].iloc[[0,-2]])    


persistant_matching_lines.append(zip([8+diag_2*timestep_distabce,8+diag_2*timestep_distabce],tbl_1["Points:0"].iloc[[0,-2]],\
             tbl_1["Points:1"].iloc[[0,-2]])) 
radius.append(radius_diag)
labels.extend([1]*(len(persistant_matching_lines) - len(labels)))

match_indices  = np.where(matching==1)
lines = []
threshold = 0.1
for row,col in list(zip(match_indices[0],match_indices[1])):
    distance_1 =   np.sqrt((tbl_0["Points:0"][(row*2)+1]-tbl_0["Points:0"][(row*2)])**2 +\
                            (tbl_0["Points:1"][(row*2)+1]-tbl_0["Points:1"][(row*2)])**2)
    distance_2 =   np.sqrt((tbl_1["Points:0"][(col*2)+1]-tbl_1["Points:0"][(col*2)])**2 +\
                            (tbl_1["Points:1"][(col*2)+1]-tbl_1["Points:1"][(col*2)])**2)
#     print(distance_1, distance_2)  
    if distance_1 >= threshold or distance_2 >=threshold:
        ax.plot([8+diag_1*40,8+diag_2*40],[tbl_0["Points:0"][(row*2)+1],tbl_1["Points:0"][(col*2)+1]],\
                [tbl_0["Points:1"][(row*2)+1],tbl_1["Points:1"][(col*2)+1]],\
                color="blue")
        
#         
        persistant_matching_lines.append(zip([8+diag_1*timestep_distabce,8+diag_2*timestep_distabce],[tbl_0["Points:0"][(row*2)+1],tbl_1["Points:0"][(col*2)+1]],\
                [tbl_0["Points:1"][(row*2)+1],tbl_1["Points:1"][(col*2)+1]]))
        radius.append(radius_match) 


#     clr = (np.random.random_sample(),np.random.random_sample(),np.random.random_sample())
    xs = np.ravel([tbl_0["Coordinates:0"][row*2+1],tbl_1["Coordinates:0"][2*col+1]])
    ys = np.ravel([tbl_0["Coordinates:1"][row*2+1]+10*diag_1,tbl_1["Coordinates:1"][2*col+1]+10*diag_2])
    zs = np.ravel([tbl_0["Coordinates:2"][row*2+1],tbl_1["Coordinates:2"][2*col+1]])
    lines.append(list(zip(xs,ys,zs)))
#     ax2.plot(xs,ys,zs, marker="o")
# lineDf = gpd.GeoDataFrame(geometry=[LineString(line) for line in lines])
labels.extend([2]*(len(persistant_matching_lines) - len(labels)))
lineDf = gpd.GeoDataFrame(geometry=[LineString(line) for line in persistant_matching_lines])
lineDf["radius"] = radius
lineDf["label"] = labels
# write_vtk(lineDf, file_name=r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\{}_{}.vtk".format(diag_1,diag_2))
write_vtk(lineDf)#, file_name=r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\{}_{}_line.vtk".format(diag_1,diag_2))
plt.grid()
ax.set_xlabel("time step")
ax.set_ylabel("Birth")
ax.set_zlabel("Birth-Death")
plt.title("Matching Pairs between step {} and {}".format(diag_1, diag_2))
plt.tight_layout()
# plt.show()


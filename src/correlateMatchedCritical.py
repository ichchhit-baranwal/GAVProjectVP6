'''
Created on 08-Dec-2021

@author: ichch
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv
import geopandas as gpd
from shapely.geometry import Point, LineString


def write_vtk(pointDf, path):
    #create emtpy dict to store the partial unstructure grids
    #iterate over the points
    lineTubes = {}
    labels = []
    for index, valuesx in pointDf.iterrows():
        coords = np.asarray(list(*valuesx.geometry.coords))
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
#         cellSec = [1,index]
#     
#         #convert list to numpy arrays
#         cellSecArray = np.array(cellSec)
#         cellTypeArray = np.array([1])
#         linePointArray = np.array([list(coords)])
#     
#         partialLineUgrid = pv.UnstructuredGrid(cellSecArray,cellTypeArray,linePointArray)   
#         #we can add some values to the point
#         partialLineUgrid.cell_data["data"] = 5
        direction = np.asarray(valuesx.data_val)
        mag = np.linalg.norm(direction)
        if mag > 0:
            direction = direction/mag
            lineTubes[str(index)] = pv.Cylinder(center=coords+mag*0.5*direction, direction=direction,\
                                                 height=mag, radius = 0.1)
            lineTubes[str(index)]["labels"] = np.asarray([valuesx.labels]*lineTubes[str(index)].number_of_cells)
#             labels.append(valuesx.labels)
    
    #merge all tubes and export resulting vtk
    lineBlocks = pv.MultiBlock(lineTubes)
    lineGrid = lineBlocks.combine()
#     lineGrid["labels"] = labels
    lineGrid.plot()
    lineGrid.save(path,binary=False)

def write_vtk_b1(pointDf, path):
    #create emtpy lists to collect point information
    cellSec = []
    cellTypeSec = []
    pointSec = []
    
    #iterate over the points
    i = 0
    data_values = []
    labels = []
    for index, valuesx in pointDf.iterrows():
        coords = list(*valuesx.geometry.coords)

        if (not (np.isnan(coords[0]) or  np.isnan(coords[1]) or np.isnan(coords[2])) ) and  np.sum(np.asarray(valuesx.data_val)**2) > 0:
            pointSec.append(coords)
            cellTypeSec.append([1])
            cellSec.append([1,i])
            data_values.append(valuesx.data_val)
            labels.append(valuesx.labels)
            i+=1
    #convert list to numpy arrays
    cellArray = np.array(cellSec)
    cellTypeArray = np.array(cellTypeSec)
    pointArray = np.array(pointSec)
    
    #create the unstructured grid object
    pointUgrid = pv.UnstructuredGrid(cellArray,cellTypeArray,pointArray)
    
    #we can add some values to the point
    
    data_values = np.asarray(data_values) 
    pointUgrid.cell_data["labels"] = labels
    pointUgrid.cell_data["data_val"] = np.linalg.norm(data_values, axis=1)
    pointUgrid.cell_data["data_val"][pointUgrid.cell_data["data_val"] == 0] = 1
    pointUgrid.cell_data["vectors"] = data_values / pointUgrid.cell_data["data_val"].reshape(-1,1) 
    print(np.linalg.norm(pointUgrid.cell_data["vectors"], axis=1))
#     pointUgrid.set_active_vectors("data_val")
    pointUgrid = pointUgrid.glyph(scale = "data_val", orient = "vectors")
    
    #plot and save as vtk
#     print(pointUgrid.arrows)
    pointUgrid.arrows.plot()
    pointUgrid.arrows.save(path,binary=False)
    
    
def write_vector_vtk(pointDf, path):
    #create emtpy lists to collect point information
    cellSec = []
    cellTypeSec = []
    pointSec = []
     
    #iterate over the points
    i = 0
    data_values = []
    for index, valuesx in pointDf.iterrows():
        coords = list(*valuesx.geometry.coords)
 
        if not (np.isnan(coords[0]) or  np.isnan(coords[1]) or np.isnan(coords[2])):
            pointSec.append(coords)
            cellTypeSec.append([1])
            cellSec.append([1,i])
            data_values.append(valuesx.data_val)
            i+=1
    #convert list to numpy arrays
    cellArray = np.array(cellSec)
    cellTypeArray = np.array(cellTypeSec)
    pointArray = np.array(pointSec)
     
    #create the unstructured grid object
    pointUgrid = pv.UnstructuredGrid(cellArray,cellTypeArray,pointArray)
     
    #we can add some values to the point
    pointUgrid.cell_data["vector_val"] = data_values
     
    #plot and save as vtk
#     pointUgrid.plot()
    pointUgrid.save(path,binary=False)
    
pth = "F:\\MTechCourse\\Graphics And Visualization\\Project\\extracted persistence diag\\persistence diag_{}.csv"
# tbl_0 = pd.read_csv(pth.format(0))
# dict_acc = {}
# dict_root = {}
print("start")
matchings = [np.load(r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\{}_{}.npy".format(step-1,step))\
              for step in  range(1,102)]

print("loading completed")
max_crit = np.max([matching.shape[0] for matching in matchings])

correlates_ = -1*np.ones(shape=(max_crit,102), dtype=np.int32)

correlates_[0:matchings[0].shape[0],0] = np.arange(matchings[0].shape[0])

for step in range(1,102):
#     print(matchings[step-1].shape)
    match_indices = [np.where(matchings[step-1][index] == 1)[0] if index > -1 else np.asarray([]) for index in correlates_[:,step-1]]
    match_indices = [index[0] if index.shape[0] > 0 else -1 for index in match_indices]
    max_index = np.max(match_indices)
#     print(len(match_indices))
#     extra_indices = np.arange(max_index+1, matchings[step].shape[0])
#     match_indices.extend(extra_indices)
#     print(matchings[step-1].shape,len(match_indices))
    correlates_[0:len(match_indices),step] = match_indices

print("Constructing correlation completed")
# 
# for step in range(102):
#     tbl = pd.read_csv(pth.format(step))
#     indices = correlates_[:,step]
#     coords_ = [tuple(tbl.iloc[row*2][["Coordinates:0","Coordinates:1","Coordinates:2"]]) if row>=0 else (np.nan,np.nan,np.nan)  for row in indices]
#     coords_df = gpd.GeoDataFrame(geometry = [Point(*coord) for coord in coords_])
#     coords_df["data_val"] = np.arange(len(coords_))
#     write_vector_vtk(coords_df, r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\colored_coords_{}.vtk".format(step))
#     print(coords_)

# print("Writing colored coords completed")
# exit()    
distance_data = []
distance_coords = []
for index in range(correlates_.shape[0]):
    #     tbl = 
    coords_ = [tuple(pd.read_csv(pth.format(step)).iloc[correlates_[index,step]*2 + 1][["Coordinates:0","Coordinates:1","Coordinates:2"]])\
                if correlates_[index,step]>=0 else (np.nan,np.nan,np.nan)  for step  in range(correlates_[index].shape[0])]
    point_1 = coords_[0]
    distance_points =  [np.sqrt((point_1[0]-matched_point[0])**2 + (point_1[1]-matched_point[1])**2 + (point_1[2]-matched_point[2])**2)\
                        for matched_point in coords_]
    max_distance_index = np.nanargmax(distance_points)
    if distance_points[max_distance_index] > 0:
#         print(point_1, distance_points[max_distance_index], max_distance_index, np.nanmin(distance_points))
        distance_data.append(distance_points[max_distance_index])
        distance_coords.append(Point(point_1))
        
# for point_ in distance_coords:
#     print(point_)


max_distance_index = np.argsort(distance_data)
for index in max_distance_index[-5:]:
#     print(index)
    print(distance_data[index], tuple(distance_coords[index].coords))


max_five_coords = []
max_five_as_vectors = []
vector_labels = []
label = 0
for index in max_distance_index[-1::-1]:
    coords_ = []
    vectors_ = []
    for step  in range(correlates_[index].shape[0]):
        if correlates_[index,step]>=0:
            coords_.append(tuple(pd.read_csv(pth.format(step)).\
                                 iloc[correlates_[index,step]*2 + 1][["Coordinates:0","Coordinates:1","Coordinates:2"]]))
        else:
            coords_.append(coords_[-1])
        vector_labels.append(label)    
        if step > 0:
#             print(step, correlates_[index,step],coords_[-1],coords_[-2])
            vectors_.append(tuple([coords_[-1][0] - coords_[-2][0],coords_[-1][1] - coords_[-2][1],coords_[-1][2] - coords_[-2][2]]))
    label+=1
#     print()
    vectors_.append(tuple([0,0,0]))
    max_five_coords.extend(coords_)
    max_five_as_vectors.extend(vectors_)
# print(max_five_as_vectors[:-5])
point_df = gpd.GeoDataFrame(geometry=[Point(point_) for point_ in max_five_coords])
point_df["data_val"] = max_five_as_vectors
point_df["labels"] = vector_labels
write_vtk(point_df,r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\distance_vectors.vtk" )  

# print(scala)
# for step in range(1,102):
#     tbl_1 = pd.read_csv(pth.format(step))
#     matching = np.load(r"F:\MTechCourse\Graphics And Visualization\Project\Matchings\{}_{}.npy".format(step-1,step)) 
#     match_indices  = np.where(matching==1)
#     for row,col in list(zip(match_indices[0],match_indices[1])):
#         birth_1 = tuple(tbl_0.iloc[row*2][["Coordinates:0","Coordinates:1","Coordinates:2"]])
#         death_1 = tuple(tbl_0.iloc[row*2+1][["Coordinates:0","Coordinates:1","Coordinates:2"]])
#         coords_1 = tuple([birth_1, death_1])
#         birth_2 = tuple(tbl_1.iloc[col*2][["Coordinates:0","Coordinates:1","Coordinates:2"]])
#         death_2 = tuple(tbl_1.iloc[col*2+1][["Coordinates:0","Coordinates:1","Coordinates:2"]])
#         coords_2 = tuple([birth_2, death_2])
#         try:
#             root_coords = dict_root[coords_1]
#             dict_acc[root_coords].append(coords_2)
#             dict_root[coords_2] = root_coords
#         except KeyError:
# #             print(step, step-1, row)
#             pass
#     tbl_0=tbl_1
# for root in dict_acc:
#     print(len(dict_acc[root]))        
    

     
                
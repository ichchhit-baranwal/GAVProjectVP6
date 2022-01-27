import numpy as np
import re
import os
def extract_vector_data(file_name):
    b_data = None
    with open(file_name,"rb") as f : 
        b_data = f.read()
    # print(len(b_data))
    data = "".join(map(chr,b_data))
    # print(len(data))
    if (data.find("# AmiraMesh BINARY-LITTLE-ENDIAN 2.1") < 0):
        print("Not a proper AmiraMesh file.\n");
        exit(1)
    lattice_index = data.find("define Lattice") + len("define Lattice") + 1
    end_index = data.find('\n',lattice_index)
    # print(data[lattice_index:2048])
    xDim, yDim,zDim = map(int,data[lattice_index:end_index].split())
    # print(xDim,yDim,zDim)
    bounding_index = data.find("BoundingBox") + len("BoundingBox") + 1
    end_index = data.find(',\n',bounding_index)
    xmin, xmax,ymin,ymax,zmin,zmax = map(float,data[bounding_index:end_index].split())
    # print(xmin,xmax,ymin,ymax,zmin,zmax)
    
    coordtype_index = data.find("CoordType") + len("CoordType") + 1
    end_index = data.find('\n',coordtype_index)
    is_uniform = data[coordtype_index:end_index] == '"uniform"'
    # print("is Uniform ", is_uniform)
    num_components = 1
    lattice_float_index = data.find("Lattice { float", end_index) + len("Lattice { float")
    if(data[lattice_float_index] == "["):
        lattice_float_index += 1
        end_index = data.find("]", lattice_float_index)
        num_components = int(data[lattice_float_index:end_index])
    
    # print(num_components)
    
    if (xDim <= 0 or yDim <= 0 or zDim <= 0
        or xmin > xmax or ymin > ymax or zmin > zmax
        or not is_uniform or num_components <= 0):
        print("Something went wrong\n")
        exit(1)
    index_start_data = data.find("Data section follows\n@1\n")+len("Data section follows\n@1\n")
    # regex = re.compile("{}*".format(chr(b'\x00'[0])))
    # result = regex.search(data)
    # print(result.group(1))
    data = data[index_start_data:]
    data_len = num_components*xDim*yDim*zDim*4
    # print(b_data[index_start_data:index_start_data+4096])
    actual_data = np.frombuffer(b_data[index_start_data:index_start_data+data_len], dtype="float32")
    # print(actual_data.shape, actual_data.dtype)
    actual_data = actual_data.reshape(xDim,yDim,zDim,num_components)
    mag_data = np.linalg.norm(actual_data,axis=3)
    flat_max=mag_data.argmax()
    max_index = np.unravel_index(flat_max, mag_data.shape)
    print(flat_max, max_index, mag_data[max_index], actual_data[max_index])
    # for index_i in range(actual_data.shape[0]):
        # print(actual_data[index_i])
        
    # print(mag_data.shape)
    return actual_data,xDim,yDim,zDim, (xmin,xmax,ymin,ymax,zmin,zmax)
    
    
    
if __name__ == "__main__":
    dir = "../Data/SquareCylinder/"
    out_dir = "../Data/VectorOutput/"
    file_list_file = dir + os.sep + "SquareCylinder.fileseries"
    input_list = []
    with open(file_list_file) as f:
        input_list = f.read()
        input_list = input_list.split("\n")
    # print(input_list)
    file_list = [fname.strip() for fname in input_list if fname.strip().endswith(".am")]
    with open(out_dir+os.sep+"FileList.txt","w") as file_:
        for fle in file_list:
            print(fle)
            data, xDim,yDim,zDim, bounds = extract_vector_data(dir+os.sep+fle)
            fle_name = fle.split(".am")[0] +".raw".format(xDim,yDim,zDim) 
            data.tofile(out_dir+os.sep+fle_name)
            file_.writelines(fle_name + os.linesep)
    with open(out_dir+os.sep+"MetaData.txt","w") as file_:
        file_.writelines("x_bounds=({},{})".format(bounds[0],bounds[1]) + os.linesep ) 
        file_.writelines("y_bounds=({},{})".format(bounds[2],bounds[3])+ os.linesep) 
        file_.writelines("z_bounds=({},{})".format(bounds[4],bounds[5])+ os.linesep)
        file_.writelines("dim=({}x{}x{})".format(xDim,yDim,zDim)+ os.linesep)
        file_.writelines("dtype=float"+ os.linesep)
        
    # extract_vector_data(file_name)
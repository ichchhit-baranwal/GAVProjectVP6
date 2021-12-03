#include <stdio.h>
#include <string.h>
#include <math.h>
#include <assert.h>




char * d[102]={"flow_t0008.am","flow_t0048.am","flow_t0088.am","flow_t0128.am","flow_t0168.am","flow_t0208.am","flow_t0248.am","flow_t0288.am","flow_t0328.am","flow_t0368.am","flow_t0408.am","flow_t0448.am","flow_t0488.am","flow_t0528.am","flow_t0568.am","flow_t0608.am","flow_t0648.am","flow_t0688.am","flow_t0728.am","flow_t0768.am","flow_t0808.am","flow_t0848.am","flow_t0888.am","flow_t0928.am","flow_t0968.am","flow_t1008.am","flow_t1048.am","flow_t1088.am","flow_t1128.am","flow_t1168.am","flow_t1208.am","flow_t1248.am","flow_t1288.am","flow_t1328.am","flow_t1368.am","flow_t1408.am","flow_t1448.am","flow_t1488.am","flow_t1528.am","flow_t1568.am","flow_t1608.am","flow_t1648.am","flow_t1688.am","flow_t1728.am","flow_t1768.am","flow_t1808.am","flow_t1848.am","flow_t1888.am","flow_t1928.am","flow_t1968.am","flow_t2008.am","flow_t2048.am","flow_t2088.am","flow_t2128.am","flow_t2168.am","flow_t2208.am","flow_t2248.am","flow_t2288.am","flow_t2328.am","flow_t2368.am","flow_t2408.am","flow_t2448.am","flow_t2488.am","flow_t2528.am","flow_t2568.am","flow_t2608.am","flow_t2648.am","flow_t2688.am","flow_t2728.am","flow_t2768.am","flow_t2808.am","flow_t2848.am","flow_t2888.am","flow_t2928.am","flow_t2968.am","flow_t3008.am","flow_t3048.am","flow_t3088.am","flow_t3128.am","flow_t3168.am","flow_t3208.am","flow_t3248.am","flow_t3288.am","flow_t3328.am","flow_t3368.am","flow_t3408.am","flow_t3448.am","flow_t3488.am","flow_t3528.am","flow_t3568.am","flow_t3608.am","flow_t3648.am","flow_t3688.am","flow_t3728.am","flow_t3768.am","flow_t3808.am","flow_t3848.am","flow_t3888.am","flow_t3928.am","flow_t3968.am","flow_t4008.am","flow_t4048.am"};
char * e[102] = {"timestep1.vtk","timestep2.vtk","timestep3.vtk","timestep4.vtk","timestep5.vtk","timestep6.vtk","timestep7.vtk","timestep8.vtk","timestep9.vtk","timestep10.vtk","timestep11.vtk","timestep12.vtk","timestep13.vtk","timestep14.vtk","timestep15.vtk","timestep16.vtk","timestep17.vtk","timestep18.vtk","timestep19.vtk","timestep20.vtk","timestep21.vtk","timestep22.vtk","timestep23.vtk","timestep24.vtk","timestep25.vtk","timestep26.vtk","timestep27.vtk","timestep28.vtk","timestep29.vtk","timestep30.vtk","timestep31.vtk","timestep32.vtk","timestep33.vtk","timestep34.vtk","timestep35.vtk","timestep36.vtk","timestep37.vtk","timestep38.vtk","timestep39.vtk","timestep40.vtk","timestep41.vtk","timestep42.vtk","timestep43.vtk","timestep44.vtk","timestep45.vtk","timestep46.vtk","timestep47.vtk","timestep48.vtk","timestep49.vtk","timestep50.vtk","timestep51.vtk","timestep52.vtk","timestep53.vtk","timestep54.vtk","timestep55.vtk","timestep56.vtk","timestep57.vtk","timestep58.vtk","timestep59.vtk","timestep60.vtk","timestep61.vtk","timestep62.vtk","timestep63.vtk","timestep64.vtk","timestep65.vtk","timestep66.vtk","timestep67.vtk","timestep68.vtk","timestep69.vtk","timestep70.vtk","timestep71.vtk","timestep72.vtk","timestep73.vtk","timestep74.vtk","timestep75.vtk","timestep76.vtk","timestep77.vtk","timestep78.vtk","timestep79.vtk","timestep80.vtk","timestep81.vtk","timestep82.vtk","timestep83.vtk","timestep84.vtk","timestep85.vtk","timestep86.vtk","timestep87.vtk","timestep88.vtk","timestep89.vtk","timestep90.vtk","timestep91.vtk","timestep92.vtk","timestep93.vtk","timestep94.vtk","timestep95.vtk","timestep96.vtk","timestep97.vtk","timestep98.vtk","timestep99.vtk","timestep100.vtk","timestep101.vtk","timestep102.vtk"};


/** Find a string in the given buffer and return a pointer
    to the contents directly behind the SearchString.
    If not found, return the buffer. A subsequent sscanf()
    will fail then, but at least we return a decent pointer.
*/
const char* FindAndJump(const char* buffer, const char* SearchString)
{
    const char* FoundLoc = strstr(buffer, SearchString);
    if (FoundLoc) return FoundLoc + strlen(SearchString);
    return buffer;
}


/** A simple routine to read an AmiraMesh file
    that defines a scalar/vector field on a uniform grid.
*/
int main()
{
    //int counting = 40;
    char  *name = "flow_t";
    char * txt = ".txt";
    char  *am = ".am";
    for (int counting = 0;counting < 102; counting = counting + 1)
    {
    //int x = countnum(counting);
    //const char* FileName = "testscalar.am";
    const char* FileName = d[counting];
    //const char* FileName = "testvector2c.am";
    const char * fwri = e[counting];
    FILE* fp = fopen(FileName, "rb");
    FILE* fw = fopen(fwri,"w");
    if (!fp)
    {
        printf("Could not find %s\n", FileName);
        return 1;
    }
    fprintf(fw,"# vtk DataFile Version 4.2\nvtk output\nASCII\nDATASET STRUCTURED_POINTS\nDIMENSIONS 192 64 48\nSPACING 0.1667 0.125 0.125\n");
    fprintf(fw,"ORIGIN -12 -4 0\nPOINT_DATA 589824\nFIELD FieldData 1\nzos 1 589824 double\n");
    printf("Reading %s\n", FileName);

    //We read the first 2k bytes into memory to parse the header.
    //The fixed buffer size looks a bit like a hack, and it is one, but it gets the job done.
    char buffer[2048];
    fread(buffer, sizeof(char), 2047, fp);
    buffer[2047] = '\0'; //The following string routines prefer null-terminated strings

    if (!strstr(buffer, "# AmiraMesh BINARY-LITTLE-ENDIAN 2.1"))
    {
        printf("Not a proper AmiraMesh file.\n");
        fclose(fp);
        return 1;
    }

    //Find the Lattice definition, i.e., the dimensions of the uniform grid
    int xDim(0), yDim(0), zDim(0);
    sscanf(FindAndJump(buffer, "define Lattice"), "%d %d %d", &xDim, &yDim, &zDim);
    printf("\tGrid Dimensions: %d %d %d\n", xDim, yDim, zDim);

    //Find the BoundingBox
    float xmin(1.0f), ymin(1.0f), zmin(1.0f);
    float xmax(-1.0f), ymax(-1.0f), zmax(-1.0f);
    sscanf(FindAndJump(buffer, "BoundingBox"), "%g %g %g %g %g %g", &xmin, &xmax, &ymin, &ymax, &zmin, &zmax);
   /* printf("\tBoundingBox in x-Direction: [%g ... %g]\n", xmin, xmax);
    printf("\tBoundingBox in y-Direction: [%g ... %g]\n", ymin, ymax);
    printf("\tBoundingBox in z-Direction: [%g ... %g]\n", zmin, zmax);
*/
    //Is it a uniform grid? We need this only for the sanity check below.
    const bool bIsUniform = (strstr(buffer, "CoordType \"uniform\"") != NULL);
    //printf("\tGridType: %s\n", bIsUniform ? "uniform" : "UNKNOWN");

    //Type of the field: scalar, vector
    int NumComponents(0);
    if (strstr(buffer, "Lattice { float Data }"))
    {
        //Scalar field
        NumComponents = 1;
    }
    else
    {
        //A field with more than one component, i.e., a vector field
        sscanf(FindAndJump(buffer, "Lattice { float["), "%d", &NumComponents);
    }
   // printf("\tNumber of Components: %d\n", NumComponents);

    //Sanity check
    if (xDim <= 0 || yDim <= 0 || zDim <= 0
        || xmin > xmax || ymin > ymax || zmin > zmax
        || !bIsUniform || NumComponents <= 0)
    {
        printf("Something went wrong\n");
        fclose(fp);
        return 1;
    }

    //Find the beginning of the data section
    const long idxStartData = strstr(buffer, "# Data section follows") - buffer;
    if (idxStartData > 0)
    {
        //Set the file pointer to the beginning of "# Data section follows"
        fseek(fp, idxStartData, SEEK_SET);
        //Consume this line, which is "# Data section follows"
        fgets(buffer, 2047, fp);
        //Consume the next line, which is "@1"
        fgets(buffer, 2047, fp);

        //Read the data
        // - how much to read
        const size_t NumToRead = xDim * yDim * zDim * NumComponents;
        // - prepare memory; use malloc() if you're using pure C
        float* pData = new float[NumToRead];
        if (pData)
        {
            // - do it
            const size_t ActRead = fread((void*)pData, sizeof(float), NumToRead, fp);
            // - ok?
            if (NumToRead != ActRead)
            {
                printf("Something went wrong while reading the binary data section.\nPremature end of file?\n");
                delete[] pData;
                fclose(fp);
                return 1;
            }

            //Test: Print all data values
            //Note: Data runs x-fastest, i.e., the loop over the x-axis is the innermost
            //printf("\nPrinting all values in the same order in which they are in memory:\n");
            int Idx(0);
            int cnt = 0;
            for(int k=0;k<zDim;k++)
            {
                for(int j=0;j<yDim;j++)
                {
                    for(int i=0;i<xDim;i++)
                    {
                        //Note: Random access to the value (of the first component) of the grid point (i,j,k):
                        // pData[((k * yDim + j) * xDim + i) * NumComponents]
                        assert(pData[((k * yDim + j) * xDim + i) * NumComponents] == pData[Idx * NumComponents]);
                        long double ll = 0;
                        for(int c=0;c<NumComponents;c++)
                        {
                            long double aa = pData[Idx * NumComponents + c];
                            //printf("%g ", pData[Idx * NumComponents + c]);
                            ll += aa*aa;
                            //fprintf(fw,"%.14llf ",aa );
                        }
                        ll= sqrt(ll);
                        fprintf(fw,"%llf\n",ll);
                        cnt++;
                        //printf("\n");
                        Idx++;
                    }
                }
            }
            printf("count %d",cnt);
            //cout<<"count->"<<cnt<<"\n"
            delete[] pData;
        }
    }
    fprintf(fw,"METADATA\nINFORMATION 0");
    fclose(fp);
    fclose(fw);
    }
    printf("done\n");
    return 0;
}

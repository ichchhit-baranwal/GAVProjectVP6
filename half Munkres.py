import math

def iszero(t):
    return t==0

matchings = []
globalstep = 1
iter = 0
done = False
rowsize = 0
colsize = 0
C = []
M = []
rowCover = []
colCover = []
path = []
createdZeros = []
rowLimitsMinus = []
rowLimitsPlus = []
colLimitsMinus = []
colLimitsPlus = []
pathRow0 = 0
pathCol0 = 0
pathCount = 0

def setInput(s1,s2,costMatrix):
    global iter,rowsize,colsize,globalstep,done,C,M,rowCover,rowLimitsMinus,rowLimitsPlus,colCover
    global colLimitsMinus,colLimitsPlus,path,createdZeros,pathRow0,pathCol0
    
    iter = 0
    globalstep = 1
    done = False

    rowsize = s1
    colsize = s2
    C = []
    M = []
    rowCover = []
    colCover = []
    path = []
    createdZeros = []
    rowLimitsMinus = []
    rowLimitsPlus = []
    colLimitsMinus = []
    colLimitsPlus = []

    nbpaths = 1 + colsize + rowsize
    for i in range(nbpaths):
        path.append([0,0])
    
    for i in range(rowsize):
        M.append([])
        C.append([])
        for j in range(colsize):
            M[i].append(0)
            C[i].append(costMatrix[i][j])
    
    for i in range(rowsize):
        rowLimitsPlus.append(0)
        rowLimitsMinus.append(0)
        rowCover.append(False)
    
    for j in range(colsize):
        colLimitsMinus.append(0)
        colLimitsPlus.append(0)
        colCover.append(False)

def runHalf(matchings):
    global iter,done,globalstep
    step = globalstep
    maxiter = 5000
    while(done == False):
        # print(C)
        iter += 1
        if iter > maxiter:
            step = 7
        
        if step == 1:
            step = stepOne(step)
        elif step == 2:
            step = stepTwo(step)
        elif step == 3:
            step = stepThree(step)
        elif step == 4:
            step = stepFour(step)
        elif step == 5:
            step = stepFive(step)
        elif step == 6:
            step = stepSix(step)
        elif step == 7:
            step = stepSeven(step)
            done = True

    globalstep = step

    return 0

# Preprocess cost matrix
def stepOne(step):
    minInCol = 1e9 + 7
    maxVal = 1e9+7

    for r in range(rowsize - 1):
        rowLimitsPlus[r] = -1
        rowLimitsMinus[r] = -1
    
    for c in range(colsize - 1):
        colLimitsMinus[c] = -1
        colLimitsPlus[c] = -1
    
    dropMinus = 0
    dropPlus = 0

    for r in range(rowsize -1):
        for c in range(colsize - 1):
            if C[r][c] != maxVal:
                rowLimitsMinus[r] = c
                break

        if rowLimitsMinus[r] == -1:
            dropMinus += 1
            rowLimitsMinus[r] = 0
        
        for c in range(colsize -2 ,-1,-1):
            if C[r][c] != maxVal:
                rowLimitsPlus[r] = c + 1
                break

        if rowLimitsPlus[r] == -1:
            dropPlus += 1
            rowLimitsPlus[r] = colsize - 1
    
    if dropMinus > 0:
        print("[Munkres] Unexpected non-assignable row [minus], dropping optimisation for ",dropMinus)
    
    if dropPlus > 0:
        print("[Munkres] Unexpected non-assignable row [minus], dropping optimisation for ",dropPlus)

    dropMinus = 0
    dropPlus = 0

    for c in range(colsize-1):
        for r in range(rowsize - 1):
            if C[r][c] != maxVal:
                colLimitsMinus[c] = r
                break
        
        for r in range(rowsize-1,-1,-1):
            if C[r][c] != maxVal:
                colLimitsPlus[c] = r+1
                break
        
        if colLimitsPlus[c] == -1:
            dropPlus += 1
            colLimitsMinus[c] = 0
        
        if colLimitsMinus[c] == -1:
            dropMinus += 1
            colLimitsMinus[c] = rowsize

    if dropMinus > 0:
        print("[Munkres] Unexpected non-assignable column [minus], dropping optimisation for ",dropMinus)
    
    if dropPlus > 0:
        print("[Munkres] Unexpected non-assignable column [minus], dropping optimisation for ",dropPlus)

    rowLimitsMinus[rowsize - 1] = 0
    rowLimitsPlus[rowsize - 1] = colsize - 1

    # Remove last column (except the last element) from all other columns.
    # The last column will then be ignored during the solving.

    for r in range(rowsize - 1):
        lastele = C[r][colsize-1]
        for c in range(colsize-1):
            C[r][c] -= lastele
    
    # Subtract minimum value in every column except the last.
    for c in range(colsize - 1):
        minInCol = C[0][c]

        for r in range(rowsize):
            if C[r][c] < minInCol:
                minInCol = C[r][c]
            
        for r in range(rowsize):
            C[r][c] -= minInCol
    
    step = 2
    return step

# Find a zero in the matrix,
# star it if it is the only one in its row and col.
def stepTwo(step):
    global C,M,rowCover,rowsize,colsize,colCover
    for r in range(rowsize-1):
        for c in range(colsize-1):
            if rowCover[r] == False and colCover[c] == False and iszero(C[r][c]):
                M[r][c] = 1
                rowCover[r] = True
                colCover[c] = True
    
    for c in range(colsize-1):
        if iszero(C[rowsize-1][c]) and colCover[c] == False:
            M[rowsize-1][c] = 1
            colCover[c] = True
    
    # remove coverings (temporarily used to fing independent zeros)
    for r in range(rowsize):
        rowCover[r] = False
    
    for c in range(colsize-1):
        colCover[c] = False
    
    step = 3
    return step


# Check column coverings.
# If all columns are starred (1 star only per column is possible)
# then the algorithm is terminated.
def stepThree(step):
    global C,M,rowCover,rowsize,colsize,colCover,rowLimitsMinus,rowLimitsPlus,colLimitsMinus,colLimitsPlus
    for r in range(rowsize):
        start = rowLimitsMinus[r]
        end = rowLimitsPlus[r]
        for c in range(start,end,1):
            if M[r][c] == 1:
                colCover[c] = True
    
    processedCol = 0

    for c in range(colsize-1):
        if colCover[c] == True:
            processedCol += 1
    
    if processedCol >= colsize - 1:
        step = 7
    else:
        step = 4
    
    return step

# Find a non covered zero, prime it
# . if current row is last or has no starred z
# . else, cover row and uncover the col with a
# Repeat until there are no uncovered zero lef
# Save smallest uncovered value then -> step 6
def stepFour(step):
    global pathRow0,pathCol0,colCover,rowCover
    row = -1
    col = -1
    done = False
    while(done == False):
        row,col = findZero(row,col)

        if row == -1:
            done = True
            step = 6
        else:
            M[row][col] = 2
            colOfStarInRow = findStarInRow(row)
            # If a star was found and it is not in the last row
            if colOfStarInRow > -1 and row < (rowsize - 1):
                rowCover[row] = True
                colCover[colOfStarInRow] = False
                step = 4
            else:
                done = True
                step = 5
                pathRow0 = row
                pathCol0 = col
    return step

def findStarInRow(row):
    global rowLimitsMinus,rowLimitsPlus,M
    start = rowLimitsMinus[row]
    end = rowLimitsPlus[row]
    for c in range(start,end):
        if M[row][c] == 1:
            return c
    return -1

def findZero(row,col):
    global createdZeros,rowCover,colCover,rowLimitsPlus,rowLimitsMinus
    row = -1
    col = -1

    while(len(createdZeros) > 0):
        zero = createdZeros.pop()
        f = zero[0]
        s = zero[1]
        if rowCover[f] == False and colCover[s] == False:
            row = f
            col = s
            return row,col
    
    for r in range(rowsize):
        start = rowLimitsMinus[r]
        end = rowLimitsPlus[r]
        if rowCover[r] == True:
            continue
        for c in range(start,end):
            if colCover[c] == True:
                continue
            if C[r][c] == 0:
                row = r
                col = c
                return row,col
    return row,col


# Make path of alternating primed and starred zeros
# 1. uncovered primed found at step 4
# 2. same column, starred (if any)
# 3. same row, primed (always one)
# 4. continue until a primed zero has no starred zero in its column
# Unstar each starred zero in the series, star each primed zero
# in the series,
# erase all primes, uncover every line, return to step 3.
def stepFive(step):
    global pathCount,path,M,rowCover,rowsize,colCover,colsize,rowLimitsMinus,rowLimitsPlus,pathRow0,pathCol0
    pathCount = 1
    
    path[pathCount-1][0] = pathRow0
    path[pathCount-1][1] = pathCol0

    done = False
    r = 0
    c = 0
    while(done == False):
        r = findStarInCol(path[pathCount-1][1])
        if r == -1:
            done = True
        else:
            pathCount += 1
            path[pathCount-1][0] = r
            path[pathCount-1][1] = path[pathCount-2][1] 

            c = findPrimeInRow(path[pathCount-1][0])
            if c == -1:
                print("Munkres didn't find expected prime")
            pathCount += 1
            path[pathCount-1][0] = path[pathCount-2][0]
            path[pathCount-1][1] = c

    for p in range(pathCount):
        if M[path[p][0]][path[p][1]] == 1:
            M[path[p][0]][path[p][1]] = 0
        else:
            M[path[p][0]][path[p][1]] = 1
    
    # clear covers
    for r in range(rowsize):
        rowCover[r] = False
    for c in range(colsize-1):
        colCover[c] = False
    
    # Erase Primes
    for r in range(rowsize):
        start = rowLimitsMinus[r]
        end = rowLimitsPlus[r]
        for c in range(start,end):
            if M[r][c] == 2:
                M[r][c] = 0
    
    step = 3
    return step

def findStarInCol(col):
    global colLimitsMinus,colLimitsPlus,rowsize,M
    start = colLimitsMinus[col]
    end = colLimitsPlus[col]
    for r in range(start,end):
        if M[r][col] == 1:
            return r

    if M[rowsize-1][col] == 1:
        return rowsize - 1
    return -1 

def findPrimeInRow(row):
    start = rowLimitsMinus[row]
    end = rowLimitsPlus[row]
    for c in range(start,end):
        if M[row][c] == 2:
            return c
    return -1


# Add smallest value to every element of each covered row,
# subtract it from every element of each uncovered col.
# Return to step 4 without altering any stars/primes/covers.
def stepSix(step):
    global rowsize,rowCover,rowLimitsMinus,rowLimitsPlus,colCover,C,createdZeros,colCover
    minVal = 1e9+7
    
    # find smallest
    for r in range(rowsize):
        if rowCover[r] == True:
            continue

        start = rowLimitsMinus[r]
        end = rowLimitsPlus[r]

        for c in range(start,end):
            if colCover[c] == True:
                continue

            if C[r][c] < minVal:
                minVal = C[r][c]

    createdZeros = []

    # add and subtract
    for r in range(rowsize):
        start = rowLimitsMinus[r]
        end = rowLimitsPlus[r]
        for c in range(start,end):
            if rowCover[r] == True:
                C[r][c] += minVal
            
            if colCover[c] == False:
                C[r][c] -= minVal
                if iszero(C[r][c]):
                    createdZeros.append([r,c])
    

    step = 4
    return step

def stepSeven(step):
    print("[HalfMunkres] " , iter , " iterations.")
    return step



def runHalfMunkres(s1,s2,mat):
    global matchings
    setInput(s1,s2,mat)
    runHalf(matchings)


s1 = 3
s2 = 3
mat = [[2500,4000,3500,10000],
        [4000,6000,3500,10000],
        [2000,4000,2500,10000],
        [9000,9000,4000,10000]]
runHalfMunkres(s1+1,s2+1,mat)
print(M)
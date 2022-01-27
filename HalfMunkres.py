import math

class HalfMunkres:
    def __init__(self):
        self.globalstep = 1
        self.iter = 0
        self.rowsize = 0
        self.colsize = 0
        self.C = []
        self.M = []
        self.rowCover = []
        self.colCover = []
        self.path = []
        self.createdZeros = []
        self.rowLimitsMinus = []
        self.rowLimitsPlus = []
        self.colLimitsMinus = []
        self.colLimitsPlus = []
        self.pathRow0 = 0
        self.pathCol0 = 0
        self.pathCount = 0
    
    def iszero(self,t):
        return t==0
    
    def setInput(self,s1,s2,costMatrix):
        
        self.iter = 0
        self.globalstep = 1
    
        self.rowsize = s1
        self.colsize = s2
        self.C = []
        self.M = []
        self.rowCover = []
        self.colCover = []
        self.path = []
        self.createdZeros = []
        self.rowLimitsMinus = []
        self.rowLimitsPlus = []
        self.colLimitsMinus = []
        self.colLimitsPlus = []
    
        nbpaths = 1 + self.colsize + self.rowsize
        for i in range(nbpaths):
            self.path.append([0,0])
        
        for i in range(self.rowsize):
            self.M.append([])
            self.C.append([])
            for j in range(self.colsize):
                self.M[i].append(0)
                self.C[i].append(costMatrix[i][j])
        
        for i in range(self.rowsize):
            self.rowLimitsPlus.append(0)
            self.rowLimitsMinus.append(0)
            self.rowCover.append(False)
        
        for j in range(self.colsize):
            self.colLimitsMinus.append(0)
            self.colLimitsPlus.append(0)
            self.colCover.append(False)
    
    def runHalf(self):
        step = self.globalstep
        maxiter = 5000
        done=False
        while(done == False):
            # print(self.C)
            self.iter += 1

            if self.iter > maxiter:
                step = 7
            
            if step == 1:
                step = self.stepOne(step)
            elif step == 2:
                step = self.stepTwo(step)
            elif step == 3:
                step = self.stepThree(step)
            elif step == 4:
                step = self.stepFour(step)
            elif step == 5:
                step = self.stepFive(step)
            elif step == 6:
                step = self.stepSix(step)
            elif step == 7:
                step = self.stepSeven(step)
                done = True
        self.globalstep = step
        return 0
    
    # Preprocess cost matrix
    def stepOne(self,step):
        minInCol = 1e9 + 7
        maxVal = 1e9+7
    
        for r in range(self.rowsize - 1):
            self.rowLimitsPlus[r] = -1
            self.rowLimitsMinus[r] = -1
        
        for c in range(self.colsize - 1):
            self.colLimitsMinus[c] = -1
            self.colLimitsPlus[c] = -1
        
        dropMinus = 0
        dropPlus = 0
    
        for r in range(self.rowsize -1):
            for c in range(self.colsize - 1):
                if self.C[r][c] != maxVal:
                    self.rowLimitsMinus[r] = c
                    break
    
            if self.rowLimitsMinus[r] == -1:
                dropMinus += 1
                self.rowLimitsMinus[r] = 0
            
            for c in range(self.colsize -2 ,-1,-1):
                if self.C[r][c] != maxVal:
                    self.rowLimitsPlus[r] = c + 1
                    break
    
            if self.rowLimitsPlus[r] == -1:
                dropPlus += 1
                self.rowLimitsPlus[r] = self.colsize - 1
        
        if dropMinus > 0:
            print("[Munkres] Unexpected non-assignable row [minus], dropping optimisation for ",dropMinus)
        
        if dropPlus > 0:
            print("[Munkres] Unexpected non-assignable row [minus], dropping optimisation for ",dropPlus)
    
        dropMinus = 0
        dropPlus = 0
    
        for c in range(self.colsize-1):
            for r in range(self.rowsize - 1):
                if self.C[r][c] != maxVal:
                    self.colLimitsMinus[c] = r
                    break
            
            for r in range(self.rowsize-1,-1,-1):
                if self.C[r][c] != maxVal:
                    self.colLimitsPlus[c] = r+1
                    break
            
            if self.colLimitsPlus[c] == -1:
                dropPlus += 1
                self.colLimitsMinus[c] = 0
            
            if self.colLimitsMinus[c] == -1:
                dropMinus += 1
                self.colLimitsMinus[c] = self.rowsize
    
        if dropMinus > 0:
            print("[Munkres] Unexpected non-assignable column [minus], dropping optimisation for ",dropMinus)
        
        if dropPlus > 0:
            print("[Munkres] Unexpected non-assignable column [minus], dropping optimisation for ",dropPlus)
    
        self.rowLimitsMinus[self.rowsize - 1] = 0
        self.rowLimitsPlus[self.rowsize - 1] = self.colsize - 1
    
        # Remove last column (except the last element) from all other columns.
        # The last column will then be ignored during the solving.
    
        for r in range(self.rowsize - 1):
            lastele = self.C[r][self.colsize-1]
            for c in range(self.colsize-1):
                self.C[r][c] -= lastele
        
        # Subtract minimum value in every column except the last.
        for c in range(self.colsize - 1):
            minInCol = self.C[0][c]
    
            for r in range(self.rowsize):
                if self.C[r][c] < minInCol:
                    minInCol = self.C[r][c]
                
            for r in range(self.rowsize):
                self.C[r][c] -= minInCol
        
        step = 2
        return step
    
    # Find a zero in the matrix,
    # star it if it is the only one in its row and col.
    def stepTwo(self,step):
        for r in range(self.rowsize-1):
            for c in range(self.colsize-1):
                if self.rowCover[r] == False and self.colCover[c] == False and self.iszero(self.C[r][c]):
                    self.M[r][c] = 1
                    self.rowCover[r] = True
                    self.colCover[c] = True
        
        for c in range(self.colsize-1):
            if self.iszero(self.C[self.rowsize-1][c]) and self.colCover[c] == False:
                self.M[self.rowsize-1][c] = 1
                self.colCover[c] = True
        
        # remove coverings (temporarily used to fing independent zeros)
        for r in range(self.rowsize):
            self.rowCover[r] = False
        
        for c in range(self.colsize-1):
            self.colCover[c] = False
        
        step = 3
        return step
    
    
    # Check column coverings.
    # If all columns are starred (1 star only per column is possible)
    # then the algorithm is terminated.
    def stepThree(self,step):
        for r in range(self.rowsize):
            start = self.rowLimitsMinus[r]
            end = self.rowLimitsPlus[r]
            for c in range(start,end,1):
                if self.M[r][c] == 1:
                    self.colCover[c] = True
        
        processedCol = 0
    
        for c in range(self.colsize-1):
            if self.colCover[c] == True:
                processedCol += 1
        
        if processedCol >= self.colsize - 1:
            step = 7
        else:
            step = 4
        
        return step
    
    # Find a non covered zero, prime it
    # . if current row is last or has no starred z
    # . else, cover row and uncover the col with a
    # Repeat until there are no uncovered zero lef
    # Save smallest uncovered value then -> step 6
    def stepFour(self,step):
        row = -1
        col = -1
        done = False
        while(done == False):
            row,col = self.findZero(row,col)
    
            if row == -1:
                done = True
                step = 6
            else:
                self.M[row][col] = 2
                colOfStarInRow = self.findStarInRow(row)
                # If a star was found and it is not in the last row
                if colOfStarInRow > -1 and row < (self.rowsize - 1):
                    self.rowCover[row] = True
                    self.colCover[colOfStarInRow] = False
                    step = 4
                else:
                    done = True
                    step = 5
                    self.pathRow0 = row
                    self.pathCol0 = col
        return step
    
    def findStarInRow(self,row):
        start = self.rowLimitsMinus[row]
        end = self.rowLimitsPlus[row]
        for c in range(start,end):
            if self.M[row][c] == 1:
                return c
        return -1
    
    def findZero(self,row,col):
        row = -1
        col = -1
    
        while(len(self.createdZeros) > 0):
            zero = self.createdZeros.pop()
            f = zero[0]
            s = zero[1]
            if self.rowCover[f] == False and self.colCover[s] == False:
                row = f
                col = s
                return row,col
        
        for r in range(self.rowsize):
            start = self.rowLimitsMinus[r]
            end = self.rowLimitsPlus[r]
            if self.rowCover[r] == True:
                continue
            for c in range(start,end):
                if self.colCover[c] == True:
                    continue
                if self.C[r][c] == 0:
                    row = r
                    col = c
                    return row,col
        return row,col
    
    
    # Make self.path of alternating primed and starred zeros
    # 1. uncovered primed found at step 4
    # 2. same column, starred (if any)
    # 3. same row, primed (always one)
    # 4. continue until a primed zero has no starred zero in its column
    # Unstar each starred zero in the series, star each primed zero
    # in the series,
    # erase all primes, uncover every line, return to step 3.
    def stepFive(self,step):
        self.pathCount = 1
        
        self.path[self.pathCount-1][0] = self.pathRow0
        self.path[self.pathCount-1][1] = self.pathCol0
    
        done = False
        r = 0
        c = 0
        while(done == False):
            r = self.findStarInCol(self.path[self.pathCount-1][1])
            if r == -1:
                done = True
            else:
                self.pathCount += 1
                self.path[self.pathCount-1][0] = r
                self.path[self.pathCount-1][1] = self.path[self.pathCount-2][1] 
    
                c = self.findPrimeInRow(self.path[self.pathCount-1][0])
                if c == -1:
                    print("Munkres didn't find expected prime")
                self.pathCount += 1
                self.path[self.pathCount-1][0] = self.path[self.pathCount-2][0]
                self.path[self.pathCount-1][1] = c
    
        for p in range(self.pathCount):
            if self.M[self.path[p][0]][self.path[p][1]] == 1:
                self.M[self.path[p][0]][self.path[p][1]] = 0
            else:
                self.M[self.path[p][0]][self.path[p][1]] = 1
        
        # clear covers
        for r in range(self.rowsize):
            self.rowCover[r] = False
        for c in range(self.colsize-1):
            self.colCover[c] = False
        
        # Erase Primes
        for r in range(self.rowsize):
            start = self.rowLimitsMinus[r]
            end = self.rowLimitsPlus[r]
            for c in range(start,end):
                if self.M[r][c] == 2:
                    self.M[r][c] = 0
        
        step = 3
        return step
    
    def findStarInCol(self,col):
        start = self.colLimitsMinus[col]
        end = self.colLimitsPlus[col]
        for r in range(start,end):
            if self.M[r][col] == 1:
                return r
    
        if self.M[self.rowsize-1][col] == 1:
            return self.rowsize - 1
        return -1 
    
    def findPrimeInRow(self,row):
        start = self.rowLimitsMinus[row]
        end = self.rowLimitsPlus[row]
        for c in range(start,end):
            if self.M[row][c] == 2:
                return c
        return -1
    
    
    # Add smallest value to every element of each covered row,
    # subtract it from every element of each uncovered col.
    # Return to step 4 without altering any stars/primes/covers.
    def stepSix(self,step):
        minVal = 1e9+7
        
        # find smallest
        for r in range(self.rowsize):
            if self.rowCover[r] == True:
                continue
    
            start = self.rowLimitsMinus[r]
            end = self.rowLimitsPlus[r]
    
            for c in range(start,end):
                if self.colCover[c] == True:
                    continue
    
                if self.C[r][c] < minVal:
                    minVal = self.C[r][c]
    
        self.createdZeros = []
    
        # add and subtract
        for r in range(self.rowsize):
            start = self.rowLimitsMinus[r]
            end = self.rowLimitsPlus[r]
            for c in range(start,end):
                if self.rowCover[r] == True:
                    self.C[r][c] += minVal
                
                if self.colCover[c] == False:
                    self.C[r][c] -= minVal
                    if self.iszero(self.C[r][c]):
                        self.createdZeros.append([r,c])
        
    
        step = 4
        return step
    
    def stepSeven(self,step):
        print("[HalfMunkres] " , self.iter , " iterations.")
        return step
    



class detectors():

    #Method for eye jerking detection:
    def jerking_detection(x,minDist=5,maxDist=12):
        coordR=[]
        coordL=[]
        avgX=0
        si=0
        dist=0
        jerkR=0
        jerkL=0
        right=True
        biggest=0
        smallest=1000000
        
        for i in range (0, len(x)):
            if x[i]>biggest:
                biggest=x[i]
            if x[i]<smallest:
                smallest=x[i]
        midpoint=int((biggest+smallest)/2)

        for i in range (1, len(x)):
            if x[si]<=x[i] and x[si]>midpoint:
                coordR.append(x[si])
            else:
                coordR.append(x[si])
                dist=coordR[-1]-coordR[0]
                if dist>minDist and dist<maxDist:
                    jerkR=jerkR+1
                    print("Right Jerk: ",coordR)
                    del coordR[:]
                else:
                    del coordR[:]
            if x[si]>=x[i] and x[si]<midpoint:
                coordL.append(x[si])
            else:
                coordL.append(x[si])
                dist=coordL[0]-coordL[-1]
                if dist>minDist and dist<maxDist:
                    jerkL=jerkL+1
                    print("Left Jerk: ",coordL)
                    del coordL[:]
                else:
                    del coordL[:]
            si=si+1
        if jerkR<2 or jerkL<2:
            jerkR=0
            jerkL=0
        if jerkR>6:
            jerkR=6
        if jerkL>6:
            jerkL=6
        if jerkR>jerkL:
            return jerkR
        else:
            return jerkL
            
                    

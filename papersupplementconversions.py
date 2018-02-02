import math

# polynomials are lists
# these are just simple functions to implement arithmetic operations on poly.


def removeTailingZeroes(poly):
     lengthNonZero= len(poly)
     if(lengthNonZero == 0):
          return []
     while poly[lengthNonZero-1] == 0:
          lengthNonZero = lengthNonZero -1
     result= poly[:lengthNonZero]

     return result

def addPoly(p1,p2):
    if(len(p1) > len(p2)):
        result = addPoly(p1,p2 + ([0] * (len(p1)-len(p2)) ))[:]
    elif(len(p2)>len(p1)):
        result = addPoly(p2,p1)[:]
    else:
        result = p1[:]
        for i in range(0,len(result)):
            result[i] = result[i] + p2[i]
    return removeTailingZeroes(result[:])

def multiplyByConstant(constant, poly):
    result = poly[:]
    for i in range(0,len(result)):
        result[i] = result[i] * constant
    return result[:]

def multiplyByVar(poly):
    result = [0] + poly[:]
    return result[:]

def divideByVar(poly):
    result = poly[1:len(poly)]
    return result[:]

def multPoly(p1,p2):
    if(len(p1)>len(p2)):
        return multPoly(p2,p1)[:]

    if(len(p1) == 0):
        result = []
    else:
        first = p1[0]
        restOfP1 = p1[1:len(p1)]
        firstTimesP2 = multiplyByConstant(first,p2)[:]
        restOfP1TimesP2 = multiplyByVar(multPoly(restOfP1, p2)  )[:]
        result = addPoly(firstTimesP2,restOfP1TimesP2)[:]
    return result[:]

def Conversion(data, command):
    #print("Command: ",command)
    if(command == "RC to Bump"):
        # this is how the input is interpreted
        r = data[0]
        c = data[1]
        # these are the outputs
        u_out = [r]
        d_out = [1,r*c]
        n_out = 1
        result = [u_out,d_out,n_out]

    elif(command == "Bump to RC"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        if(n != 1):
            print("Tried to extract RC from Bump with n!=0");
        # these are the outputs
        r_out = u[0]
        c_out = d[1]/u[0]
        result = [r_out,c_out]

    elif(command == "Ladder+Bump to Bump"):
         # this is how the input is interpreted
        r = data[0]
        c = data[1]       

        u = data[2]
        d = data[3]
        n = data[4]
       
        # these are the outputs
        u_out = addPoly(u,multiplyByConstant(r,d))[:]
        d_out = addPoly( multPoly([1,r*c], d), multPoly([0,c], u))[:]
        n_out = n + 1
        result = [u_out,d_out,n_out]

    elif(command == "Bump to Ladder+Bump"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]

        # these are the outputs
        n_out = n - 1
        r_out = (u[n_out]*u[n_out])/((u[n_out] * d[n_out]) - (d[n_out+1] * u[n_out-1]))
        c_out = d[n_out+1]/u[n_out]
        u_out = addPoly(u, multiplyByConstant(-u[n_out]/(u[n_out]*d[n_out] - d[n_out+1]*u[n_out-1]),addPoly(multiplyByConstant(u[n_out],d)    ,multPoly([0,-d[n_out+1]],u)   )))[:]

        d_out = addPoly(d, multPoly([0,-d[n_out+1]/u[n_out]],u))[:]


        result = [r_out,c_out,u_out,d_out,n_out]

    elif(command == "Voight+Bump to Bump"):
        # this is how the input is interpreted
        r = data[0]
        c = data[1]
        u = data[2]
        d = data[3]
        n = data[4]

        # these are the outputs
        u_out = addPoly(multPoly([1,r*c],u),multiplyByConstant(r,d))[:]
        d_out = multPoly([1,r*c],d)[:]
        n_out = n + 1
        result = [u_out,d_out,n_out]

    elif(command == "2-Bump to 2-Voight"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        # these are the outputs
        tau1 = 1/2 * (d[1] + math.sqrt(d[1]*d[1] - 4 * d[2]))
        tau2 = 1/2 * (d[1] - math.sqrt(d[1]*d[1] - 4 * d[2]))
        r2_out = (u[1] - u[0]*tau2)/(tau1 - tau2)
        r1_out = u[0] - r2_out
        c1_out = tau1/r1_out
        c2_out = tau2/r2_out

        result = [[r1_out,c1_out],[r2_out,c2_out]]

    elif(command == "Maxwell+Bump to Bump"):
        # this is how the input is interpreted
        r = data[0]
        c = data[1]
        u = data[2]
        d = data[3]
        n = data[4]
        # these are the outputs
        u_out = multPoly([1,r*c],u)[:]
        d_out = addPoly(multPoly([1,r*c],d),multPoly([0,c],u))[:]
        n_out = n + 1
        result = [u_out,d_out,n_out]

    elif(command == "2-Bump to 2-Maxwell"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        # these are the outputs
        if(n!=2):
            print("tried to convert Bump to Maxwell but not 2 bumps")
        r1_out = u[0]
        r2_out = u[1]/(d[1] - (d[2]*u[0]/u[1] + u[1]/u[0]))
        c1_out = d[2]/u[1]
        c2_out = u[1]/(u[0]*r2_out)

        result = [[r1_out,c1_out],[r2_out,c2_out]]

    elif(command == "3-Bump to 3-Maxwell"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        # these are the outputs
        if(n!=3):
            print("tried to convert Bump to Maxwell but not 3 bumps")
        r1_out = u[0]
        c1_out = d[3]/u[2]

        a = multiplyByConstant(1/u[0],u)[:]
        b = addPoly(multiplyByConstant(1/u[0],d),addPoly(multiplyByConstant(-1/(u[0]*u[0]), u ),multPoly([0,-d[3]/(u[2]*u[0])],u)))[:]
        tau2 = 1/2 * (a[1] + math.sqrt(a[1]*a[1] - 4*a[2]))
        tau3 = 1/2 * (a[1] - math.sqrt(a[1]*a[1] - 4*a[2]))

        c2_out = (b[1] * tau2 - b[2])/(tau2-tau3)
        c3_out = (b[2] - b[1]*tau3)/(tau2 - tau3)

        r2_out = tau2/c_out[2]
        r3_out = tau3/c_out[3]

        result = [[r1_out,c1_out],[r2_out,c2_out], [r3_out,c3_out]]

    elif(command == "n-Bump to n-Ladder"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        # these are the outputs
        rcList = []
        while n > 1:
            output = Conversion([u,d,n],"Bump to Ladder+Bump")[:]
            r = output[0]
            c = output[1]
            rcList = rcList + [[r,c]]
            u = output[2]
            d = output[3]
            n = output[4]
        output = Conversion([u,d,n],"Bump to RC")[:]
        r = output[0]
        c = output[1]
        rcList = rcList + [[r,c]]

        result = rcList[:]

    elif(command == "n-Ladder to n-Bump"):
        # this is how the input is interpreted
        rcList = data[:]
        # these are the outputs
        r = rcList[len(rcList)-1][0]
        c = rcList[len(rcList)-1][1]
        rcList = data[:len(rcList)-1]
        output = Conversion([r,c],"RC to Bump")[:]
        u = output[0]
        d = output[1]
        n = output[2]
        while len(rcList) >0 :
            r = rcList[len(rcList)-1][0]
            c = rcList[len(rcList)-1][1]
            rcList = data[:len(rcList)-1]
            output = Conversion([r,c,u,d,n],"Ladder+Bump to Bump")[:]
            u = output[0]
            d = output[1]
            n = output[2]

        result = [u,d,n]

    elif(command == "n-Voight to n-Bump"):
        # this is how the input is interpreted
        rcList = data
        # these are the outputs
        r = rcList[len(rcList)-1][0]
        c = rcList[len(rcList)-1][1]
        rcList = data[:len(rcList)-1]
        output = Conversion([r,c],"RC to Bump")[:]
        u = output[0]
        d = output[1]
        n = output[2]

        while len(rcList) >0 :
            r = rcList[len(rcList)-1][0]
            c = rcList[len(rcList)-1][1]
            rcList = data[:len(rcList)-1]
            output = Conversion([r,c,u,d,n],"Voight+Bump to Bump")[:]
            u = output[0]
            d = output[1]
            n = output[2]

        result = [u,d,n]

    elif(command == "n-Maxwell to n-Bump"):
        # this is how the input is interpreted
        rcList = data[:]
        # these are the outputs
        r = rcList[0][0]
        c = rcList[0][1]
        rcList = data[1:len(rcList)]
        output = Conversion([r,c],"RC to Bump")[:]
        u = output[0]
        d = output[1]
        n = output[2]

        while len(rcList) >0 :
            r = rcList[0][0]
            c = rcList[0][1]
            rcList = data[1:len(rcList)]
            output = Conversion([r,c,u,d,n],"Maxwell+Bump to Bump")[:]
            u = output[0]
            d = output[1]
            n = output[2]

        result = [u,d,n]


    elif(command == "C to Bump"):
        # this is how the input is interpreted
        c = data[0]
        # these are the outputs
        u_out = [1]
        d_out = [0,c]
        n_out = 1
        result = [u_out,d_out,n_out]


    elif(command == "Bump to C"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        # these are the outputs

        c_out = d[1]
        result = [c_out]

    elif(command == "n-Bump to n-Ladder, C"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]
        rcList = []
        # these are the outputs
        while n>1:
            output = Conversion([u,d,n],"Bump to Ladder+Bump")[:]
            r = output[0]
            c = output[1]
            rcList = rcList + [[r,c]]
            u = output[2]
            d = output[3]
            n = output[4]

        output = Conversion([u, d, n], "Bump to C")[:]
        c = output[0]
        rcList = rcList + [c]
        result = rcList

    elif(command == "n-Ladder to n-Bump, C"):
        # this is how the input is interpreted
        rcList = data[:]
        # these are the outputs
        c = rcList[len(rcList)-1]
        rcList = data[:len(rcList)-1]
        output = Conversion([c],"C to Bump")[:]
        u = output[0]
        d = output[1]
        n = output[2]
        while len(rcList) >0 :
            r = rcList[len(rcList)-1][0]
            c = rcList[len(rcList)-1][1]
            rcList = data[:len(rcList)-1]
            output = Conversion([r,c,u,d,n],"Ladder+Bump to Bump")[:]
            u = output[0]
            d = output[1]
            n = output[2]

        result = [u,d,n]


    elif(command == "n-Voight to n-Bump, C"):
        # this is how the input is interpreted
        rcList = data[:]
        # these are the outputs
        c = rcList[len(rcList)-1]
        rcList = data[:len(rcList)-1]
        output = Conversion([c],"C to Bump")[:]
        u = output[0]
        d = output[1]
        n = output[2]

        while len(rcList) >0 :
            r = rcList[len(rcList)-1][0]
            c = rcList[len(rcList)-1][1]
            rcList = data[:len(rcList)-1]
            output = Conversion([r,c,u,d,n],"Voight+Bump to Bump")[:]
            u = output[0]
            d = output[1]
            n = output[2]

        result = [u,d,n]

    elif(command == "Bump to C+Bump"):
        # this is how the input is interpreted
        u = data[0]
        d = data[1]
        n = data[2]

        # these are the outputs
        c_out = d[1]
        d_out = multiplyByConstant(1/c_out,divideByVar(d))[:]
        u_out = multiplyByConstant(1/c_out,divideByVar(addPoly(u, multiplyByConstant(-1,d_out))))[:]
        n_out = n - 1


        result = [c_out,u_out,d_out,n_out]

    elif(command == "n-Voight to n-Ladder, C"):
        result= Conversion(Conversion(data,"n-Voight to n-Bump, C"),"n-Bump to n-Ladder, C")

    elif(command == "n-Voight to n-Ladder"):
        result= Conversion(Conversion(data,"n-Voight to n-Bump"),"n-Bump to n-Ladder")

    elif(command == "n-Maxwell to n-Ladder"):
        result= Conversion(Conversion(data,"n-Maxwell to n-Bump"),"n-Bump to n-Ladder")

    elif(command == "n-Voight to n-Maxwell"):
        if(len(data)>3):
            print("n-Voight to n-Maxwell is not yet implemented for n>3")
        elif(len(data) == 3):
            result= Conversion(Conversion(data,"n-Voight to n-Bump"),"3-Bump to 3-Maxwell")
        elif(len(data) == 2):
            result= Conversion(Conversion(data,"n-Voight to n-Bump"),"2-Bump to 2-Maxwell")
        else:
            print("too simple")


    elif(command == "n-Ladder to n-Maxwell"):
        if(len(data)>3):
            print("n-Ladder to n-Maxwell is not yet implemented for n>3")
        elif(len(data) == 3):
            result= Conversion(Conversion(data,"n-Ladder to n-Bump"),"3-Bump to 3-Maxwell")
        elif(len(data) == 2):
            result= Conversion(Conversion(data,"n-Ladder to n-Bump"),"2-Bump to 2-Maxwell")
        else:
            print("too simple")

    elif(command == "n-Ladder to n-Voight"):
        if(len(data)>2):
            print("n-Ladder to n-Voight is not yet implemented for n>2")
        elif(len(data) == 2):
            result= Conversion(Conversion(data,"n-Ladder to n-Bump"),"2-Bump to 2-Voight")
        else:
            print("too simple")


    elif(command == "Simple Figure 1 Conversion"):
        # this is how the input is interpreted
        rOhm = data[0]
        r1   = data[1]
        c1   = data[2]
        # these are the outputs
        r1_out = rOhm + r1
        r2_out = (rOhm + r1) * rOhm/r1
        c1_out = c1  * (r1*r1)/((rOhm + r1)*(rOhm + r1))
        result = [r1_out,c1_out,r2_out]
    else:
        print("Unknown Command")
        result = []
    return result




print("Test 1")
print(Conversion([1033.22,109.00030],"RC to Bump"))
print("Test 2")
print(Conversion([[1033.22]  ,[1,112621.289966]  , 1 ],"Bump to RC"))


print("Test 3")
print(Conversion([3131322,0.1,[1033.22]  ,[1,112621.289966]  , 1 ],"Ladder+Bump to Bump"))
print("Test 4")
print(Conversion([[3132355.22, 352653522938.91504], [1.0, 425856.811966, 35265352293.8915], 2],"Bump to Ladder+Bump"))

print("Complex Figure")
print("C = 1")
print(Conversion([[100, 0.0001], [10, 1] , [10, 10], [10, 100] ,
  1], "n-Voight to n-Ladder, C"))



print("C = 10")
print(Conversion([[100, 0.0001], [10, 1] , [10, 10], [10, 100] ,
  10], "n-Voight to n-Ladder, C"))

print("C = 100")
print(Conversion([[100, 0.0001], [10, 1] , [10, 10], [10, 100] ,
  100], "n-Voight to n-Ladder, C"))

print("C = 1000")
print(Conversion([[100, 0.0001], [10, 1] , [10, 10], [10, 100] ,
  1000], "n-Voight to n-Ladder, C"))

print("C = 10000")
print(Conversion([[100, 0.0001], [10, 1] , [10, 10], [10, 100] ,
  10000], "n-Voight to n-Ladder, C"))


Conversion([1,2,3],"Simple Figure 1 Conversion")





import sys


def candidate(u,c):
    if(c == 2):
        print('C'+str(c)+' is:-')
    v = []
    x = []

    for k in u.keys():
        x.append(k)
    #print(x)

    for i in range(0, len(u)-1, 1):
        for j in range(i+1, len(u), 1):
            v1 = []
            v1.append(x[i])
            v1.append(x[j])
            v.append(v1)

    newv = []
    for i in range(0, len(v), 1):
        l3 = []
        z = v[i]
        a = ','.join(z)
        nv = a.split(',')
        for z in range(0, len(nv), 1):
            l3.append(nv[z])
        newv.append(l3)
    #print(newv)
    return newv



def freqlist(u,v,w,c):
    minsupport = w
    print('L'+str(c)+' is:-')
    L = {}
    for i in range(0, len(u), 1):
        #for x, y in u.items():
        z = u[i]
        a = ','.join(z)          
        if(v[i] >= minsupport):
                L[a] = v[i]
    print(L)
    return L



def supcount(u,v,rows):
    print("Support is:-")
    sup = []
    for i in range(0, len(u), 1):
        j = 0
        count = 0
        while(j < rows):
            if(set(u[i]).issubset(set(v[j]))):
                count += 1
            j +=1
        sup.append(count)
    print(sup)
    return sup

def supcountfin(u,v,rows):
    sup = []
    for i in range(0, len(u), 1):
        j = 0
        count = 0
        while(j < rows):
            if(set(u[i]).issubset(set(v[j]))):
                count += 1
            j +=1
        sup.append(count)
    return sup



def removedup(u,v):
    print('C'+str(v)+' is:-')
    remd = []
    newremd = []
    
    for i in range(0, len(u), 1):
        a = set(u[i])
        k = list(a)
        remd.append(k)
        
    for i in range(0, len(remd), 1):
        if (len(remd[i]) == v):
            newremd.append(remd[i])
    
    print(newremd)
    return newremd
     
    

def association(list,n,combo=[]):
    if combo is None:
        combo = []

    if len(list) == n:
        if combo.count(list) == 0:
            combo.append(list)
            combo.sort()
        return combo
    else:
        for i in range(0, len(list), 1):
            #for j in range(0, len(list[i]), 1):
            ref_list = list[:i] + list[i+1:]
            combo = association(ref_list,n,combo)
        return combo

         
           
    


def main():
    support = int(input("Enter Minimum Support Value:"))
    confidence = int(input("Enter Minimum Confidence Value in Percentage:"))

    datafile = sys.argv[1]
    f = open(datafile)
    newdata = []
    l = f.readline()
    while(l != ''):
        a = l.split()
        l2 = a[1].split()
        newdata.append(l2)
        l = f.readline()    
    
    #print(newdata)
    rows = len(newdata)
    f.close()
    
    data = []
    for i in newdata:
        for j in i:
            l3 = []
            a = j.split(',')
            for z in range(0, len(a), 1):
                l3.append(a[z])
            data.append(l3)
    print("DATA IS:-")
    print(data)
        
    #1st iteration
    iteration = 1
    print("1st ITERATION:")
    print('C1 is:-')
    C = {}
    for j in newdata:
        for x in j:
            a = x.split(',')
            print(a)
            for z in range(0, len(a), 1):
                if(a[z] in C):
                    C[a[z]] = C[a[z]] + 1
                else:
                    C[a[z]] = 1

    print(C)
    #print(count['Sugar'])
    print('L1 is:-')
    L = {}
    for i in range(0, len(C), 1):
        for x, y in C.items():
            if(y >= support):
                L[x] = y
    print(L)
    strongassoc = []
    
    flag = 0
    iteration += 1
    p = candidate(L,iteration)
    print(p)
    s = supcount(p,data,rows)
    f = freqlist(p,s,support,iteration)
    #print(f)
    
    f1 = open("associations.txt","a+")
    #f2 = open("finalassoc.txt","a+")
    if(bool(f) == True):
        c = iteration - 1
        l = []
        for x in f:
            a = x.split(',')
            l.append(a)
        #print(l)

        strongassoc = []
        
        while(c != 0):
            for i in range(0, len(l), 1):
                ar = association(l[i],c,combo=[])
                #print(ar)
                for j in range(0, len(ar), 1):
                    x = []
                    conf = []
                    for k in range(0, len(l[i]), 1):
                        num1 = []
                        denom1 = []
                        if(l[i][k] not in ar[j]):
                            sa = []
                            lis = ""
                            x.append(l[i][k])
                            #print(x + ar[j])
                            print(str(x)+" -> "+str(ar[j]))
                            #print(str(ar[j])+" -> "+str(l[k]))
                            f1.write(str(x)+" -> "+str(ar[j])+"\n")
                            #f2.write(str(x)+"*"+str(ar[j])+"\n")
                            #f1.write(str(ar[j])+" -> "+str(l[k])+"\n")
                            num = list(set(x).union(set(ar[j])))
                            num1.append(num)
                            numsupp = supcountfin(num1,data,rows)
                            print("Support of (A U B) is:-",numsupp)
                            denom = list(set(x))
                            denom1.append(denom)
                            denomsupp = supcountfin(denom1,data,rows)
                            print("Support of A is:-",denomsupp)
                            #print(num)
                            #print(denom)
                            conf.append((numsupp[0]/denomsupp[0])*100)
                            print("Confidence in % is:-",conf)
                            if(conf[0] >= confidence):
                                lis = (str(x)+" -> "+str(ar[j]))
                                sa.append(lis)
                                sa.append(str(numsupp))
                                sa.append(str(conf))
                                strongassoc.append(sa)

            c -= 1
    f1.close()
    #f2.close()
   
    #assoc = set(line.strip() for line in open("associations.txt"))
    #print("This is 1st",list(assoc))
    '''
    f1 = open("associations.txt","w+")
    f1.truncate()
    f1.close()
    '''

    for i in range(0, len(s),1):
        if(s[i] >= support):
            flag = 1
            break
        else:
            flag = 0

    if(len(f) == 1 or len(f) == 0):
        flag = 0
        
    iteration += 1
    while(flag == 1): 
        f1 = open("associations.txt","a+")
        #f2 = open("finalassoc.txt","a+")
        
        p = candidate(f,iteration)
        r = removedup(p,iteration)
        s = supcount(r,data,rows)
        f = freqlist(r,s,support,iteration)
        if(bool(f)  == True):
            c = iteration - 1
            l = []
            for x in f:
                a = x.split(',')
                l.append(a)
            while(c != 0):
                for i in range(0, len(l), 1):
                    ar = association(l[i],c,combo=[])
                    #print(ar)

                    for j in range(0, len(ar), 1):
                        x = []
                        conf = []
                        num1 = []
                        denom1 = []
                        sa = []
                        lis = []
                        for k in range(0, len(l[i]), 1):
                            #num1 = []
                            #denom1 = []
                            if(l[i][k] not in ar[j]):
                                x.append(l[i][k])
                        print(str(x)+" -> "+str(ar[j]))
                        f1.write(str(x)+" -> "+str(ar[j])+"\n")
                        num = list(set(x).union(set(ar[j])))
                        num1.append(num)
                        numsupp = supcountfin(num1,data,rows)
                        print("Support of (A U B) is:-",numsupp)
                        denom = list(set(x))
                        denom1.append(denom)
                        denomsupp = supcountfin(denom1,data,rows)
                        print("Support of A is:-",denomsupp)
                        #print(num)
                        #print(denom)
                        conf.append((numsupp[0]/denomsupp[0])*100)
                        print("Confidence in % is:-",conf)
                        if(conf[0] >= confidence):
                            lis = (str(x)+" -> "+str(ar[j]))
                            sa.append(lis)
                            sa.append(str(numsupp))
                            sa.append(str(conf))
                            strongassoc.append(sa)


                        conf = []
                        num1 = []
                        denom1 = []
                        sa = []
                        lis = ""
                        
                        print(str(ar[j])+" -> "+str(x))
                        f1.write(str(ar[j])+" -> "+str(x)+"\n")
                        num = list(set(ar[j]).union(set(x)))
                        num1.append(num)
                        numsupp = supcountfin(num1,data,rows)
                        print("Support of (A U B) is:-",numsupp)
                        denom = list(set(ar[j]))
                        denom1.append(denom)
                        denomsupp = supcountfin(denom1,data,rows)
                        print("Support of A is:-",denomsupp)
                        #print(num)
                        #print(denom)
                        conf.append((numsupp[0]/denomsupp[0])*100)
                        print("Confidence in % is:-",conf)
                        if(conf[0] >= confidence):
                            lis = (str(x)+" -> "+str(ar[j]))
                            sa.append(lis)
                            sa.append(str(numsupp))
                            sa.append(str(conf))
                            strongassoc.append(sa)


                        #f2.write(str(x)+"*"+str(ar[j])+"\n")
                        #f2.write(str(ar[j])+"*"+str(x)+"\n")

                c -= 1

        f1.close()
        #f2.close()

        if(bool(f) == True):        
            assoc = set(line.strip() for line in open("associations.txt"))
            #print("This is association after removal of any duplicates\n",list(assoc))

        f1 = open("associations.txt","w+")
        f1.truncate()
        f1.close()
       
        iteration += 1
        for i in range(0, len(s),1):
            if(s[i] >= support):
                flag = 1
                break
            else:
                flag = 0
        if(len(f) == 1 or len(f) == 0):
            flag = 0


    seen = set()
    print("STRONG ASSOCIATION RULES ARE IN THE FORMAT ([A->B] , [Support] , [Confidence]):-")
    #print(strongassoc)
    #print("A->B  Support  Confidence")
    for x in strongassoc:
        if tuple(x) not in seen:
            seen.add(tuple(x))
    stronga = list(seen)
    for i in range(0,len(stronga), 1):
        print(list(stronga[i]))

    
if __name__ == "__main__":
    main()

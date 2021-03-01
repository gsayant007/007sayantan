import random
import numpy as np
%config Completer.use_jedi = False
import math
string='01'
import matplotlib.pyplot as plt
def create_individual(n_proj:int,time:int):
    m=[[int(random.choice(string)) for i in range(n_proj)] for j in range(time)]
    for i in range(len(m)-1):
        for j in range(len(m[i])):
            if m[i][j]==1:
                m[i+1][j]=0
            elif m[i][j]==0:
                m[i+1][j]=1
                
    for i in range(len(m)):
        if np.sum(m[i])>=M:
            pass
        else:
            if np.sum(m[i])==0:
                r=random.choice([j for j in range(5)])
                m[i][r]=1
                m[i][r+1]=1
            elif np.sum(m[i])==1:
                for j in range(len(m[i])):
                    if m[i][j]==1 and j!=5:
                        m[i][j+1]=1
                    elif m[i][j]==1 and j==5:
                        m[i][1]=1
    return m
N=6 #number of projects
T=2 # number of time periods
M=2 # compulsory projects to be attempted
B=[random.randrange(20,60) for i in range(N)]
r=[[random.randrange(1,10) for i in range(N)] for t in range(T)]    #recycling cost
s=[[random.randrange(1,10) for i in range(N)] for t in range(T)]    # sorting cost
d=[[random.randrange(1,10) for i in range(N)] for t in range(T)]    # disassembly cost

for t in range(T):
    for i in range(N):
        if r[t][i]+s[t][i]+d[t][i]<=B[i]:
            pass
        else:
            r[t][i]=int(B[i]/4)
            s[t][i]=int(B[i]/4)
            d[t][i]=int(B[i]/4)

u=[[random.randrange(1,10) for i in range(N)] for t in range(T)] # resources available for each projects in time period t
# sample solution x=[[1,1,0,0,0,0],[0,1,0,1,1,0]]
# Tau=[random.randrange(7,21) for i in range(N)] # duration of each projects
U=[random.randrange(20,60) for t in range(T)] #Maximum resources available in time period t.
max_gen=200
pop_size=50
mutation_probability=0.58
cross_over_rate=0.4

def obj_func_1(x:list):
    sum1=0
    for i in range(len(x)):
        for j in range(len(x[i])):
            sum1+=(r[i][j]+s[i][j]+d[i][j])*x[i][j]
    return sum1
    
    
def obj_func_2(x:list):
    s1=0
    s2=0
    for i in range(len(x)):
        for j in range(len(x[i])):
            s1=s1+u[i][j]*x[i][j]
    for t in range(T):
        s2=s2+U[t]
    return s2-s1
def coll_obj_func(x):
    return [obj_func_1(x),obj_func_2(x)]

def mutation(x:list,prob:float):
    y=[[0 for i in range(N)] for j in range(T)]
    for i in range(len(x)):
        for j in range(len(x[i])):
            if prob<0.59 and x[i][j]==0:
                y[i][j]=int(random.choice(string))
            elif 0.59<=prob<=0.9 and x[i][j]==1:
                y[i][j]=int(random.choice(string))
    for i in range(len(y)):
        for j in range(len(y[i])):
            if y[i][j]==0:
                y[i][j]=int(random.choice(string))
            elif y[i][j]==1:
                y[i][j]=0
    return y
def cross_over(L:list,cross_rate:float):
    z=[[0 for i in range(N)] for j in range(T)]
    for x in L:
        for y in L:
            if cross_rate<0.4:
                z[0][0:3]=x[0][0:3]
                z[0][3:6]=y[0][3:6]
                z[1]=x[1]
                return z
        
            else:
                z[1][0:3]=x[1][0:3]
                z[1][3:6]=y[1][3:6]
                z[0]=y[0]
                return z
cross_over(L,0.49) 

def count_1(x:list):
    sum1=0
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j]==1:
                sum1=sum1+1
            else:
                sum1=sum1
    return sum1
 
def list_to_str(L:list):
    str1=''
    for ele in L:
        str1+=str(ele)
    return str1  
  
def non_dominated_sort(L:list):
    S={}
    n={}
    rank={}
    front=[[]]
    for p in L:
        S[list_to_str(np.reshape(p,12))]=[]
        n[list_to_str(np.reshape(p,12))]=0
        for q in L:
            if (obj_func_1(p)<=obj_func_1(q) and obj_func_2(p)<=obj_func_2(q)) and (obj_func_1(p)<obj_func_1(q) or obj_func_2(p)<obj_func_2(q)):
                if q not in S[list_to_str(np.reshape(p,12))]:
                    S[list_to_str(np.reshape(p,12))].append(q)
            elif (obj_func_1(q)<=obj_func_1(p) and obj_func_2(q)<=obj_func_2(p)) and (obj_func_1(q)<obj_func_1(p) or obj_func_2(q)<obj_func_2(p)):
                n[list_to_str(np.reshape(p,12))]=n[list_to_str(np.reshape(p,12))]+1
        if n[list_to_str(np.reshape(p,12))]==0:
            rank[list_to_str(np.reshape(p,12))]=1
            front[0].append(p)
    i=0
    while len(front[i])!=0:
        Q=[]
        for p in front[i]:
            for q in S[list_to_str(np.reshape(p,12))]:
                n[list_to_str(np.reshape(p,12))]=n[list_to_str(np.reshape(p,12))]-1
                if n[list_to_str(np.reshape(p,12))]==0:
                    rank[list_to_str(np.reshape(p,12))]=i+1
                    if q not in Q:
                        Q.append(q)
        i=i+1
        front.append(Q)
    return front
            
    
        
L=[]
for i in range(20):
    L.append(create_individual(N,T))
# non_dominated_sort(L)
f1_values=[obj_func_1(x) for x in L]
f2_values=[obj_func_2(x) for x in L]
def crowding_distance(L:list):
    l=len(L)
    distance=[0 for i in range(l)]
    for i in range(2):
        L=sorted(L,key=lambda x:coll_obj_func(x)[i])
        distance[0]=-99999
        distance[l-1]=99999
        for j in range(1,l-1):
            distance[j]+=(coll_obj_func(L[j+1])[i]-coll_obj_func(L[i-1])[i])

    
    return distance

P={}
Q={}
R={}
for i in range(max_gen):
    P[i]=[]
    Q[i]=[]
    R[i]=[]
t=0
while(t<5):
    for i in range(pop_size):
        P[t].append(create_individual(N,T))
    for p in P[t]:
        Q[t].append(mutation(p,0.58))
    R[t]=P[t]+Q[t]
    
    FRONTS=non_dominated_sort(R[t])
    
    for k in range(len(FRONTS)-1):
        for i in range(len(FRONTS[k])):
            for j in range(len(FRONTS[k])-i-1):
                if crowding_distance(FRONTS[k])[j]<crowding_distance(FRONTS[k])[j+1]:
                    FRONTS[k][j],FRONTS[k][j+1]=FRONTS[k][j+1],FRONTS[k][j]
#     for k in range(len(FRONTS)-1):
#         f1_values=[obj_func_1(FRONTS[k][i]) for i in range(len(FRONTS[k]))]
#         f2_values=[obj_func_2(FRONTS[k][i]) for i in range(len(FRONTS[k]))]
#         plt.scatter(f1_values,f2_values)
    
    
    
    i=0
    while len(P[t+1])+len(FRONTS[i])<=pop_size and FRONTS[i]!=[]:
        CROWDING_DISTS=[]
        CROWDING_DISTS.append(crowding_distance(FRONTS[i]))
        P[t+1]=P[t+1]+FRONTS[i]
        i=i+1
        P[t+1]=P[t+1]+FRONTS[k][0:(pop_size-len(P[t+1]))]
    for p in P[t+1]:
        Q[t+1].append(mutation(p,mutation_probability))
    R[t+1]=P[t+1]+Q[t+1]
    R[t]=R[t+1]
        
    for k in range(len(FRONTS)-1):
        f1_values=[obj_func_1(FRONTS[k][i]) for i in range(len(FRONTS[k]))]
        f2_values=[obj_func_2(FRONTS[k][i]) for i in range(len(FRONTS[k]))]
        plt.scatter(f1_values,f2_values)
    
    
        
    t=t+1   

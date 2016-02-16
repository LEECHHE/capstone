# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
import collections
import itertools
import pandas as pd
#Parameters
# x1 = [1,1,0,1,0,0,1,0,1,0]
# x2 = [0,1,0,1,0,1,1,0,1]
# x3 = [0,1,1,1,0,1,1,0,1,0]
ans = {"Iris-setosa":0,"Iris-versicolor":1,"Iris-virginica":2}
class K2(object):
    # u : a limit to the number of parents
    # n : the number of features
    # D : database
    # r : the length of the list of all possible values of attribute x[i] in D
    def __init__(self,args):
        self._u, self._D, self._r = self.__parse(args)
        print(self._D)

    def __parse(self,args):
        path = args.dataset
        delimiter = args.delimiter
        #try to read dataset
        try:
            f = open(path,"r")
        except:
            print("Invalid path : "+path)
            return None

        #meta-data
        #[Id,SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm,Species]
        self._meta_data = f.readline().split(delimiter)[1:] #exclude 'Id'
        u = len(self._meta_data)-1
        D = list()

        #input database D
        #it is only for Iris data
        while True:
            data = f.readline().rstrip('\n').split(delimiter)[1:]
            if not data : break;
            for i in xrange(len(data)-1):
                data[i] = float(data[i])
            data[4] = ans[data[4]]
            D.append(data)
        # D=np.array(D)

        #try to find r
        ## this phase seems inefficient.....
        #get all possible values
        r = [set()]*len(self._meta_data)
        for i in xrange(len(self._meta_data)):
            for data in D[i]:
                r[i].add(data)

        #get the length of each set
        for i in xrange(len(r)):
            r[i] = len(r[i])
        return u,pd.DataFrame(D),r


    def run(self):
        pi = {}
        Pred = [
        [],[],[0,1],[0,1],[0,1,2,3]
        ]
        D = self._D
        r = self._r
        u = self._u
        
        for i in xrange(len(self._meta_data)):
            pi[i] = []

        for i in xrange(len(self._meta_data)):
            #print '-------------------'+str(i)
            
            #Initialization of P_old
            unique_vals = list(set(D[i]))
            alphas = []
            for ele in unique_vals:
                alphas.append(sum([x==ele for x in D[i]]))
            N = sum(alphas)
            P_old = math.factorial(r[i]-1)/math.factorial(N+r[i]-1)*np.product([math.factorial(x) for x in alphas])
            print 'P_old = %f' % P_old
            
            
            #START
            OKToProceed = True
            the_list = []
            while OKToProceed and len(pi[i])<u and len(Pred[i])>0:
                vals = []
                Dyn_Pred = [x for x in Pred[i] if x not in pi[i]]
                for pred in Dyn_Pred:
                    unique = list(set(D[pred]))
                    temp = [x for x in the_list]
                    temp.append(unique)
                    combinations = list(itertools.product(*temp))
                    val1 = 1
                    temp_nodes = [x for x in pi[i]]
                    temp_nodes.append(pred)
                    for ele in combinations:
                        temp_D = D
                        print '----'+str(pred)
                        print ele
                        for l in range(len(ele)):
                            temp_D = temp_D[temp_D[temp_nodes[l]]==ele[l]]
                        # print i
                        # print temp_D
                        SS = []
                        for uval in unique_vals:
                            SS.append(sum(temp_D[i]==uval))
                        NN = sum(SS)
                        prod_fact = np.prod([math.factorial(x) for x in SS])
                        val1 *= math.factorial(r[i]-1)/math.factorial(NN+r[i]-1)*prod_fact
                    vals.append(val1)
                #print vals
                if len(vals)>0:
                    P_new = np.max(vals)
                    p = [ww for ww, j in enumerate(vals) if j == P_new]
                    pos = p[0]
                    if P_new > P_old:
                        P_old = P_new
                        pi[i].append(Pred[i][pos])
                        the_list.append(list(set(D[pred])))
                    else:
                        OKToProceed = False
                else:
                    OKToProceed = False
            if len(pi[i])>0:
                for ele in pi[i]:
                    print 'Node: '+self._meta_data[i]+', Parents of x'+self._meta_data[i]+': '+self._meta_data[ele]
            else:
                print ('Node: '+self._meta_data[i]+' has no parents!!')

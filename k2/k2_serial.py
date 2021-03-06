from __future__ import division
import numpy as np
import itertools
import pandas as pd
import operator
import time
import sys
import argparse
import pickle

meta_data = []
def vals_of_attributes(D, n):
    output = []
    for i in xrange(n):
        output.append(list(map(lambda x : round(x,4), np.unique(D[:, i]))))
    return output


def alpha(df, mask):
    _df = df
    for combo in mask:
        _df = _df[_df[combo[0]] == combo[1]]
    return len(_df)


def f(i, pi, attribute_values, df):

    phi_i_ = [attribute_values[item] for item in pi]
    if len(phi_i_) == 1:
        phi_i = [[item] for item in phi_i_[0]]
    else:
        phi_i = list(itertools.product(*phi_i_))

    # bug fix: phi_i might contain empty tuple (), which shouldn't count in q_I
    try:
        phi_i.remove(())
    except ValueError:
        pass

    q_i = len(phi_i)

    V_i = attribute_values[i]
    r_i = len(V_i)

    #product = 1
    product = 0
    #numerator = math.factorial(r_i - 1)
    numerator = np.sum([np.log(b) for b in range(1, r_i)])

    # special case: q_i = 0
    if q_i == 0:
        js = ['special']
    else:
        js = range(q_i)

    for j in js:

        # initializing mask to send to alpha
        if j == 'special':
            mask = []
        else:
            mask = zip(pi, phi_i[j])

        # initializing counts that will increase with alphas
        N_ij = 0
        #inner_product = 1
        inner_product = 0

        for k in xrange(r_i):
            # adjusting mask for each k
            mask_with_k = mask + [[i, V_i[k]]]
            alpha_ijk = alpha(df, mask_with_k)
            N_ij += alpha_ijk
            #inner_product = inner_product*math.factorial(alpha_ijk)
            inner_product = inner_product + np.sum([np.log(b) for b in range(1,
             alpha_ijk + 1)])
        #denominator = math.factorial(N_ij + r_i - 1)
        denominator = np.sum([np.log(b) for b in range(1, N_ij + r_i)])
        #product = product*(numerator/denominator)*inner_product
        product = product + numerator - denominator + inner_product
    return product

# Pred = [[],[],[1],[1],[0,1,2]]
def k2(D, node_order, u=2):
    n = D.shape[1]
    assert len(node_order) == n, ("Node order is not correct length."
        "  It should have length %r" % n)
    attribute_values = vals_of_attributes(D, n)

    df = pd.DataFrame(D)
    OKToProceed = False
    parents = {}

    for i in xrange(n):
        OKToProceed = False
        pi = []
        pred = node_order[0:i]
        P_old = f(node_order[i], pi, attribute_values, df)
        if len(pred) > 0:
            OKToProceed = True
        while (OKToProceed is True and len(pi) < u):
            iters = [item for item in pred if item not in pi]
            if len(iters) > 0:
                f_to_max = {}
                for z_hat in iters:
                    f_to_max[z_hat] = f(node_order[i], pi + [z_hat],
                        attribute_values, df)
                z = max(f_to_max.iteritems(), key=operator.itemgetter(1))[0]
                P_new = f_to_max[z]

                if P_new > P_old:
                    print("P_new : %f, P_old : %f" %(P_new, P_old))
                    P_old = P_new
                    pi = pi + [z]
                else:
                    OKToProceed = False
            else:
                OKToProceed = False
        parents[node_order[i]] = pi
        print("Node ["+meta_data[i]+"]'s parent - "+str([meta_data[i] for i in pi]))
        # print("Node "+str(i)+"'s parent - "+str(pi))
    #print parents

    return parents
origin = {'True':1, 'False':0, 'Abnormal':0, 'Normal':1}
def toNumber(line):
    if not line : return;
    ret = line.split(',')[1:]
    for i in range(len(ret)):
        ret[i] = origin[ret[i]]
    return ret

def parse(args):
        path = args.D
        delimiter = ','
        # ans = {"Iris-setosa":0,"Iris-versicolor":1,"Iris-virginica":2}
        # delimiter = args.delimiter
        #try to read dataset
        try:
            f = open(path,"r")
        except:
            print("Invalid path : "+path)
            return None

        #meta-data
        #[Id,SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm,Species]
        meta_data = f.readline().rstrip('\n').rstrip('\r').split(delimiter)[1:] #exclude 'Id'
        D = list()

        #input database D
        #it is only for Iris data
        while True:
            data = toNumber(f.readline().rstrip('\n').rstrip('\r'))
            if not data : break;
            D.append(data)
        # D=np.array(D)
        # print(D)
        return np.array(D),meta_data

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''K2 In Serial:  Calculates
         the parent set for each node in your data file and returns a
         dictionary of the form{feature: [parent set]}.''')
    parser.add_argument('-D', nargs='?', default=None, help='''Path to csc file
         containing a 0/1 array with m observations (rows) and n features
         (columns).  A value of 1 represents the presence of that feature in
         that observation. One of --random and -D must be used.''')
    # parser.add_argument('--node_order', '-o', nargs='?', type=list,
    #     default=None, help='''A list of integers containing the column order
    #     of features in your matrix.  If not provided, order the features in
    #     accordance with their order in the file.''')
    # parser.add_argument('--random', '-r', action="store_true",
    #     help='''Include this option to calculate parents for a random matrix.
    #     If --random is included, -D and --node_order should be left out, and
    #     -m, --seed, and -n can be included.   One of --random and -D ust be
    #     used.''')
    # parser.add_argument('--seed', nargs='?', type=int, default=None,
    #         help='The seed for the random matrix.  Only use with --random')
    # parser.add_argument('-n', nargs='?', type=int, default='10',
    #         help='''The number of features in a random matrix.
    #         Default is 10.  Only use with --random''')
    # parser.add_argument('-m', nargs='?', type=int, default='100',
    #     help='''The number of observations in a random matrix.
    #     Default is 100. Only use with --random''')
    parser.add_argument('-u', nargs='?', type=int, default=2,
        help='''The maximum number of parents per feature.  Default is 2.
                Must be less than number of features.''')
    parser.add_argument('--outfile', nargs='?', default=None, help='''The
         output file where the dictionary of {feature: [parent set]} will be
         written''')
    args = parser.parse_args()

    u = args.u
    outfile = args.outfile

    # if args.random:
    #     n = args.n
    #     m = args.m
    #     if args.seed is not None:
    #         np.random.seed(args.seed)
    #     D = np.random.binomial(1, 0.7, size=(m, n))
    #     node_order = list(range(n))
    D, meta_data = parse(args)
    node_order = list(range(np.int32(D.shape[1])))

    start = time.time()
    parents = k2(D, node_order, u=u)
    end = time.time()

    ##### Outputs #####
    print "Serial computing time", end - start

    if args.outfile is not None:
        out = open(outfile, 'w')
        try:
            pickle.dump(parents, out)
        except RuntimeError:
            for key, item in parents.iteritems():
                strr = str(key) + ' ' + str(item) + '\n'
                out.write(strr)
    else:
        print parents
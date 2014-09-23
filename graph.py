#! /usr/bin/env python2

import numpy as np
import pylab as plt
import subprocess
import sys
import time

def run(num_attrs, num_examples, num_pairs, num_neighbors):
    open('extern.h', 'w').write('''\
#define NUM_ATTRS {}
#define NUM_EXAMPLES {}
#define NUM_PAIRS {}
#define NUM_NEIGHBORS {}
'''.format(num_attrs, num_examples, num_pairs, num_neighbors))
    subprocess.check_output('make && ./main.py data', shell=True)

    cu_time = time.time()
    subprocess.check_output('./main_cu')
    cu_time = time.time() - cu_time

    c_time = time.time()
    subprocess.check_output('./main_c')
    c_time = time.time() - c_time

    return [cu_time, c_time]

if 0:
    num_attrs = 1000
    num_pairs = 20000
    num_neighbors = 5
    xs = np.logspace(np.log10(100), np.log10(3000), 10).astype(np.int32)
    ys = []
    if 1:
        for num_examples in xs:
            print(num_examples)
            ys.append(run(num_attrs, num_examples, num_pairs, num_neighbors))

        ys = np.array(ys)
        np.save('tmp/examples', ys)

    print(ys)
    ys = np.load('tmp/examples.npy')
    ratio = ys[:,1] / ys[:,0]
    print(ratio)

    plt.xlabel('Number of examples')
    plt.ylabel('Runtime in seconds (log scale)')
    plt.grid()
    plt.plot(xs, ys[:,1], 'x-', label='CPU')
    plt.plot(xs, ys[:,0], 'x-', label='GPU')
    plt.legend()
    plt.yscale('log')
    plt.savefig('img/examples.png')

if 0:
    num_attrs = 1000
    num_examples = 1000
    num_neighbors = 5
    xs = np.logspace(np.log10(1000), np.log10(30000), 10)
    ys = []
    if 0:
        for num_pairs in xs:
            ys.append(run(num_attrs, num_examples, num_pairs, num_neighbors))

        ys = np.array(ys)
        np.save('tmp/pairs', ys)

    ys = np.load('tmp/pairs.npy')
    print(ys)
    ratio = ys[:,1] / ys[:,0]
    print(ratio)

    plt.xlabel('Number of attribute pairs')
    plt.ylabel('Runtime in seconds (log scale)')
    plt.grid()
    plt.plot(xs, ys[:,1], 'x-', label='CPU')
    plt.plot(xs, ys[:,0], 'x-', label='GPU')
    plt.legend()
    plt.yscale('log')
    plt.savefig('img/pairs.png')


if 1:
    num_attrs = 1000
    num_examples = 2000
    num_pairs = 20000
    xs = [1, 3, 5, 7, 9]
    ys = []
    if 1:
        for num_neighbors in xs:
            print(num_neighbors)
            ys.append(run(num_attrs, num_examples, num_pairs, num_neighbors))

        ys = np.array(ys)
        np.save('tmp/neighbors', ys)

    ys = np.load('tmp/neighbors.npy')
    print(ys)
    ratio = ys[:,1] / ys[:,0]
    print(ratio)

    plt.xlabel('Number of nearest neighbors')
    plt.ylabel('Runtime in seconds (log scale)')
    plt.grid()
    plt.plot(xs, ys[:,1], 'x-', label='CPU')
    plt.plot(xs, ys[:,0], 'x-', label='GPU')
    plt.legend()
    plt.yscale('log')
    plt.savefig('img/neighbors.png')

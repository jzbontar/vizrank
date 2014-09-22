#! /usr/bin/env python2

import numpy as np
import pylab as plt
import subprocess
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
    num_pairs = 5000
    num_neighbors = 5
    xs = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
    ys = []
    if 0:
        for num_examples in xs:
            ys.append(run(num_attrs, num_examples, num_pairs, num_neighbors))

        ys = np.array(ys)
        np.save('ys', ys)

    ys = np.load('ys.npy')
    ratio = ys[:,1] / ys[:,0]
    print(ratio)

    plt.xlabel('Number of examples')
    plt.ylabel('Runtime in seconds (log scale)')
    plt.grid()
    plt.plot(xs, ys[:,0], 'x-')
    plt.plot(xs, ys[:,1], 'x-')
    plt.yscale('log')
    plt.show()

num_attrs = 1000
num_examples = 1000
num_neighbors = 5
xs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
ys = []
if 1:
    for num_pairs in xs:
        ys.append(run(num_attrs, num_examples, num_pairs, num_neighbors))

    ys = np.array(ys)
    np.save('ys', ys)

ys = np.load('ys.npy')
ratio = ys[:,1] / ys[:,0]
print(ratio)

plt.xlabel('Number of pairs')
plt.ylabel('Runtime in seconds (log scale)')
plt.grid()
plt.plot(xs, ys[:,0], 'x-')
plt.plot(xs, ys[:,1], 'x-')
plt.yscale('log')
plt.show()

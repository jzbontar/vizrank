#! /usr/bin/env python2

import numpy as np
import sys

# grab definitions from extern.h
exec(open('extern.h').read().replace('#define ','').replace(' ', ' = '))

# generate data
if 'data' in sys.argv:
    np.random.seed(1)

    X = np.random.normal(size=(NUM_EXAMPLES, NUM_ATTRS)).astype(np.float32)
    Y = np.random.randint(0, 2, size=NUM_EXAMPLES)
    P = []

    for i in range(NUM_ATTRS):
        if len(P) < NUM_PAIRS:
            for j in range(i + 1, NUM_ATTRS):
                if len(P) < NUM_PAIRS:
                    P.append([i, j])

    open('data/X.bin', 'wb').write(X.tostring())
    open('data/Y.bin', 'wb').write(Y.astype(np.int32).tostring())
    open('data/P.bin', 'wb').write(np.array(P, dtype=np.int32).tostring())
    sys.exit()

X = np.memmap('data/X.bin', dtype=np.float32, mode='r', shape=(NUM_EXAMPLES, NUM_ATTRS))
Y = np.memmap('data/Y.bin', dtype=np.int32, mode='r', shape=(NUM_EXAMPLES,))
P = np.memmap('data/P.bin', dtype=np.int32, mode='r', shape=(NUM_PAIRS, 2))

D = np.empty((NUM_NEIGHBORS, 2), dtype=np.float32)
for attr1, attr2 in P:
    score = 0
    for i in range(NUM_EXAMPLES):
        for k in range(NUM_NEIGHBORS):
            D[k, 0] = 2e38
        for j in range(NUM_EXAMPLES):
            if i != j:
                max_k = 0
                for k in range(1, NUM_NEIGHBORS):
                    if D[k, 0] > D[max_k, 0]:
                        max_k = k
                dist = np.sqrt((X[i, attr1] - X[j, attr1])**2 + (X[i, attr2] - X[j, attr2])**2)
                if dist < D[max_k, 0]:
                    D[max_k, 0] = dist
                    D[max_k, 1] = Y[j]
        for k in range(NUM_NEIGHBORS):
            if Y[i] == D[k, 1]:
                score += 1
    print attr1, attr2, score

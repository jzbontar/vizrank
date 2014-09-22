#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "extern.h"

int main(void)
{
	int Xfd, Yfd, Pfd;
	float *X, *D, dist, d1, d2;
	int *Y, *P, i, j, k, p, attr1, attr2, score, max_k;

	Xfd = open("data/X.bin", O_RDONLY);
	Yfd = open("data/Y.bin", O_RDONLY);
	Pfd = open("data/P.bin", O_RDONLY);

	X = mmap(NULL, NUM_EXAMPLES * NUM_ATTRS * sizeof(float), PROT_READ, MAP_SHARED, Xfd, 0);
	Y = mmap(NULL, NUM_EXAMPLES * sizeof(int), PROT_READ, MAP_SHARED, Yfd, 0);
	P = mmap(NULL, NUM_PAIRS * 2 * sizeof(int), PROT_READ, MAP_SHARED, Pfd, 0);

	D = malloc(NUM_NEIGHBORS * 2 * sizeof(float));
	for (p = 0; p < NUM_PAIRS; p++) {
		attr1 = P[p * 2];
		attr2 = P[p * 2 + 1];
		score = 0;
		for (i = 0; i < NUM_EXAMPLES; i++) {
			for (k = 0; k < NUM_NEIGHBORS; k++) {
				D[k * 2] = 2e38;
			}
			for (j = 0; j < NUM_EXAMPLES; j++) {
				if (i != j) {
					max_k = 0;
					for (k = 1; k < NUM_NEIGHBORS; k++) {
						if (D[k * 2] > D[max_k * 2]) {
							max_k = k;
						}
					}
					d1 = X[i * NUM_ATTRS + attr1] - X[j * NUM_ATTRS + attr1];
					d2 = X[i * NUM_ATTRS + attr2] - X[j * NUM_ATTRS + attr2];
					dist = sqrtf(d1 * d1 + d2 * d2);
					if (dist < D[max_k * 2]) {
						D[max_k * 2] = dist;
						D[max_k * 2 + 1] = Y[j];
					}
				}
			}
			for (k = 0; k < NUM_NEIGHBORS; k++) {
				if (Y[i] == D[k * 2 + 1]) {
					score++;
				}
			}
		}
		printf("%d %d %d\n", attr1, attr2, score);
	}
	return 0;
}

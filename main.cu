#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "extern.h"

#define TB 128
#define CUDA_ASSERT(x) (assert((x) == cudaSuccess))

__global__ void rank(float *X, int *Y, int *P, int *S)
{
	int id = blockIdx.x * blockDim.x + threadIdx.x;
	float D[NUM_NEIGHBORS * 2];

	if (id < NUM_PAIRS) {
		int attr1 = P[id * 2];
		int attr2 = P[id * 2 + 1];
		int score = 0;
		for (int i = 0; i < NUM_EXAMPLES; i++) {
			for (int k = 0; k < NUM_NEIGHBORS; k++) {
				D[k * 2] = 2e38;
			}
			for (int j = 0; j < NUM_EXAMPLES; j++) {
				if (i != j) {
					int max_k = 0;
					for (int k = 1; k < NUM_NEIGHBORS; k++) {
						if (D[k * 2] > D[max_k * 2]) {
							max_k = k;
						}
					}
					float d1 = X[i * NUM_ATTRS + attr1] - X[j * NUM_ATTRS + attr1];
					float d2 = X[i * NUM_ATTRS + attr2] - X[j * NUM_ATTRS + attr2];
					float dist = sqrtf(d1 * d1 + d2 * d2);
					if (dist < D[max_k * 2]) {
						D[max_k * 2] = dist;
						D[max_k * 2 + 1] = Y[j];
					}
				}
			}
			for (int k = 0; k < NUM_NEIGHBORS; k++) {
				if (Y[i] == D[k * 2 + 1]) {
					score++;
				}
			}
		}
		S[id] = score;
	}
}

int main(void)
{
	int Xfd, Yfd, Pfd, *hY, *hP, *dY, *dP, *hS, *dS;
	float *hX, *dX;
	
	Xfd = open("data/X.bin", O_RDONLY);
	Yfd = open("data/Y.bin", O_RDONLY);
	Pfd = open("data/P.bin", O_RDONLY);

	hX = (float *)mmap(NULL, NUM_EXAMPLES * NUM_ATTRS * sizeof(float), PROT_READ, MAP_SHARED, Xfd, 0);
	hY = (int *)mmap(NULL, NUM_EXAMPLES * sizeof(int), PROT_READ, MAP_SHARED, Yfd, 0);
	hP = (int *)mmap(NULL, NUM_PAIRS * 2 * sizeof(int), PROT_READ, MAP_SHARED, Pfd, 0);
	hS = (int *)malloc(NUM_PAIRS * sizeof(int));

	CUDA_ASSERT(cudaMalloc(&dX, NUM_EXAMPLES * NUM_ATTRS * sizeof(float)));
	CUDA_ASSERT(cudaMalloc(&dY, NUM_EXAMPLES * sizeof(int)));
	CUDA_ASSERT(cudaMalloc(&dP, NUM_PAIRS * 2 * sizeof(int)));
	CUDA_ASSERT(cudaMalloc(&dS, NUM_PAIRS * sizeof(int)));

	CUDA_ASSERT(cudaMemcpy(dX, hX, NUM_EXAMPLES * NUM_ATTRS * sizeof(float), cudaMemcpyHostToDevice));
	CUDA_ASSERT(cudaMemcpy(dY, hY, NUM_EXAMPLES * sizeof(int), cudaMemcpyHostToDevice));
	CUDA_ASSERT(cudaMemcpy(dP, hP, NUM_PAIRS * 2 * sizeof(int), cudaMemcpyHostToDevice));

	rank<<<(NUM_PAIRS - 1) / TB + 1, TB>>>(dX, dY, dP, dS);
	CUDA_ASSERT(cudaMemcpy(hS, dS, NUM_PAIRS * sizeof(int), cudaMemcpyDeviceToHost));
	for (int i = 0; i < NUM_PAIRS; i++) {
		printf("%d\n", hS[i]);
	}
	
	return 0;
}

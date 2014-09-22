#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "extern.h"

int main(void)
{
	int Xfd, Yfd, Pfd;
	float *X;
	int *Y, *P;

	Xfd = open("data/X.bin", O_RDONLY);
	Yfd = open("data/Y.bin", O_RDONLY);
	Pfd = open("data/P.bin", O_RDONLY);

	X = mmap(NULL, NUM_EXAMPLES * NUM_ATTRS * sizeof(float), PROT_READ, MAP_SHARED, Xfd, 0);
	Y = mmap(NULL, NUM_EXAMPLES * sizeof(int), PROT_READ, MAP_SHARED, Yfd, 0);
	P = mmap(NULL, NUM_PAIRS * 2 * sizeof(int), PROT_READ, MAP_SHARED, Pfd, 0);

	close(Xfd);
	close(Yfd);
	close(Pfd);

	printf("%f\n", X[0]);
	printf("%d\n", Y[0]);
	printf("%d\n", P[0]);

	return 0;
}

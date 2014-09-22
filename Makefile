all: main_c main_cu

main_c: main.c extern.h
	gcc -Wall -O3 -lm main.c -o main_c

main_cu: main.cu extern.h
	nvcc main.cu -o main_cu

clean:
	rm -f main_c

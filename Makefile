main_c: main.c extern.h
	gcc -Wall -O3 -lm main.c -o main_c

clean:
	rm -f main_c

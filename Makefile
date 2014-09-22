main_c: main.c extern.h
	gcc -Wall -O2 main.c -o main_c

clean:
	rm -f main_c

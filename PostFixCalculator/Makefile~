cc = gcc
flags = -g
rpn: rpn.o
	$(cc) $(flags) rpn.o -o rpn
rpn.o: rpn.c rpn.h
	$(cc) $(flags) -c rpn.c
clean:
	rm -f *.o

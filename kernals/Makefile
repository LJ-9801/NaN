CC = clang
CFLAGS = -dynamiclib -fopenmp -std=gnu99 -O2 -Wall
DEPS = mat_gen.h
MKDIR_P = mkdir
OUT_DIR = ../kernals/build


mat_gen.dylib: mat_gen.c $(DEPS)
	$(MKDIR_P) $(OUT_DIR)
	$(CC) $(CFLAGS) $< -o $(OUT_DIR)/$@
	
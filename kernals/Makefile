uname_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')
uname_M := $(shell sh -c 'uname -m 2>/dev/null || echo not')
$(info uname_S is $(uname_S))
$(info uname_M is $(uname_M))

CC = clang
CFLAGS = -fopenmp -std=gnu99 -O2 -Wall -lm
DEPS = mat_gen.h
MKDIR_P = mkdir
OUT_DIR = ../kernals/build


ifeq ($(uname_S),Darwin)
# Mac OS X
CFLAGS += -dynamiclib
mat_gen.dylib: mat_gen.c $(DEPS)
	$(MKDIR_P) $(OUT_DIR)
	$(CC) $(CFLAGS) $< -o $(OUT_DIR)/$@
endif
ifeq ($(uname_S),Linux)
# Linux
CFLAGS += -shared -fPIC
mat_gen.so: mat_gen.c $(DEPS)
	$(MKDIR_P) $(OUT_DIR)
	$(CC) $(CFLAGS) $< -o $(OUT_DIR)/$@
endif

	
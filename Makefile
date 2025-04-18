# Compiler and flags
CC = gcc
CFLAGS = -Wall -g -fPIC
LDFLAGS = -shared

# Target shared library
TARGET_LIB = rijndael.so

# Platform-specific settings
ifeq ($(OS),Windows_NT)
    RM = cmd /C del /Q
    TARGET_LIB_PATH = rijndael.so
else
    RM = rm -f
    TARGET_LIB_PATH = rijndael.so
endif

# Default target
all: $(TARGET_LIB)

# Object files
rijndael.o: rijndael.c rijndael.h
	$(CC) $(CFLAGS) -c rijndael.c

# Shared library
$(TARGET_LIB): rijndael.o
	$(CC) $(LDFLAGS) -o $(TARGET_LIB) rijndael.o

# Clean up
clean:
	$(RM) *.o $(TARGET_LIB_PATH)
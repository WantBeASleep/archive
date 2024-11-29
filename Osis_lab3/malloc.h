// fixCommitso
#include <string.h>
#ifndef SRC_MALLOC_H_
#define SRC_MALLOC_H_

void *malloc(size_t size);
void *calloc(size_t number, size_t size);
void free(void *p);
void *realloc(void *p, size_t size);


#endif
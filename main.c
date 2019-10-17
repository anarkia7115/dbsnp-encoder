#include <stdio.h>

struct SnpKey {
    int chr;
    int pos;
    int* refa;
    int* refc;
    int* refg;
    int* reft;
    int* alta;
    int* altc;
    int* altg;
    int* altt;
};

struct SnpKey;

int main() {
    printf("Hello world!");
}
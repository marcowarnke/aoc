#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {

    FILE* file = fopen(argv[1], "r");
    if(!file) {
        perror("File opening failed");
        return EXIT_FAILURE;
    }

    int num = 0;
    int current_freq = 0;
    while (!feof(file)) {
        fscanf(file, "%d\n", &num);
        current_freq += num;
    }

    printf("resulting frequency: %d\n", current_freq);

    fclose(file);

    return EXIT_SUCCESS;
}


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool contains(const int* buffer, const size_t buffer_size, const int number) {
    for (size_t i = 0; i < buffer_size; i++) {
        if (buffer[i] == number)
            return true;
    }
    return false;
}

int part1(FILE* file) {
    int num = 0;
    int current_freq = 0;
    while (!feof(file)) {
        fscanf(file, "%d\n", &num);
        current_freq += num;
    }
    return current_freq;
}

int part2(FILE* file) {
    const size_t buffer_size = 1024 * 1024;
    int buffer[buffer_size];
    size_t buffer_index = 0;

    int num = 0;
    int current_freq = 0;
    while (true) {
        if (feof(file))
            rewind(file);

        fscanf(file, "%d\n", &num);
        current_freq += num;

        if (contains((int*) buffer, buffer_index, current_freq))
            return current_freq;

        buffer[buffer_index] = current_freq;
        buffer_index++;
    }
}

int main(int argc, char** argv) {

    FILE* file = fopen(argv[1], "r");
    if(!file) {
        perror("File opening failed");
        return EXIT_FAILURE;
    }

    printf("resulting frequency: %d\n", part1(file));
    printf("first repeating frequency: %d\n", part2(file));

    fclose(file);

    return EXIT_SUCCESS;
}


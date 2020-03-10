#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool check_letters(const char* s, const unsigned int count) {
    const size_t size = strlen(s);
    for (size_t i = 0; i < size; i++) {
        unsigned int counter = 0;
        const char c = s[i];
        for (size_t j = 0; j < size; j++) {
            if (c == s[j])
                counter++;
        }

        if (counter == count) {
            printf("%d - %c in %s\n", count, s[i], s);
            return true;
        }
    }
    return false;
}

bool has_exactly_two_of_letter(const char* s) {
    return check_letters(s, 2);
}

bool has_exactly_three_of_letters(const char* s) {
    return check_letters(s, 3);
}

int main(int argc, const char** argv) {

    if (argc < 2) {
        fprintf(stderr, "missing input argument!\n");
        return EXIT_SUCCESS;
    }

    FILE* file = fopen(argv[1], "r");
    if (!file) {
        perror("failed to open file!\n");
        return EXIT_FAILURE;
    }

    char buffer[32];
    unsigned int twos_count = 0;
    unsigned int threes_count = 0;
    while (!feof(file)) {
        fscanf(file, "%s\n", buffer);
        if (has_exactly_two_of_letter(buffer))
            twos_count++;
        if (has_exactly_three_of_letters(buffer))
            threes_count++;
    }

    printf("twos * threes = checksum\n%d * %d = %d\n", twos_count, threes_count, twos_count * threes_count);

    return EXIT_SUCCESS;
}


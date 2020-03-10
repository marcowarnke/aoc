#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

/* s, t: two strings; ls, lt: their respective length */
/* copied from somewhere... */
int lev_distance(const char *s, int ls, const char *t, int lt)
{
        int a, b, c;
 
        /* if either string is empty, difference is inserting all chars 
         * from the other
         */
        if (!ls) return lt;
        if (!lt) return ls;
 
        /* if last letters are the same, the difference is whatever is
         * required to edit the rest of the strings
         */
        if (s[ls - 1] == t[lt - 1])
                return lev_distance(s, ls - 1, t, lt - 1);
 
        /* else try:
         *      changing last letter of s to that of t; or
         *      remove last letter of s; or
         *      remove last letter of t,
         * any of which is 1 edit plus editing the rest of the strings
         */
        a = lev_distance(s, ls - 1, t, lt - 1);
        b = lev_distance(s, ls,     t, lt - 1);
        c = lev_distance(s, ls - 1, t, lt    );
 
        if (a > b) a = b;
        if (a > c) a = c;
 
        return a + 1;
}

void part2(FILE* file) {
    rewind(file);

    char buffer[64];
    char** ids = malloc(1024 * sizeof(char*));
    size_t lines = 0;
    for (size_t i = 0; !feof(file); i++) {
        fscanf(file, "%s\n", buffer);
        printf("buf: %s\n", buffer);
        ids[i] = malloc(strlen(buffer) * sizeof(char));
        //TODO copy into the ids[i]
        lines++;
    }

    for (size_t i = 0; i < lines; i++) {
        printf("%lu : %lu : %s\n", i, strlen(ids[i]), ids[i]);
    }

    for (size_t i = 0; i < lines; i++) {
        for (size_t j = 0; j < lines; j++) {
            int alen = strlen(ids[i]);
            int blen = strlen(ids[j]);
            int distance = lev_distance(ids[i], alen, ids[j], blen);
            if (distance == 1)
                printf("found words %s and %s\n", ids[i], ids[j]);
        }
    }

    free(ids);
}

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
    part2(file);
    fclose(file);

    return EXIT_SUCCESS;
}


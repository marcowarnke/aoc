#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FABRIC_SIZE 1024
#define CLAIM_COUNTS 2048
#define MAX_CLAIMS_PER_TILE 1024

typedef struct {
  unsigned int id, spc_left, spc_top, width, height;
  bool has_overlaps;
} claim_t;

typedef struct {
  size_t count_claims;
  claim_t **claims;
} fab_tile_t;

static void claim_fabric(void *tfabric, claim_t *claim) {
  unsigned int(*fabric)[FABRIC_SIZE] = tfabric;
  for (size_t i = claim->spc_top; i < (claim->spc_top + claim->height); i++) {
    for (size_t j = claim->spc_left; j < (claim->spc_left + claim->width);
         j++) {
      fabric[i][j]++;
      if (fabric[i][j] > 1) {
        claim->has_overlaps = true;
      }
    }
  }
}

static void claim_tiles(void *tfabric, claim_t *claim) {
  fab_tile_t(*fabric)[FABRIC_SIZE] = tfabric;
  for (size_t i = claim->spc_top; i < (claim->spc_top + claim->height); i++) {
    for (size_t j = claim->spc_left; j < (claim->spc_left + claim->width);
         j++) {
      fabric[i][j].claims[fabric[i][j].count_claims] = claim;
      fabric[i][j].count_claims++;
      if (fabric[i][j].count_claims > 1) {
        for (size_t k = 0; k < fabric[i][j].count_claims; k++) {
          fabric[i][j].claims[k]->has_overlaps = true;
        }
      }
    }
  }
}

static unsigned int count_conflicting_claims(void *tfabric) {
  unsigned int count = 0;
  unsigned int(*fabric)[FABRIC_SIZE] = tfabric;
  for (size_t i = 0; i < FABRIC_SIZE; i++) {
    for (size_t j = 0; j < FABRIC_SIZE; j++) {
      if (fabric[i][j] > 1)
        count++;
    }
  }
  return count;
}

static void print_single_claims(claim_t *claims, size_t sc) {
  for (size_t i = 1; i <= sc; i++) {
    if (!claims[i].has_overlaps)
      printf("claim with id %d\n", claims[i].id);
  }
}

static void part1(FILE *file) {
  // create the fabric like a game board
  unsigned int fabric[FABRIC_SIZE][FABRIC_SIZE] = {0};
  claim_t *claims = calloc(CLAIM_COUNTS, sizeof(claim_t));
  size_t claim_count = 0;
  for (unsigned int id, spc_left, spc_top, width, height;
       fscanf(file, "#%u @ %u,%u: %ux%u\n", &id, &spc_left, &spc_top, &width,
              &height) == 5;) {
    claim_t claim = {.id = id,
                     .spc_left = spc_left,
                     .spc_top = spc_top,
                     .width = width,
                     .height = height,
                     .has_overlaps = false};
    memcpy(&claims[id], &claim, sizeof(claim_t));
    claim_count++;
    claim_fabric(&fabric, &claims[id]);
  }
  printf("overlapping sqr inches: %d\n", count_conflicting_claims(&fabric));
  free(claims);
}

static void init_tiles(void *tfabric) {
  fab_tile_t(*fabric)[FABRIC_SIZE] = tfabric;
  for (size_t i = 0; i < FABRIC_SIZE; i++) {
    for (size_t j = 0; j < FABRIC_SIZE; j++) {
      fabric[i][j].claims = calloc(MAX_CLAIMS_PER_TILE, sizeof(claim_t *));
    }
  }
}

static void part2(FILE *file) {
  // create the fabric like a game board
  fab_tile_t *fabric[FABRIC_SIZE][FABRIC_SIZE] = {0};
  claim_t *claims = calloc(CLAIM_COUNTS, sizeof(claim_t));
  size_t claim_count = 0;
  init_tiles(fabric);
  for (unsigned int id, spc_left, spc_top, width, height;
       fscanf(file, "#%u @ %u,%u: %ux%u\n", &id, &spc_left, &spc_top, &width,
              &height) == 5;) {
    claim_t claim = {.id = id,
                     .spc_left = spc_left,
                     .spc_top = spc_top,
                     .width = width,
                     .height = height,
                     .has_overlaps = false};
    memcpy(&claims[id], &claim, sizeof(claim_t));
    claim_count++;
    claim_tiles(&fabric, &claims[id]);
  }
  print_single_claims(claims, claim_count);
  free(claims);
}

int main(int argc, const char **argv) {
  if (argc < 2) {
    fprintf(stderr, "missing input argument!\n");
    return EXIT_FAILURE;
  }

  fopen(NULL, "r");

  FILE *file = fopen(argv[1], "r");
  if (!file) {
    perror("failed to open file!\n");
    return EXIT_FAILURE;
  }

  part1(file);
  rewind(file);
  part2(file);

  fclose(file);
  return EXIT_SUCCESS;
}

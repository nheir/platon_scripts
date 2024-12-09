// PL:title=Création d'un ensemble

/* PL:statement==
Écrire une fonction `int creation(Ensemble *ens, int taille_max)` qui crée in ensemble vide pouvant conteniur jusqu'à `taille_max` éléments.
La fonction renverra 1 en cas de succès et 0 sinon.

```c
typedef struct {
    int *elements;
    int carninal;
    int capacite;
} Ensemble;
```
PL:== */

// PL:tag=alloc|struct|arrays

// PL:code_before==
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void *alloc(void *ptr, size_t size) {
    if (ptr && size == 0) {
        free(ptr);
        return NULL;
    }
    if (ptr == NULL) {
        fprintf(stderr, "# Allocation de %zu octets\n", size);
        return calloc(1, size);
    }
    fprintf(stderr, "# Réallocation de %zu octets\n", size);
    return realloc(ptr, size);
}

#define malloc(size) alloc(NULL, size)
#define calloc(nb, size) alloc(NULL, (size)*(nb))
#define realloc(ptr, size) alloc(ptr, size)
#define free(ptr) alloc(ptr, 0)

typedef struct {
    int *elements;
    int cardinal;
    int capacite;
} Ensemble;
// PL:==

// PL:soluce==
int creation(Ensemble *ens, int taille_max) {
    ens->elements = malloc(sizeof(int) * taille_max);
    if (ens->elements == NULL)
        return 0;
    ens->capacite = taille_max;
    ens->cardinal = 0;
    return 1;
}
// PL:==

// PL:code==
/* a vous */
// PL:==

// PL:code_after==
void affiche(Ensemble e) {
    printf("Cardinalité : %d\n", e.cardinal);
    printf("Capacité    : %d\n", e.capacite);
    printf("Contenu     :");
    for (int i = 0; i < e.cardinal; i++) {
        printf(" %d", e.elements[i]);
    }
    printf("\n");
}

void destruction(Ensemble *ens) {
    if (ens->elements != NULL) {
        free(ens->elements);
        ens->elements = NULL;
        ens->cardinal = 0;
        ens->capacite = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <taille>\n", argv[0]);
        return 1;
    }

    int taille = atoi(argv[1]);

    Ensemble ens;
    if (creation(&ens, taille)) {
        printf("Initialisation sans erreur\n");
        affiche(ens);
        destruction(&ens);
    } else {
        printf("Initialisation avec erreur\n");
    }

    return 0;
}
// PL:==

/* PL:checks_args_stdin==
[
    ["Test 10", ["10"], ""],
    ["Test 1000", ["1000"], ""],
    ["Test 1000000", ["1000000"], ""],
]
PL:== */

#include <time.h>
#include <stdio.h>
#include "../lib/rngs.h"
#include "../lib/rvgs.h"

#define TAM 50

int main(int argc, char *argv[])
{
	int i;
	int vet[TAM];
	
	printf("Casa inicial selecionada: %s%s\n", argv[1], argv[2]);
	
	PlantSeeds(time(NULL));
	
	
	for(i = 0; i < TAM; i++)
	{
		vet[i] = (int) Equilikely(0.0, 1.0);
	}
	
	for(i = 0; i < TAM; i++)
	{
		printf("%d\n", vet[i]);
	}
	return 0;
}

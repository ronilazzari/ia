# Projeto final de IA

Este projeto resolverá o problema do cavalo de xadrez por meio de algoritmo genético.

A abordagem para esta implementação seguirá aquela usada por [Gordon e Slocum](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1331065&isnumber=29392).


## Como compilar este projeto

Há duas maneiras de compilar o código-fonte deste projeto.

Os dois métodos são explicados a seguir.

### Método 1: usando cmake & make

Confira se você possui os programas *cmake* e *make* instalados em seu computador. Feito isso, copie todos os arquivos contidos no diretório _proj_. Em seguida, dentro de _proj_, execute os seguintes comandos no console:

1. `$ cmake .`

2. `$ make`

Pronto! O programa principal assim como a biblioteca deveriam ser gerados automagicamente. Por enquanto o executável se encontra em proj/src.

TODO: ainda me falta alterar o arquivo CMakeLists.txt para criar os binários fora dos diretórios com os códigos-fontes.

### Método 2: na unha

#### 1. Compilando as bibliotecas

O passo-a-passo para compilar as duas bibliotecas feitas por [Steve Park](http://www.cs.wm.edu/~va/software/park/park.html) foi baseado no seguinte [link](http://www.cs.dartmouth.edu/~campbell/cs50/buildlib.html).

1. Primeiramente navegue, dentro de _proj_, até o diretório _lib_

2. Por enquanto, dentro de _proj_/_lib_ deveria haver somente os seguintes arquivos:

	`CMakeLists.txt  README.md  rngs.c  rngs.h  rvgs.c  rvgs.h`

3. Compile todos os arquivos terminados por _.c_ com o seguinte comando:

	`$ gcc -Wall -pedantic-errors -c *.c`

	> Uma mensagem de _warning_ vai aparecer, mas pode ser ignorada :-)

4. Agora, dois novos arquivos com extensão _.o_ deveriam aparecer no diretório _lib_:

	`CMakeLists.txt  README.md  rngs.c  rngs.h  **rngs.o**  rvgs.c  rvgs.h  **rvgs.o**`

5. Em seguida, empacotemos os dois novos arquivos em um só chamado _librandom.a_:

	`$ ar -cvq librandom.a *.o`

6. Pronto! Os arquivos existentes agora em seu diretório _lib_ deveriam ser os seguintes:

	`CMakeLists.txt  README.md  rngs.h  rvgs.c  rvgs.o`

	`librandom.a     rngs.c     rngs.o  rvgs.h`

#### 2. Compilando o arquivo principal

Vá até o diretório _src_ dentro de _proj_ e execute os seguintes passos:

1. (...)

2. (...)

3. (...)

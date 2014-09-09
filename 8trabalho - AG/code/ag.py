#!/usr/bin/python

import random
from math import *

from param import *

def gera_individuo_aleatorio():
	
	return (''.join(random.choice(string_base) for j in range(TamanhoDaString)))

def gera_populacao(TamanhoDaPopulacao):
	
	a = []
	
	for i in range(TamanhoDaPopulacao):
		a.insert(i, gera_individuo_aleatorio())
	
	return a

def binario_em_decimal(Lista):
	
	a = []
	
	for i in range(len(Lista)):
		a.insert(i, int(Lista[i], 2))
	
	return a

def calcula_aptidao(Cromossomo_Individuo):

	return (abs((Cromossomo_Individuo)*(sin(sqrt(Cromossomo_Individuo)))))

def calcula_aptidao_total(Dicionario):

	aptidao_total = 0
	
	for i in range(len(Dicionario)):
	
		aptidao_total = aptidao_total + Dicionario[i]
	
	return aptidao_total

def associa_aptidao(Populacao):	

	dicionario = {}

	for i in range(len(Populacao)):
		
		dicionario[i] = calcula_aptidao(Populacao[i])	

	return dicionario
	
def associa_probabilidade(Dicionario, AptidaoTotal):

	for i in range(len(Dicionario)):
		
		Dicionario[i] = Dicionario[i]/AptidaoTotal
	
	return Dicionario

def associa_prob_cumulativa(Dicionario):

	prob_acumulada = 0
	
	for i in range(len(Dicionario)):
		
		prob_acumulada = prob_acumulada + Dicionario[i]
		
		Dicionario[i] = prob_acumulada
	
	return Dicionario

def seleciona(Populacao, Dicionario):
	
	PopulacaoSelecionada = []
	
	DicionarioAuxiliar = {}
	
	ListaAuxiliar = []
	
	ListaAuxiliar = Dicionario.values()
	
	indice = 0
	
	for i in range(len(Dicionario)):
		
		DicionarioAuxiliar[Dicionario[i]] = i	
	
	for i in range(len(Populacao)):
		
		numero_aleatorio = random.uniform(0.0,1.0)
		
		ListaAuxiliar.append(numero_aleatorio)
		
		ListaAuxiliar.sort()
		
		indice = ListaAuxiliar.index(numero_aleatorio)
		
		if(indice == (len(ListaAuxiliar) - 1)):
		
			indice = indice - 1
		
		ListaAuxiliar.remove(numero_aleatorio)
		
		PopulacaoSelecionada.insert(i, Populacao[DicionarioAuxiliar[ListaAuxiliar[indice]]])
	
	return PopulacaoSelecionada

def cruza(Populacao):

	pai = ""
	mae = ""
	
	indice_pai = random.choice(range(len(Populacao)))

	indice_mae = random.choice(range(len(Populacao)))
	
	pai = Populacao[indice_pai]
	mae = Populacao[indice_mae]
	
	indice_cruzamento = random.choice(range(0,(len(pai)-2)))
	
	pai = list(pai)
	mae = list(mae)
	
	for i in range(indice_cruzamento, len(pai)):
		
		aux = ''
		
		aux = pai[i]
		
		pai[i] = mae[i]
		
		mae[i] = aux
	
	pai = ''.join(pai)
	mae = ''.join(mae)
	
	Populacao[indice_pai] = pai
	Populacao[indice_mae] = mae
	
	return Populacao

def muta(Populacao):
	
	indice_populacao = random.randint(0, (len(Populacao)-1))
	
	auxilio = Populacao[indice_populacao]
	
	auxilio = list(auxilio)
	
	indice_individuo = random.randint(0, (len(auxilio)-1))
	
	if (auxilio[indice_individuo] == '1'):
		
		auxilio[indice_individuo] = '0'
	
	else:
		auxilio[indice_individuo] = '1'
	
	auxilio = ''.join(auxilio)

	Populacao[indice_populacao] = auxilio
	
	return Populacao

def muta2(Populacao):
	
	auxilio = ''
	
	for i in range(len(Populacao)):
		
		prob_mutacao = random.uniform(0.0,1.0)
		
		if(prob_mutacao <= pm):
		
			auxilio = Populacao[i]
	
			auxilio = list(auxilio)
			
			for j in range(len(auxilio)):

				prob_mutacao2 = random.uniform(0.0,1.0)
				
				if (prob_mutacao2 <= pm):
	
					if (auxilio[j] == '1'):
		
						auxilio[j] = '0'
	
					else:
				
						auxilio[j] = '1'
	
			auxilio = ''.join(auxilio)

			Populacao[i] = auxilio
	
	return Populacao

pop = gera_populacao(100)

print pop, "\n"


numero_geracao = 0

while (numero_geracao < 70):

	a = binario_em_decimal(pop)

	print a, "\n"

	dic = associa_aptidao(a)

	print dic, "\n"

	aptotal = calcula_aptidao_total(dic)

	print aptotal, "\n"

	dic = associa_probabilidade(dic, aptotal)

	print dic, "\n"

	dic = associa_prob_cumulativa(dic)

	print dic, "\n"
	
	pop = seleciona(pop, dic)
	
	print pop
	
	for i in range(len(pop)):

		prob_cruzamento = random.uniform(0.0,1.0)
		
		if(prob_cruzamento <= pc):

			pop = cruza(pop)
	
	print pop

	pop = muta2(pop)	
#	for i in range(len(pop)):
#		
#		prob_mutacao = random.uniform(0.0,1.0)
#		
#		if(prob_mutacao < pm):

#			pop = muta(pop)
	
	print pop
	
	numero_geracao = numero_geracao + 1

print pop

a = binario_em_decimal(pop)

print a

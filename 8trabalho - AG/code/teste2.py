#!/usr/bin/python

import random

from math import pow

string_base = '01'
TamanhoDaString = 12

def gera_individuo_aleatorio():
	
	return (''.join(random.choice(string_base) for j in range(TamanhoDaString)))

def gera_populacao(TamanhoDaPopulacao):
	
	a = []
	
	for i in range(TamanhoDaPopulacao):
		a.insert(i, gera_individuo_aleatorio())
	
	return a

def binario_em_decimal(String):

	decimal = 0
	
	for i in range(len(String)):
		
		decimal = decimal + int(String[(len(String) - 1) - i])*pow(2, potencia)
		
		potencia = potencia + 1	
	
	return decimal

def binario_em_decimal2(Lista):
	
	a = []
	
	for i in range(len(Lista)):
		a.insert(i, binario_em_decimal(Lista[i]))
	
	return a

populacao = gera_populacao(10)

populacao_em_dec = binario_em_decimal2(populacao)

print populacao_em_dec

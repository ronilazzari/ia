#!/usr/bin/python

from constants import *

import csv
import numpy

x1 = []
x2 = []
x3 = []
x4 = []
target = []

peso = [0.2, 0.3, 0.4, 0.5]
bias = 0.1
tolerancia = 1.0

ciclos = 0

ErroAntes = 0.0
ErroAgora = 100.0

saida = []

def calculaSaidaLiquida(VetorEntrada0, VetorEntrada1, VetorEntrada2, VetorEntrada3, VetorPeso, ValorBias):
	
	SaidaLiquida = 0.0
	
	SaidaLiquida = VetorEntrada0*VetorPeso[0] + VetorEntrada1*VetorPeso[1] + VetorEntrada2*VetorPeso[2] + VetorEntrada3*VetorPeso[3] + ValorBias

	return SaidaLiquida
	
def atualizaBias(ValorBias, TaxaAprendizagem, Target, SaidaCalculada):

	NovoBias = 0.0
	NovoBias = ValorBias + (TaxaAprendizagem*(Target - SaidaCalculada))
	return NovoBias
	
def atualizaPesos(ValorPeso, TaxaAprendizagem, Target, SaidaCalculada, ValorEntrada):

	NovoPeso = 0.0
	NovoPeso = ValorPeso + (TaxaAprendizagem*(Target - SaidaCalculada)*ValorEntrada)
	return NovoPeso

def calculaErro(Target, SaidaCalculada):
	
	Erro = 0.0
	
	for i in range(TAM_VETOR_ENTRADA):
		
		Erro = Erro + (target[i] - SaidaCalculada[i])
	
	return Erro

def calculaErroSucessivo(ErroAtual, ErroAnterior):
	
	ErroSucessivo = ErroAtual - ErroAnterior
	
	return ErroSucessivo

def calculaErroQuadratico(Target, SaidaCalculada):

	ErroQuadratico = 0.0
	
	for i in range(TAM_VETOR_ENTRADA):
	
		ErroQuadratico = ErroQuadratico + (Target[i] - SaidaCalculada[i])*(Target[i] - SaidaCalculada[i])
	
	return ErroQuadratico


# Agora comeca a funcao principal realmente...

with open('tabtreinamento.csv', 'r') as csvfile:
	leitora = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in leitora:
		x1.append(row[0])
		x2.append(row[1])
		x3.append(row[2])
		x4.append(row[3])
		target.append(row[4])

x1.remove('x1')
x2.remove('x2')
x3.remove('x3')
x4.remove('x4')
target.remove('d')

for i in range(TAM_VETOR_ENTRADA):
	x1[i] = float(x1[i])
	x2[i] = float(x2[i])
	x3[i] = float(x3[i])
	x4[i] = float(x4[i])
	target[i]  = float(target[i])

while(abs(tolerancia) > PRECISAO):
	
	for i in range(TAM_VETOR_ENTRADA):
		
		saida.insert(i, calculaSaidaLiquida(x1[i], x2[i], x3[i], x4[i], peso, bias))
		
		bias = atualizaBias(bias, APRENDIZAGEM, target[i], saida[i])
		
		peso[0] = atualizaPesos(peso[0], APRENDIZAGEM, target[i], saida[i], x1[i])
		
		peso[1] = atualizaPesos(peso[1], APRENDIZAGEM, target[i], saida[i], x2[i])
		
		peso[2] = atualizaPesos(peso[2], APRENDIZAGEM, target[i], saida[i], x3[i])

		peso[3] = atualizaPesos(peso[3], APRENDIZAGEM, target[i], saida[i], x4[i])
	
	ciclos = ciclos + 1

	
	ErroAgora = calculaErroQuadratico(target, saida)

	print ciclos, ErroAgora
	
	tolerancia = calculaErroSucessivo(ErroAgora, ErroAntes)
	
	ErroAntes = ErroAgora

#!/usr/bin/python

'''
Aluno: Roni Gilberto Goncalves
Matricula: 10921EEL026

Versao do programa: 0.1a

'''

from gi.repository import Gtk
from array import array

#Variaveis globais
w1 = 0
w2 = 0
b = 0
x1 = array('i', [-1, -1, 1, 1])
x2 = array('i', [-1, 1, -1, 1])
saida = array('i')

#Funcoes comuns
def func_soma(entrada1, entrada2, bias, peso1, peso2):
	
	return ((peso1*entrada1) + (peso2*entrada2) + bias)

def func_ativa(net):
	
	if net < 0:
		sinal = -1
	
	else:
		sinal = 1
	
	return sinal

#Funcoes de callback
def func_treinar(widget, *events):

	global saida
	global w1
	global w2
	global b
	
	Y1 = y1.get_text()
	Y2 = y2.get_text()
	Y3 = y3.get_text()
	Y4 = y4.get_text()
	
	saida.append(int(Y1))
	saida.append(int(Y2))
	saida.append(int(Y3))
	saida.append(int(Y4))
	
	for i in range(3):
		
		d1 = x1[i]*saida[i]
		d2 = x2[i]*saida[i]
	
		w1 = w1 + d1
		w2 = w2 + d2
		b = b + saida[i]

	d1 = x1[3]*saida[3]
	d2 = x2[3]*saida[3]
	
	w1 = w1 + d1
	w2 = w2 + d2
	b = b + saida[3]
	
	print w1
	print w2
	print b
	print d1
	print d2
	
	botaoTreinar.set_label('Treinado!')
	botaoTreinar.set_sensitive(False)
	LabelStatus.set_text('Treinamento completo!')

def func_testar(widget, *events):
	
	E1 = e1.get_text()
	E2 = e2.get_text()
	
	E1 = int(E1)
	E2 = int(E2)
	
	resposta = func_ativa(func_soma(E1, E2, b, w1, w2))
	resposta = str(resposta)
	
	LabelResultado.set_text(resposta)

def func_novoTreino(widget, *events):

	global w1
	global w2
	global b
	
	w1 = 0
	w2 = 0
	b = 0
		
	botaoTreinar.set_sensitive(True)
	botaoTreinar.set_label('Treinar')
	LabelResultado.set_text('')
	LabelStatus.set_text('Aguardando treinamento...')
	
	y1.set_text('')
	y2.set_text('')
	y3.set_text('')
	y4.set_text('')
	
	e1.set_text('')
	e2.set_text('')
	
#Dicionario de eventos
handlers = {
    'clicaTreinar': func_treinar,
    'clicaTestar' : func_testar,
    'clicanovoTreino' : func_novoTreino,
}

#Construindo interface e associando sinais a callbacks
builder = Gtk.Builder()
builder.add_from_file('../ui/interface3.ui')
builder.connect_signals(handlers)

#Configurando janela
win = builder.get_object('gamb.IA.rra')
win.connect('destroy', Gtk.main_quit)

#Obtendo widgets para posterior manipulacao

LabelStatus = builder.get_object('status')
LabelResultado = builder.get_object('saida_teste')

e1 = builder.get_object('entrada1')
e2 = builder.get_object('entrada2')

y1 = builder.get_object('saida1')
y2 = builder.get_object('saida2')
y3 = builder.get_object('saida3')
y4 = builder.get_object('saida4')

botaoTreinar = builder.get_object('b_treina')
botaoTestar = builder.get_object('b_testa')
botaonovoTeino = builder.get_object('b_novoTreino')

#Exibindo interface e iniciando loop de eventos
win.show_all()
Gtk.main()

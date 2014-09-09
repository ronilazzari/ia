#!/usr/bin/python
"""
Aluno: Roni Gilberto Goncalves
Matricula: 10921EEL026

"""

from gi.repository import Gtk

class Janela(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="gamb.IA.rra")
		
		grid = Gtk.Grid()
		self.add(grid)
		
		ind_treinamento = Gtk.Label(label="Treinamento")
		ind_teste = Gtk.Label(label="Teste")
		
		b_treina = Gtk.Button(label="Treinar")
		b_testa = Gtk.Button(label="Testar")
		
		separador = Gtk.VSeparator()
		
		grid.attach(ind_treinamento, 1, 1, 10, 1)
		grid.attach_next_to(separador, ind_treinamento, 1, 5, 1)
		grid.attach_next_to(ind_teste, separador, 1, 2, 1)
		
		grid.attach(b_treina, 2, 1, 10, 1)
		grid.attach(b_testa, 2, 2, 10, 1)
		
win = Janela()
win.connect("destroy", Gtk.main_quit)
#button = Gtk.Button("Ok")
#button.connect('clicked', botaoClicado)
#win.add(button)

win.show_all()
Gtk.main()

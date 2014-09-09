# -*- coding: utf-8 -*-
# Exemplo GTK+3

from gi.repository import Gtk

#Funções de callback
def botaoClicado(widget, *events):
    lblResult.set_text('Botao clicado')

#Dicionário de eventos
handlers = {
    'botaoClicado': botaoClicado,
}

#Construindo interface e associando sinais a callbacks
builder = Gtk.Builder()
builder.add_from_file('interface.ui')
builder.connect_signals(handlers)

#Configurando janela
win = builder.get_object("window1")
win.connect('destroy', Gtk.main_quit)

#Obtendo widgets para posterior manipulação
lblResult = builder.get_object('lblResult')

#Exibindo interface e iniciando loop de eventos
win.show_all()
Gtk.main()

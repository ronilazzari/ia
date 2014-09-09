# Exemplo GTK+3

from gi.repository import Gtk

def botaoClicado(widget, *events):
    print('Botao clicado')

win = Gtk.Window()
win.connect('destroy', Gtk.main_quit)
button = Gtk.Button("Meu botao")
button.connect('clicked', botaoClicado)
win.add(button)

win.show_all()
Gtk.main()

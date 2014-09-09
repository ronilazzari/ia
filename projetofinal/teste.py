#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('candidatos.db')

c = conn.cursor()

eita = c.execute("SELECT * from registroNovo")


while(c.fetchone()):
	print c.fetchone()
	print type(eita)

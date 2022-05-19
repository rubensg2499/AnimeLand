# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 10:55:36 2021

@author: Rubén
"""
import sqlite3
from sqlite3 import Error
from datetime import date
import requests
#Relacionadas a la base de datos.
def sql_conexion():
    try:
        con = sqlite3.connect('animeland.db')
        return con
    except Error:
        print(Error) 

def buscar_usuario(con, id_chat):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM usuario WHERE id_chat='"+id_chat+"'")
    rows = cursorObj.fetchall()
    if rows :
        return rows
    return 0

def insertar_usuario(con, id_chat,nick,nombre,apellidos):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO usuario VALUES('"+id_chat+"','"+nick+"','"+nombre+"','"+apellidos+"')")
    con.commit()

def actualizar_acceso(con,id_chat,fecha_actual):
    cursorObj = con.cursor()
    cursorObj.execute("UPDATE acceso SET num_usos = num_usos + 1 WHERE id_chat='"+id_chat+"' AND fecha='"+fecha_actual+"'")
    con.commit()
    
def insertar_acceso(con, id_chat,fecha):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO acceso VALUES('"+id_chat+"','"+fecha+"',1)")
    con.commit()
    
def buscar_acceso(con,id_chat,fecha_actual):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM acceso WHERE id_chat='"+id_chat+"' AND fecha='"+fecha_actual+"'")
    rows = cursorObj.fetchall()
    if rows :
        return rows
    return 0

def buscar_anime(con,id_anime):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM animes_buscados WHERE id_anime='"+str(id_anime)+"'")
    rows = cursorObj.fetchall()
    if rows :
        return rows
    return 0

def insertar_anime(con, id_anime,titulo):
    cursorObj = con.cursor()

    cursorObj.execute("INSERT INTO animes_buscados VALUES('{}','{}',1)".format(id_anime,titulo.replace("'","").replace('"',"")))
    con.commit()

def actualizar_anime(con, id_anime):
    cursorObj = con.cursor()
    cursorObj.execute("UPDATE animes_buscados SET num_busq = num_busq + 1 WHERE id_anime='"+id_anime+"'")
    con.commit()
    
def buscar_usuario_anime(con, id_chat, id_anime):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM usuario_anime WHERE id_anime='"+id_anime+"' AND id_chat='"+id_chat+"'")
    rows = cursorObj.fetchall()
    if rows :
        return rows
    return 0

def insertar_usuario_anime(con, id_chat, id_anime):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO usuario_anime VALUES('"+id_chat+"','"+id_anime+"',1)")
    con.commit()
    
def actualizar_usuario_anime(con, id_chat, id_anime):
    cursorObj = con.cursor()
    cursorObj.execute("UPDATE usuario_anime SET num_acce = num_acce + 1 WHERE id_anime='"+id_anime+"' AND id_chat='"+id_chat+"'")
    con.commit()

#Relacionadas al bot.
def enviar_mensaje(update,mensaje):
    update.message.reply_text(mensaje)

def enviar_imagen(url, bot, update):
    nombrelocal = 'imagen.jpg'
    imagen = requests.get(url).content
    with open(nombrelocal,"wb") as handler:
        handler.write(imagen)
    with open(nombrelocal,"rb") as photo_file:
        bot.sendPhoto(chat_id=update.message.chat.id,photo=photo_file); 
    
def obtener_fechaactual():
    today = date.today();
    hoy = "{}".format(today.day)+"/{}".format(today.month)+"/{}".format(today.year)
    return hoy

def operaciones_base_de_datos(conexion, anime, chat_id):
    if (buscar_anime(conexion,anime['mal_id']) == 0):
        insertar_anime(conexion,anime['mal_id'],anime['title'])
    else:
        actualizar_anime(conexion,str(anime['mal_id']))
                                
    if(buscar_usuario_anime(conexion,chat_id,str(anime['mal_id']))==0):
        insertar_usuario_anime(conexion,chat_id,str(anime['mal_id']))
    else:
        actualizar_usuario_anime(conexion,chat_id,str(anime['mal_id']))
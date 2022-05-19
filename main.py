# -*- coding: utf-8 -*-
"""

@author: Rubén
"""
import logging
import telegram

from telegram.error import NetworkError, Unauthorized
from time import sleep
from jikanpy import APIException, Jikan

import funciones as f
import constantes as c
import jikanpy

update_id = None
comando_ocupado = False
url = "https://www.etnassoft.com/api/v1/get/"


def main():
    global update_id
    bot = telegram.Bot(c.TELEGRAM_API)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def echo(bot):
    global update_id
    global comando_ocupado
    conexion = f.sql_conexion()
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        chat_id = str(update.message.chat.id)
        nick = str(update.message.chat.username)
        nombre = str(update.message.chat.first_name)
        apellidos = str(update.message.chat.last_name)
        fecha_actual = str(f.obtener_fechaactual())

        if(f.buscar_usuario(conexion, chat_id) == 0):
            f.insertar_usuario(conexion, chat_id, nick, nombre, apellidos)
            f.insertar_acceso(conexion, chat_id, fecha_actual)
        else:
            if(f.buscar_acceso(conexion, chat_id, fecha_actual) == 0):
                f.insertar_acceso(conexion, chat_id, fecha_actual)
            else:
                f.actualizar_acceso(conexion, chat_id, fecha_actual)

        if update.message:
            opcion = update.message.text
            if(comando_ocupado):
                if(comando_ocupado == 2):
                    f.enviar_mensaje(update, c.PROCESANDO_MENSAJE)
                    jikan = Jikan()
                    animes = jikan.search('anime', str(opcion))['results']
                    if(animes):
                        for i in range(10):
                            anime = animes[i]
                            f.operaciones_base_de_datos(
                                conexion, anime, chat_id)
                            f.enviar_imagen(
                                str(anime['image_url']), bot, update)
                            f.enviar_mensaje(update, "Id: {}\nTítulo: {}\nEpisodios: {}\nFecha de inicio: {}\nSinópsis: {}".format(
                                anime['mal_id'], anime['title'], anime['episodes'], anime['start_date'], anime['synopsis']))
                    else:
                        f.enviar_mensaje(update, c.INFORMACION_NO_ENCONTRADA)

                elif(comando_ocupado == 3):
                    f.enviar_mensaje(update, c.PROCESANDO_MENSAJE)
                    jikan = Jikan()
                    if(opcion.isdigit()):
                        try:
                            animes = jikan.genre(
                                type='anime', genre_id=int(opcion))['anime']
                            if(animes):
                                for i in range(5, 15, 1):
                                    anime = animes[i]
                                    f.operaciones_base_de_datos(
                                        conexion, anime, chat_id)
                                    f.enviar_imagen(
                                        str(anime['image_url']), bot, update)
                                    f.enviar_mensaje(update, "Id: {}\nTítulo: {}\nEpisodios: {}\nSinópsis: {}".format(
                                        anime['mal_id'], anime['title'], anime['episodes'], anime['synopsis']))
                            else:
                                f.enviar_mensaje(
                                    update, c.INFORMACION_NO_ENCONTRADA)
                        except jikanpy.exceptions.APIException:
                            f.enviar_mensaje(update, c.ID_NO_VALIDO)
                    else:
                        f.enviar_mensaje(update, c.ID_NO_VALIDO)
                elif(comando_ocupado == 4):
                    f.enviar_mensaje(update, c.PROCESANDO_MENSAJE)
                    jikan = Jikan()
                    if(opcion.isdigit()):
                        try:
                            anime = jikan.anime(int(opcion))
                            if(anime):
                                f.operaciones_base_de_datos(
                                    conexion, anime, chat_id)
                                f.enviar_imagen(
                                    str(anime['image_url']), bot, update)
                                f.enviar_mensaje(update, c.INFO_ANIME.format(anime['mal_id'],
                                                                             anime['title'],
                                                                             anime['title_japanese'],
                                                                             anime['synopsis'],
                                                                             anime['episodes'],
                                                                             anime['duration'],
                                                                             anime['rating'],
                                                                             anime['score'],
                                                                             anime['opening_themes'],
                                                                             anime['ending_themes'],
                                                                             anime['trailer_url']))
                            else:
                                f.enviar_mensaje(
                                    update, c.INFORMACION_NO_ENCONTRADA)
                        except jikanpy.Exception.APIException:
                            f.enviar_mensaje(update, c.ID_NO_VALIDO)
                    else:
                        f.enviar_mensaje(update, c.ID_NO_VALIDO)
                comando_ocupado = False
            else:
                if(opcion == c.START):
                    f.enviar_mensaje(update, c.BIENVENIDA)
                if(opcion == c.RECOMENDAR_ANIMES):
                    comando_ocupado = 1
                    f.enviar_mensaje(update, c.PROCESANDO_MENSAJE)
                    jikan = Jikan()
                    animes = jikan.top(type='anime', page=1)['top']
                    if(animes):
                        for i in range(10):
                            anime = animes[i]
                            f.operaciones_base_de_datos(
                                conexion, anime, chat_id)
                            f.enviar_imagen(
                                str(anime['image_url']), bot, update)
                            f.enviar_mensaje(update, "Id: {}\nTitulo: {}\nEpisodios: {}\nFecha de inicio: {}".format(
                                anime['mal_id'], anime['title'], anime['episodes'], anime['start_date']))
                    else:
                        f.enviar_mensaje(update, c.INFORMACION_NO_ENCONTRADA)
                    comando_ocupado = False
                elif(opcion == c.BUSCAR_ANIME):
                    comando_ocupado = 2
                    f.enviar_mensaje(
                        update, "Por favor ingrese el título de un anime a buscar.\nEjemplo: Naruto")
                elif(opcion == c.BUSCAR_ANIME_POR_GENERO):
                    comando_ocupado = 3
                    f.enviar_mensaje(update, c.LISTA_GENEROS)
                elif(opcion == c.MOSTRAR_ANIME):
                    comando_ocupado = 4
                    f.enviar_mensaje(
                        update, "Por favor ingrese el id de un anime a buscar.\nEjemplo: 666")
                else:
                    f.enviar_mensaje(update, c.MENSAJE_NO_ENTENDIDO)


if __name__ == '__main__':
    main()

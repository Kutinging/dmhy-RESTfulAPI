import asyncio
import json
import re

import aiohttp
import requests
from flask import Flask, jsonify, make_response, request

from modules.mods import *

app = Flask(__name__)

@app.route(f"/v{api.version}")
def home():
    return http.status({'status': 200, 'message': 'Welcome to dmhy RESTful API.', 'version': '1.0'}, 200)
    #return http.status(anime, 200)
#/
@app.route(f'/v{api.version}/list/', defaults={'anime_title': '','page':'1','lang':'tc','episode':''})
@app.route(f"/v{api.version}/list/<string:anime_title>")
@app.route(f"/v{api.version}/list/p<int:page>")
@app.route(f"/v{api.version}/list/<string:lang>")
@app.route(f"/v{api.version}/list/<string:anime_title>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:lang>/p<int:page>")
@app.route(f"/v{api.version}/list/<string:anime_title>/ep<int:episode>")
@app.route(f"/v{api.version}/list/<string:anime_title>/<string:lang>/ep<int:episode>")
def anime_search(anime_title='', team_id='', page=1, lang='', episode=''):
    """ search anime """
    try:
        if lang=='tc':
            lang = '繁體'
        elif lang=='sc':
            lang = '简体'
        tr_list = dmhy.animesearch(anime_title,team_id,page,lang,'{:0>2d}'.format(episode))
        title_list = website.title(tr_list)
        magnet_list = website.magnet(tr_list)
        teamid_list = website.teamid(tr_list)
        teamname_list = website.teamname(tr_list)
        anime = []
        for index in range(len(tr_list)):
            animedict = {}
            animedict['anime_title'] = title_list[index]
            animedict['anime_Fansub_team_id'] = teamid_list[index]
            animedict['anime_Fansub_team_name'] = teamname_list[index]
            animedict['download_magnet'] = magnet_list[index]
            anime.append(animedict)
        return http.status(anime, 200)
    except TypeError as e:
        log.write(str(e))
        return http.not_found(f'第 {page} 頁無資料')
    except Exception as e:
        log.write(str(e))
        return http.internal_server_error(str(e))

@app.route(f'/v{api.version}/detail/<string:anime_title>')
def anime_detail(anime_title='',team_id='',page=1,lang='',episode=''):
    """ show anime detail """
    try:
        if request.args.get('page'):
            page = request.args.get('page')
        if request.args.get('lang'):
            lang = request.args.get('lang')
        if request.args.get('team'):
            team_id = request.args.get('team')
        if request.args.get('ep'):
            episode = request.args.get('ep')
        if anime_title=='' or team_id=='' or episode=='':
            return http.internal_server_error('缺少必要參數，需要 team,ep')
        tr_list = dmhy.animesearch(anime_title,team_id,page,lang,episode)
        title_list = website.title(tr_list)
        magnet_list = website.magnet(tr_list)
        teamid_list = website.teamid(tr_list)
        teamname_list = website.teamname(tr_list)
        anime = []
        for index in range(len(tr_list)):
            animedict = {}
            animedict['anime_title'] = title_list[index]
            animedict['anime_Fansub_team_id'] = teamid_list[index]
            animedict['anime_Fansub_team_name'] = teamname_list[index]
            animedict['download_magnet'] = magnet_list[index]
            anime.append(animedict)
        return http.status(anime, 200)
    except TypeError as e:
        log.write(str(e))
        return http.not_found(f'第 {page} 頁無資料')
    except Exception as e:
        log.write(str(e))
        return http.internal_server_error(str(e))



@app.errorhandler(404)
def _not_found(e):
    """ 404 not found"""
    return http.not_found('404 not found')

@app.errorhandler(500)
def _internal_server_error(e):
    """ Internal Server Error """
    return http.internal_server_error('Server Error')


if __name__ == "__main__":
    app.run(port=7000)

from flask import Blueprint, render_template, request
from flask import current_app, redirect, url_for
from my_util.weather import get_weather
import my_util.crawl_util as cu
from my_util.gan_util import animeGAN
import os

crawl_bp = Blueprint('crawl_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':1, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':0, 'mi':0}

@crawl_bp.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'GET':
        place = request.args.get('place', '강남역')
        rest_list = cu.siksin(place)
        return render_template('crawling/food.html', menu=menu, weather=get_weather(),
                                rest_list=rest_list, place=place)
    else:
        place = request.form['place']
        return redirect(url_for('crawl_bp.food')+f'?place={place}')

@crawl_bp.route('/music')
def music():
    music_list = cu.genie()
    return render_template('crawling/music.html', menu=menu, weather=get_weather(),
                            music_list=music_list)

@crawl_bp.route('/music_jquery')
def music_jquery():
    music_list = cu.genie()
    return render_template('crawling/music_jquery.html', menu=menu, weather=get_weather(),
                            music_list=music_list)

@crawl_bp.route('/book')
def book():
    book_list = cu.interpark()
    return render_template('crawling/book.html', menu=menu, weather=get_weather(),
                            book_list=book_list)

@crawl_bp.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'GET':
        return render_template('crawling/spinner.html', menu=menu, weather=get_weather())
    else:
        youtube_list = cu.youtube()
        return render_template('crawling/youtube.html', menu=menu, weather=get_weather(),
                                youtube_list=youtube_list)

@crawl_bp.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'GET':
        return render_template('crawling/anime.html', menu=menu, weather=get_weather())
    else:
        version = request.form['version']
        f_src = request.files['face']
        file_src = os.path.join(current_app.static_folder, 'upload/') + f_src.filename
        f_src.save(file_src)
        return render_template('crawling/anime_spinner.html', menu=menu, weather=get_weather(),
                                src=f_src.filename, version=version)

@crawl_bp.route('/anime_res', methods=['POST'])
def anime_res():
    version = request.form['version']
    src = request.form['src']
    animeGAN(src, os.path.join(current_app.static_folder, 'upload/'), version)

    file_dst = os.path.join(current_app.static_folder, 'upload/') + "animated_image.jpg"
    mtime = int(os.stat(file_dst).st_mtime)
    return render_template('crawling/anime_res.html', menu=menu, weather=get_weather(),
                            src=src, version=version, mtime=mtime)
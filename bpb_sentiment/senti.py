from flask import Blueprint, render_template, request, current_app
from my_util.global_vars import okt
import os, re, joblib
import logging
import pandas as pd
import my_util.general_util as gu
from my_util.weather import get_weather
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

senti_bp = Blueprint('senti_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':1, 'mi':0}

spam_max_index = 1292
imdb_max_index = 6249
naver_max_index = 48994
shopping_max_index = 39981
imdb_lexicon_max_index = 24999

@senti_bp.route('/spam', methods=['GET', 'POST'])
def spam():
    if request.method == 'GET':
        return render_template('sentiment/spam.html', menu=menu, weather=get_weather())
    else:
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], spam_max_index)
            df_test = pd.read_csv(os.path.join(current_app.static_folder, 'data/spam_test.csv'))
            content = df_test.content[index]
            label = '스팸' if df_test.label[index] else '정상'
        else:
            content = request.form['content']
            label = '직접 확인'

        test_data = [re.sub('[^A-Za-z0-9]',' ',content).strip().lower()]
        spam_count_nb = joblib.load(os.path.join(current_app.static_folder, 'model/spam_count_nb.pkl'))
        spam_tfidf_lr = joblib.load(os.path.join(current_app.static_folder, 'model/spam_tfidf_lr.pkl'))
        pred_cn = '스팸' if spam_count_nb.predict(test_data)[0] else '정상'
        pred_tl = '스팸' if spam_tfidf_lr.predict(test_data)[0] else '정상'
        result_dict = {'label':label, 'pred_cn':pred_cn, 'pred_tl':pred_tl}
        return render_template('sentiment/spam_res.html', menu=menu, content=content,
                                res=result_dict, weather=get_weather())

@senti_bp.route('/imdb', methods=['GET', 'POST'])
def imdb():
    if request.method == 'GET':
        return render_template('sentiment/imdb.html', menu=menu, weather=get_weather())
    else:
        test_data = []
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], imdb_max_index)
            #index = int(request.form['index'] or '0')
            df_test = pd.read_csv(os.path.join(current_app.static_folder, 'data/IMDB_test.csv'))
            test_data.append(df_test.iloc[index, 0])
            label = '긍정' if df_test.sentiment[index] else '부정'
        else:
            test_data.append(request.form['review'])
            label = '직접 확인'

        imdb_count_lr = joblib.load(os.path.join(current_app.static_folder, 'model/imdb_count_lr.pkl'))
        imdb_tfidf_lr = joblib.load(os.path.join(current_app.static_folder, 'model/imdb_tfidf_lr.pkl'))
        pred_cl = '긍정' if imdb_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if imdb_tfidf_lr.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_tl':pred_tl}
        return render_template('sentiment/imdb_res.html', menu=menu, review=test_data[0],
                                res=result_dict, weather=get_weather())

@senti_bp.route('/naver', methods=['GET', 'POST'])
def naver():
    if request.method == 'GET':
        return render_template('sentiment/naver.html', menu=menu, weather=get_weather())
    else:
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], naver_max_index)
            #index = int(request.form['index'] or '0')
            df_test = pd.read_csv(os.path.join(current_app.static_folder, 'data/naver/movie_test.tsv'), sep='\t')
            org_review = df_test.document[index]
            label = '긍정' if df_test.label[index] else '부정'
        else:
            org_review = request.form['review']
            label = '직접 확인'
 
        test_data = []
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', org_review)
        #okt = Okt()
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
        morphs = okt.morphs(review, stem=True) # 토큰화
        temp_X = ' '.join([word for word in morphs if not word in stopwords]) # 불용어 제거
        test_data.append(temp_X)

        naver_count_lr = joblib.load(os.path.join(current_app.static_folder, 'model/naver_count_lr.pkl'))
        naver_count_nb = joblib.load(os.path.join(current_app.static_folder, 'model/naver_count_nb.pkl'))
        naver_tfidf_lr = joblib.load(os.path.join(current_app.static_folder, 'model/naver_tfidf_lr.pkl'))
        naver_tfidf_nb = joblib.load(os.path.join(current_app.static_folder, 'model/naver_tfidf_nb.pkl'))
        pred_cl = '긍정' if naver_count_lr.predict(test_data)[0] else '부정'
        pred_cn = '긍정' if naver_count_nb.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if naver_tfidf_lr.predict(test_data)[0] else '부정'
        pred_tn = '긍정' if naver_tfidf_nb.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_cn':pred_cn,
                                      'pred_tl':pred_tl, 'pred_tn':pred_tn}
        return render_template('sentiment/naver_res.html', menu=menu, review=org_review,
                                res=result_dict, weather=get_weather())

@senti_bp.route('/shopping', methods=['GET', 'POST'])
def shopping():
    if request.method == 'GET':
        return render_template('sentiment/shopping.html', menu=menu, weather=get_weather())
    else:
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], shopping_max_index)
            df = pd.read_csv(os.path.join(current_app.static_folder, 'data/shopping_test.csv'))
            org_review = df.reviews.values[index]
            label = '긍정' if df.label.values[index] > 0.5 else '부정'
        else:
            org_review = request.form['review']
            label = '직접 확인'
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을','ㅋㅋ','ㅠㅠ','ㅎㅎ']
        t = joblib.load(os.path.join(current_app.static_folder, 'model/shopping_tokenizer.pkl'))
        max_len = 60
        model = load_model(os.path.join(current_app.static_folder, 'model/shopping_lstm.h5'))
        
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', org_review)
        morphs = okt.morphs(review, stem=True)
        morphs = [word for word in morphs if word not in stopwords]
        encoded = t.texts_to_sequences([morphs])
        padded = pad_sequences(encoded, maxlen=max_len)
        score = float(model.predict(padded))
        pred = '긍정' if score > 0.5 else '부정'
        score = score if score > 0.5 else 1-score
        result_dict = {'label':label, 'score':round(score*100,2), 'pred':pred}
        return render_template('sentiment/shopping_res.html', menu=menu, weather=get_weather(),
                                res=result_dict, review=org_review)

@senti_bp.route('/imdb_lexicon', methods=['GET', 'POST'])
def imdb_lexicon():
    if request.method == 'GET':
        return render_template('sentiment/imdb_lexicon.html', menu=menu, weather=get_weather())
    else:
        threshold=int(request.form['threshold']) * 0.01
        senti_analyzer = SentimentIntensityAnalyzer()
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], imdb_lexicon_max_index)
            df = pd.read_csv(os.path.join(current_app.static_folder, 'data/IMDBdata.tsv'), sep='\t', quoting=3)
            review = df.review[index].replace('<br />',' ')
            review = re.sub('[^A-Za-z]',' ',review).strip()
            label = '긍정' if df.sentiment[index] == 1 else '부정'
        else:
            review = request.form['review']
            label = '직접 확인'

        score = senti_analyzer.polarity_scores(review)
        result = '긍정' if score['compound'] >= threshold else '부정'
        result_dict = {'label':label, 'vader_res':result, 'threshold':threshold}
        return render_template('sentiment/imdb_lexicon_res.html', menu=menu, 
                               review=df.review[index] if request.form['option'] == 'index' else review,
                               res=result_dict, weather=get_weather())
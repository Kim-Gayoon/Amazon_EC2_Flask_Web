## Web for DataAnalysis & AI Application
- http://3.36.223.111:5000

### Application
- 지역 분석, 카토그램, 크롤링, 워드클라우드
- 추천 시스템: 책, 영화
- 머신러닝: 분류, 회귀, PCA, 군집화
- 딥러닝: 이미지 분류, 이미지 검출
- 자연어 처리: 영화평 감성분석, 번역
- 게시판

### Software Version
- Anaconda3-2022.05 with python 3.9.7
- Tensorflow 2.8.0
- Flask 1.1.2
- Surprise 1.1.1
- Folium 0.12.1.post1
- MariaDB 5.5.68
- Bootstrap 4.6
- jQuery 3.6, jQuery-ui 1.12.1

### Hardware System
- AWS EC2 t2.small, 2GB Memory, 16GB HDD, Amazon Linux 2

### API 접속 Key 
- Weather API key (https://openweathermap.org/api)
- Kakao 인공지능 REST API key (https://developers.kakao.com/)
- 공공 인공지능 오픈 API key (https://aiopen.etri.re.kr/)

## 설치 방법
#### 1. Maria-DB 설치
<pre>
$ sudo yum install mariadb-server
$ sudo vi /etc/my.cnf.d/server.cnf
    [mysqld]
    character-set-server=utf8
    collation-server=utf8_unicode_ci
    skip-character-set-client-handshake
    default-time-zone='+9:00'
$ sudo vi /etc/my.cnf.d/client.cnf
    [client]
    default-character-set=utf8mb4
$ sudo vi /etc/my.cnf.d/mysql-clients.cnf
    [mysql]
    default-character-set=utf8mb4
$ sudo systemctl start mariadb
$ sudo systemctl enable mariadb
$ sudo systemctl status mariadb
$ mysql -u root -p                  # 최초 접속시에는 Enter가 패스워드
    MairaDB [(none)]> create database ckdb;
    MairaDB [(none)]> use mysql;
    MariaDB [mysql]> select host, user, password from user;
    MariaDB [mysql]> update user set password=password('새로운 비밀번호') where user='root';
    MariaDB [mysql]> flush privileges;
    MariaDB [mysql]> select host, user, password from user;
    MariaDB [mysql]> create user '사용자'@'#' identified by '비밀번호';
    MariaDB [mysql]> grant all privileges on *.* to '사용자'@'#';
    MariaDB [mysql]> create user '사용자'@'localhost' identified by '비밀번호';
    MariaDB [mysql]> grant all privileges on *.* to '사용자'@'localhost';
    MariaDB [mysql]> flush privileges;    
</pre>

#### 2. Anaconda 설치
<pre>
$ wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
$ bash Anaconda3-2021.11-Linux-x86_64.sh
$ source ~/.bashrc
</pre>

#### 3. 개발 도구(git, gcc 등), Java 설치
<pre>
$ sudo yum groupinstall "Development Tools"
$ sudo yum install java-11-amazon-corretto.x86_64
$ sudo vi /etc/profile.d/java.sh
    JAVA_HOME=/usr/lib/jvm/java-11-amazon-corretto.x86_64
</pre>

#### 4. Chrome, Chromedriver 설치
<pre>
$ sudo curl https://intoli.com/install-google-chrome.sh | bash
$ sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
$ google-chrome -version && which google-chrome

$ wget https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/bin
$ chromedriver -version
</pre>

#### 5. 파이썬 패키지 설치
<pre>
$ pip install mysql.connector
$ pip install scikit-surprise
$ pip install folium
$ pip install wordcloud
$ pip install selenium
$ pip install Konlpy
$ pip install tensorflow
</pre>

#### 6. 한글폰트 설치
<pre>
$ wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
$ unzip NanumFont_TTF_ALL.zip -d NanumFont
$ sudo mv NanumFont /usr/share/fonts
$ sudo fc-cache -fv
</pre>

#### 7. 설치 후 후속작업
<pre>
$ rm A* *.zip
$ python
    >>> import nltk
    >>> nltk.download('vader_lexicon')
$ git config --global user.name "본인 이름"
$ git config --global user.email 본인 이메일
    # github를 사용하기 위해서는 토큰을 생성한 후, 패스워드 입력할 때 입력해야 함
$ git clone https://github.com/ckiekim/Amazon_EC2_Flask_Web.git web
$ cd web/db                                                 # mysql.json upload
    # mysql.json에 "charset": "utf8mb4" 추가할 것
$ python db_init.py                                         # table 및 초기데이터 생성
$ cd ../static
$ mkdir clus_pca_data tmp keys model movies upload          # tmp, keys, movies data upload
$ cd data
$ mkdir mnist, movies, naver, news                          # mnist, movies, naver, news data upload
$ cd ~/web/bp5_recommendation
$ python make_movie_data(ml-latest_model)
$ cd ../bp6_classification
$ python cancer_model(iris_model, pima_model, titanic_model, wine_model)
$ cd ../bp7_advanced
$ python digits_model(mnist_model, news_model)
$ cd ../bpb_sentiment
$ python imdb_model(naver_model, spam_model)
$ cd ~/web
$ nohup python app.py > /dev/null 2>&1 &                    # 프로그램 실행
</pre>
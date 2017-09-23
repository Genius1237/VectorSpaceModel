from flask import Flask
from flask import render_template
from flask import request
from vectorspace import VectorSpaceModel
import string_processing
import sqlalchemy
import pandas

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	query = request.args.get('query', '')
	size = request.args.get('size', '')
	query = string_processing.process_0(query)
	songs_info = getSongsInfo(m.getSimilarDocuments(query, size))
	#songs_info = [(12, "hi", "nope")]
	return render_template('search.html', query=query, size=size, songs_info=songs_info)

@app.route('/song')
def song():
	song_info = getSongInfo(request.args.get('song_id', ''))
	# song_info = {
	# 	'song': "waiting for the end",
	# 	'artist': "Linkin Park",
	# 	'lyrics': "No no no no no isajfljafdksjflano\n" * 100
	# }
	return render_template('song.html', song_info=song_info)
		
def getDocuments():
	""" List of tuples (song_id, lyrics)
	"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	pd = pandas.read_sql("select song_id,text from song_lyrics",conn)
	l = [(pd.iloc[i,0], pd.iloc[i,1]) for i in pd.index] 
	return l

def getSongsInfo(song_ids):
	""" List of tuples (song_id, song_name, artist)
	"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	l =[]
	for song_id in song_ids:
		pd = pandas.read_sql("select song, artist, text from song_lyrics where song_id = %s",conn, params=[song_id])
		l.append([(pd.iloc[i,0], pd.iloc[i,1], pd.iloc[i,2]) for i in pd.index]) 
	return l	

def getSong(song_id):
	"""
	{
		'song': ;
		'artist':;
		'text':;
	}"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	pd = pandas.read_sql("select song, artist, text from song_lyrics where song_id = %s",conn, params=[song_id])
	d = {"song":pd.iloc[0,0], "artist":pd.iloc[0,1], "lyrics":pd.iloc[0,2]}
	return d

m = VectorSpaceModel()
d = getDocuments()
dc = []
for i in range(len(d)):
	dc.append((d[i][0], string_processing.process_0(d[i][1])))
m.processDocuments(dc)

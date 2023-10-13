from flask import Flask, render_template, send_file, Response, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_poc.html', music = 'music.mp3')

@app.route('/stream_music', methods=['POST', 'GET'])
def stream_music():
    song = "music/"+request.args.get("song")+".mp3"
    # music = "music.mp3"
    return send_file(song, mimetype='audio/mpeg')

@app.route('/player', methods=['GET'])
def get_player():
    # Fetch the music id from the request
    song = request.args.get("song")
    return render_template('player.html', audio = "/stream_music?song=" + song)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

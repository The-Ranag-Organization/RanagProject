from flask import Flask
app = Flask(__name__)

with open("index.html", "r") as page1:
    indexpg = page1.read()
with open("download.html", "r") as page2:
    downloadpg = page2.read()

@app.route('/')
def home():
    return indexpg;

@app.route('/download')
def download():
    return downloadpg;

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
    app.static_folder = 'static'

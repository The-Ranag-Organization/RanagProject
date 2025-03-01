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
def home():
    return downloadpg;

if __name__ == '__main__' :
    app.run(debug=True)

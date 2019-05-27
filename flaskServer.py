from flask import Flask
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/")
def main():
    return render_template('index.html').encode('utf-8').strip()

if __name__ == "__main__":
    app.run()	
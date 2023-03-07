from flask import Flask, request, render_template
from script import schedule_tee_times

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        schedule_tee_times()

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
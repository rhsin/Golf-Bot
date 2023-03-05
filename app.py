from flask import Flask, request, render_template
from main import schedule_tee_time
from test import test_tee_time

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        form_course = request.form.get("first_course")
        form_days = request.form.get("days_ahead")
        test_tee_time(form_course, form_days)

    return render_template('index.html')
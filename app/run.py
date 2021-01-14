from flask import Flask
from pages import pages
import scheduler
from predict import predict

tempalte_dir = '../templates'
static_dir = '../static'
csv_dir = '../../mounted/data'
model_dir = '../../mounted/model'

app = Flask(__name__, template_folder=tempalte_dir, static_folder=static_dir)
app.register_blueprint(pages)
app.register_blueprint(predict)


if __name__ == "__main__":
    schedule_with_tasks = scheduler.setup_jobs(csv_dir=csv_dir, model_dir=model_dir)
    scheduler.run_scheduler_in_separated_thread(schedule_with_tasks)
    app.run(debug=True, host='0.0.0.0')


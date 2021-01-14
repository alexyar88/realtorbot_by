import time
import schedule
import parser
import trainer
import threading


def setup_jobs(csv_dir, model_dir):
    # schedule.every(5).seconds.do(print, f'test scheduler')
    schedule.every().monday.at('02:30').do(parser.parse_data_to_csv, csv_dir=csv_dir)
    schedule.every().monday.at('05:30').do(trainer.run_training, csv_dir=csv_dir, model_dir=model_dir)
    return schedule


def run_scheduler_in_separated_thread(schedule_with_tasks):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule_with_tasks.run_pending()
                time.sleep(1)

    continuous_thread = ScheduleThread()
    continuous_thread.start()


if __name__ == '__main__':
    pass
    # schedule_parser('something')
    # continuous_thread.run()

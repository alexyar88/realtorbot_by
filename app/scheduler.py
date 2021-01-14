import time
import schedule
import parser


def schedule_parser(csv_path):
    # schedule.every().monday.at('5:30').do(parser.parse_data_to_csv, csv_path=csv_path)
    schedule.every().second.do(print, f'run scheduler {csv_path}')
    while True:
        schedule.run_pending()
        time.sleep(1)

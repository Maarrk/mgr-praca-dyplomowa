import argparse
import os

parser = argparse.ArgumentParser(description='Rename operators in log files.')
parser.add_argument('old')
parser.add_argument('new')
args = parser.parse_args()

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

for filename in os.listdir(log_path):
    datetime, operator, level = filename[:-4].split('_')
    if operator == args.old:
        new_name = '_'.join([datetime, args.new, level]) + '.csv'
        with open(os.path.join(log_path, filename), 'r') as fin:
            with open(os.path.join(log_path, new_name), 'w') as fout:
                header = fin.readline()
                assert header.split(',')[1] == 'simulationProfile'  # ensure format hasn't changed
                meta = fin.readline()
                words = meta.split(',')
                assert words[1] == '"' + operator + '"'  # ensure metadata matches filename
                words[1] = '"' + args.new + '"'
                meta = ','.join(words)
                fout.writelines([header, meta])

                for line in fin:
                    fout.writelines([line])

        os.remove(os.path.join(log_path, filename))

from tkinter import *
import datetime
import pandas as pd
import csv

### PARAMS ###
n_questions=5
choices=['a','b','c','d','e']
session_data_raw_fname = 'session_data_raw1.csv'
session_data_featurized_fname = 'session_data_featurized1.csv'

### BUILD GUI ###
root = Tk()
frame = Frame(root).grid()
answers = [StringVar() for _ in range(n_questions)]

with open(session_data_raw_fname, 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['question', 'answer', 'datetime'])

def make_callback(question,answer):
    def callback():
        with open(session_data_raw_fname, 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow([question, answer, datetime.datetime.now()])
    return callback

for na,a in enumerate(answers):
    for nc,c in enumerate(choices):
        Label(root, text=str(na+1)+")").grid(row=na,column=0)
        Radiobutton(frame, text=str(c), variable=a, value=c, command=make_callback(na+1,c)).grid(row=na,column=nc+1)

### RUN GUI ###
root.mainloop()
with open(session_data_raw_fname, 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['','', datetime.datetime.now()])

### COMPUTE USER DATA ###
df = pd.read_csv(session_data_raw_fname)
df['datetime'] = df['datetime'].apply(pd.to_datetime)
df['duration'] = df['datetime'].diff().shift(-1)
df = df.head(-1)
df['question'] = df['question'].apply(lambda x: int(x))

features = pd.DataFrame(df.groupby('question')['duration'].sum())
features['answer_sequence'] = df.groupby('question')['answer'].sum()
features.to_csv(session_data_featurized_fname)

print features
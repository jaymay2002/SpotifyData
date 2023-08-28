from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from flask import send_file
from multiprocessing import Process, Queue

app = Flask(__name__)

def generate_graph(dates, counts):
    plt.figure(figsize=(10, 6), dpi=80)
    plt.plot(counts, label="Counts")
    plt.xlabel("Dates")
    plt.ylabel("Counts")
    plt.title("Counts Over Time")
    plt.legend()
    plt.tight_layout()
    tmp_image_path = 'static/graph.png'  # Path within the 'static' directory
    plt.savefig(tmp_image_path)
    plt.close()

    return tmp_image_path

def calculate_top_songs(song_name):
    # Your existing data processing code
    # ...
    print("Calculating top songs START")
    names = ["endsong_"+str(i)+".json" for i in range(0,10)]
    dfs = [] # an empty list to store the data frames
    for file in names[1:3]:
        path = "/Users/jasonmaytin/Desktop/Music/Spotify Data/"
        data = pd.read_json(path + file) # read data frame from json file
        dfs.append(data) # append the data frame to the list
    temp = pd.concat(dfs, ignore_index=True)#.sort_values("ts").reset_index(drop=True)
    #top = temp.groupby("master_metadata_track_name").count().sort_values("ts",ascending=False)
    mini = pd.to_datetime(temp["ts"]).dt.date.min()
    maxi = pd.to_datetime(temp["ts"]).dt.date.max()
    len(pd.date_range(mini,maxi))
    def song(name):
        song = temp["master_metadata_track_name"]==name
        dates = pd.to_datetime(temp["ts"]).dt.normalize()
        vals = np.cumsum(song)
        return dates,vals
    #print("Calculating top songs END")
    #print(top)

    want = song(song_name)
    return want

@app.route('/')
def index():
    print("Accessing main page")
    sample_data = {
        "Song 1": 10,
        "Song 2": 15,
        "Song 3": 8,
    }
    return render_template('index.html', data=sample_data)

@app.route('/fetch_data')
def fetch_data():
    print("FETCHING DATA")
    song_name = request.args.get('song')
    top_data = calculate_top_songs(song_name)
    dates = top_data[0]
    vals = top_data[1]

    tmp_image_path = generate_graph(dates, vals)  # Call the function to generate and save the graph
    print("Graph image saved at:", tmp_image_path)

    top_data_dict = {str(date): count for date, count in zip(dates, vals)}
    #print(top_data_dict)
    return jsonify(top_data_dict)

if __name__ == '__main__':
    app.run(debug=True,port=5001)


from flask import Flask, render_template, request, session  # from module import Class.


import os 
import re
import hfpy_utils
import swim_utils


app = Flask(__name__)
app.secret_key = 'ca assigmnent'

files = os.listdir(swim_utils.FOLDER)
files.remove(".DS_Store")
names = set()
show_events = {}
name_age = {}

for swimmer in files:
    try:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
        name_age[swim_utils.get_swimmers_data(swimmer)[0]] = swim_utils.get_swimmers_data(swimmer)[1]
    except FileNotFoundError : 
        print(f"Warning: File not found for swimmer {swimmer}")

def get_swimmer_events_list():
    event_list = []
    for file in files:
        if re.search(request.form["swimmer"], file):
            title = file.split('-')[1].removesuffix(".txt")
            event_list.add(title)
    return sorted(event_list)


@app.get("/")
        
@app.get("/getswimmers")
def get_swimmers_names():
    return render_template(
        "select.html",
        title="Select a swimmer",
        data = sorted(names),
        namedata = name_age,
    )
    
@app.post("/displayevents")
def display_events():
    session["swimmer"] = request.form["swimmer"]
    event_list = []
    for file in files:
        if re.search(request.form["swimmer"], file):
            title = '-'.join(file.split('-')[2:]).removesuffix(".txt")
            event_list.append(title)
    show_events[request.form["swimmer"]] = event_list
    return render_template(
        "select2.html",
        title="Select an event",
        swimmer_event = sorted(show_events[request.form["swimmer"]]),

    )

@app.post("/chart")
def display_chart():
    swimmer = request.form.get("swimmer")
   
    filename = (
        f"{swimmer}"
        + name_age[session["swimmer"]]
        + (request.form["event"].split(" ")[0] if len(request.form["event"].split(" ")) >= 1 else "")
        + (request.form["event"].split(" ")[1] if len(request.form["event"].split(" ")) >= 2 else "")
        + ".txt"

    )
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(filename)

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [ hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts ]
    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
        times=the_times,
        converts=the_converts,
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.

import flask
from flask import request
from textgenrnn import textgenrnn
from keras.backend import clear_session

def get_network(cuisine1, cuisine2):
    clear_session()
    textgen = textgenrnn()
    try: 
        filename = cuisine1 + '_' + cuisine2 + '_weights.hdf5'
        textgen.load('./models/' + filename)
        return textgen
    except:
        try:
            filename = cuisine2 + '_' + cuisine1 + '_weights.hdf5'
            textgen.load('./models/' + filename)
            return textgen
        except:
            return False

        
# Initialize the app

app = flask.Flask(__name__)


# An example of routing:
# If they go to the page "/" (this means a GET request
# to the page http://127.0.0.1:5000/), return a simple
# page that says the site is up!


@app.route("/", methods=["POST", "GET"])
def predict():
    # request.args contains all the arguments passed by our form
    # comes built in with flask. It is a dictionary of the form
    # "form name (as set in template)" (key): "string in the textbox" (value)
    #cuisine1, cuisine2 = make_prediction(request.args)
    #return flask.render_template('predictor.html', cuisine1=cuisine1,
    #                             cuisine2=cuisine)
    return flask.render_template('index.html')

@app.route("/menu-item", methods=['GET', 'POST'])
def menu_item():
    global cuisine1
    global cuisine2
    global textgen
    cuisine1 = request.form['Cuisine1']
    cuisine2 = request.form['Cuisine2']
    if cuisine1 == cuisine2:
        errormsg = "Sorry, you have chosen the same two cuisines!"
        return flask.render_template('not-available.html', data = errormsg,
                                     cuisine1 = cuisine1, cuisine2 = cuisine2)
    textgen = get_network(cuisine1, cuisine2)

    if textgen is False:
        errormsg = "Sorry, these cuisine types aren't quite ready yet..."
        return flask.render_template('not-available.html', data = errormsg,
                                     cuisine1 = cuisine1, cuisine2 = cuisine2)
    else:
        fusion = textgen.generate(return_as_list=True)
        return flask.render_template('menu-item.html', data = fusion[0],
                                     cuisine1 = cuisine1, cuisine2 = cuisine2)

@app.route("/menu-item-reload")
def menu_reload():
    fusion = textgen.generate(return_as_list=True)
    return flask.render_template('menu-item.html', data = fusion[0],
                                 cuisine1 = cuisine1, cuisine2 = cuisine2)
# Start the server, continuously listen to requests.
# We'll have a running web app!

# For local development:
app.run()

# For public web serving:
# app.run(host='0.0.0.0')

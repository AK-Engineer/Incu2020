from flask import Flask, request, render_template, jsonify, json
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from bson import json_util


app = Flask(__name__)

app.secret_key = 'DlHhKG8DF_fe_vtcRiKZVg'

app.config["MONGO_URI"] = "mongodb://svetlana:cisco123@localhost/Device_Configuration"

json.dumps = json_util.dumps

mongo = PyMongo(app)


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# 1.HTML-for all switches
# @app.route('/switch_name_html', methods=['GET'])
# def get_switches():
#     mongo_filter = {}
#     result = mongo.db.Interfaces.find(mongo_filter)
#     return  render_template('get_switches.html',result = result)

# 1.HTML-for specified switches switches
# Samples: bru-dna-1:,mastodon:
@app.route('/<switch_name>/interfaces.html', methods=['GET'])
def get_switches(switch_name):
    mongo_filter = {'Switch_name': switch_name}
    result = mongo.db.Interfaces.find(mongo_filter)
    return render_template('interfaces.html', result=result)


# 2.JSON-for specified switches switches
@app.route('/<switch_name>/interfaces.json', methods=["GET"])
def get_switches_json(switch_name):
    mongo_filter = {'Switch_name': switch_name}
    result = mongo.db.Interfaces.find(mongo_filter)
    return jsonify({'Interfaces': result})


# 3.HTML:specified interface
# path:  is used because interface_name in url can contain '/'
@app.route('/<switch_name>/<path:interface_name>/details.html', methods=['GET'])
def get_interface_details_html(switch_name, interface_name):
    mongo_filter = {'Switch_name': switch_name, 'Interface_name': interface_name}
    try:
        result = mongo.db.Interfaces.find_one(mongo_filter)
        if result:
            return render_template('details.html', result=result, switch=switch_name, intf=interface_name)
        return '<h1>Could not find wanted interface</h1>', 400
    except ServerSelectionTimeoutError:
        return 'Could not connect to the mongodb server', 500


# 4.JSON:specified interface
@app.route('/<switch_name>/<path:interface_name>/details.json', methods=['GET'])
def get_interface_details_json(switch_name, interface_name):
    mongo_filter = {'Switch_name': switch_name, 'Interface_name': interface_name}
    try:
        result = mongo.db.Interfaces.find_one(mongo_filter)
        print(result)
        final_result = {}
        for i in result['Interface_name']:
            index = result['Interface_name'].index(i)
            if i == interface_name:
                final_result['Description'] = result['Description'][index]
                final_result['State'] = result['State'][index]
        if result:
            # return render_template('details.html', result = result, switch = switch_name, intf = interface_name)
            return jsonify(final_result)
        return '<h1>Could not find wanted interface</h1>', 400
    except ServerSelectionTimeoutError:
        return 'Could not connect to the mongodb server', 500

#5-PATCH request to update Description of certain interface
#6-PATCH request to update State of certain interface
@app.route("/<switch_name>/<path:interface_id>", methods=["PATCH"])
def update_interface_description(switch_name, interface_id):
    payload = request.get_json()
    # Query to get the entry of db with certain switch_name and interface_id
    mongo_filter = {'Switch_name': switch_name, 'Interface_name': interface_id}
    result = mongo.db.Interfaces.find_one(mongo_filter)
    # Get the index of interface_name because in db we use arrays
    for i in result['Interface_name']:
        if i == interface_id:
            index = result['Interface_name'].index(i)

    if payload:
        #Check if PATCH contains Description OR State payload
        if ('State') in payload.keys():
            if (payload['State'] not in ['Down', 'Up', 'down', 'up', 'DOWN', 'UP']):
                return 'Error, State is not valid', 500
            #Update the specific State
            result_state = mongo.db.Interfaces.find_one_and_update(
                {'Switch_name': switch_name, 'Interface_name': interface_id},
                {"$set": {'State.' + str(index) : payload['State']}},
                return_document=ReturnDocument.AFTER
            )
            return jsonify(result_state), 200
        elif ('Description') in payload.keys():
            result_desc = mongo.db.Interfaces.find_one_and_update(
                {'Switch_name': switch_name, 'Interface_name': interface_id},
                {"$set": {'Description.' + str(index) : payload['Description']}},
                return_document=ReturnDocument.AFTER
            )
            return jsonify(result_desc), 200
    return 'Error', 500

if __name__ == '__main__':
    app.run()
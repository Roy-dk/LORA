from flask import Flask, jsonify, request, render_template
from redis import Redis
import socket

app = Flask(__name__)

r = Redis(host='redis', port=6379, decode_responses=True)


@app.route('/test')
def test():
    print(r.get("foo"))
    return "get "+str(r.get("foo"))

@app.route('/api/get_data', methods=['GET'])
def get_data():  
    id = request.args.get("id")
    if id:
        print("id:",id)
        temperature = r.get(id+"-temperature")
        # print(temperature)
        weight = r.get(id+"-weight")
        light = r.get(id+"-light")
        temperature_date = r.get(id+"-temperature_date")
        weight_date = r.get(id+"-weight_date")
        light_date = r.get(id+"-light_date")
        log_date = r.get(id+"-log_date")
        log = r.get(id+"-log")
        return jsonify({
            "temperature" : temperature,
            "temperature_date" : temperature_date,
            "weight" : weight,
            "weight_date" : weight_date,
            "light" : light,
            "light_date" : light_date,
            "log" : log,
            "log_date" : log_date,
        })

@app.route('/api/send_data', methods=['GET'])
def send_data(): 
    try:
        id = request.args.get("id")
        data = request.args.get("data")
        msg = id+"#"+data
        send_list = r.get("send_list")
        if send_list == "" or send_list == None:
            r.set("send_list", msg)
        else:
            msg = send_list + "|" + msg
            r.set("send_list", msg)
        return jsonify({"code":0})
    except:
        print(send_list)
        return jsonify({"code":1,"msg":"error"})



def test():
    print(r.get("foo"))
    return "get "+str(r.get("foo"))


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)

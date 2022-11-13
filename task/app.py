from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_average_rate():
    # date_from
    # date_to
    # origin
    # destination

    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    return {'origin': origin,'destination': destination, 'date_from': date_from, 'date_to': date_to}

@app.route('/status', methods=['POST', 'GET'])
def get_status():
    return {'status': 'running'}


if __name__ == '__main__':
    app.run(debug=True)

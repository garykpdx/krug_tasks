from datetime import date, datetime

from flask import Flask
from flask import abort
from flask import request

from task.data_access import DataAccess

app = Flask(__name__)


@app.route('/rates', methods=['GET'])
def get_average_rate():
    try:
        date_from = datetime.strptime(request.args.get('date_from'), "%Y-%m-%d").date()
        date_to = datetime.strptime(request.args.get('date_to'), "%Y-%m-%d").date()
    except TypeError:
        abort(400)

    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not origin or not destination:
        abort(400)

    data = DataAccess()
    results = data.get_results(origin, destination, date_from, date_to)
    return results


@app.route('/status', methods=['GET', 'POST'])
def get_status():
    data = DataAccess()
    version = data.get_version()
    return {'status': 'running', 'database': version}


if __name__ == '__main__':
    app.run(debug=True)

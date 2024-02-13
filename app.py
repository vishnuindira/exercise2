from flask import Flask, request
from flask_restful import Resource, Api
from dicttoxml import dicttoxml
from operator import itemgetter

app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self, data_type):
        if 'employees' in app.config: 
            employees = app.config['employees']
            employees.sort(key=itemgetter('age'))
        else:
            employees = []

        if data_type == 'json':
            return {'employees': employees}
        elif data_type == 'xml':
            return dicttoxml(employees).decode()
        else:
            return {'error': 'Invalid data type'}, 404

    def post(self):
        new_employees = request.get_json()
        if 'employees' in app.config:
            app.config['employees'].extend(new_employees)
        else:
            app.config['employees'] = new_employees
        return {'message': 'Employees added'}

api.add_resource(Employees, '/<string:data_type>', '/add')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

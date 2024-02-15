# Importing libraries
from flask import Flask, request
from flask_restful import Resource, Api
from dicttoxml import dicttoxml
from operator import itemgetter

# Start a Flask application
app = Flask(__name__)
# Start a Flask-RESTful API on that application.
api = Api(app)

# Define a resource class "Employees" that will handle HTTP requests
class Employees(Resource):

    # GET method
    # data_type is specified in the URL and can be 'json' or 'xml'
    def get(self, data_type):
        # Check if 'employees' exists in Flask global config
        if 'employees' in app.config: 
            employees = app.config['employees']
            # Sort the employees by age
            employees.sort(key=itemgetter('age'))
        else:
            employees = []
        
        # Depending on the 'data_type' return different types of responses
        if data_type == 'json':
            return {'employees': employees}
        elif data_type == 'xml':
            return dicttoxml(employees).decode()
        else:
            return {'error': 'Invalid data type'}, 404

    # POST method
    def post(self):
        # Get data from post request
        new_employees = request.get_json()

        # if 'employees' exists, add the new employees to existing list
        if 'employees' in app.config:
            app.config['employees'].extend(new_employees)
        # If it doesn't exist, set 'employees' to be the new employees
        else:
            app.config['employees'] = new_employees
        return {'message': 'Employees added'}

# Add 'Employees' resource to the Api.
# It can be accessed via two endpoints: '/<string:data_type>' and '/add'
api.add_resource(Employees, '/<string:data_type>', '/add')

# If this file is being run directly, start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

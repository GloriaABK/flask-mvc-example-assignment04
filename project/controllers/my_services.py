from project import app
from flask import render_template, request, redirect, url_for 
from project.models.my_dao import *
from project.models.employees import *
from project.models.customers import *

@app.route('/get_cars', methods=['GET']) 
def query_records():
    return findAllCars()

# The method uses the registration number to find the car object from database 
@app.route('/get_cars_by_reg_number', methods=['POST']) 
def find_car_by_reg_number():
    record = json.loads(request.data) 
    print(record)
    print(record['reg'])
    return findCarByReg(record['reg'])

@app.route('/save_car', methods=["POST"]) 
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# The method uses the registration number to find the car
# object from database and updates other information from
# # the information provided as input in the json object 
@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# The method uses the registration number to find the car # object from database and removes the records @app.route('/delete_car', methods=['DELETE'])

@app.route('/delete_car', methods= ['DELETE'])
def delete_car_info():
    record = json.loads(request.data) 
    print(record) 
    delete_car(record['reg'])
    return findAllCars()


#Functions for employees

@app.route('/get_employees', methods=['GET'])
def query_records():
    return findAllEmployees()


@app.route('/save_employee', methods=["POST"])
def save_employee_info():
    record = json.loads(request.data)
    print(record)
    return save_employee(name['name'], address['address'], branch['branch'])


@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = json.loads(request.data)
    print(record)
    return update_employee(name['name'], address['address'], branch['branch'])


@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)
    print(record)
    delete_employee(name['name'])
    return findAllEmployees()


# Functions for customers
@app.route('/get_customers', methods=['GET'])
def query_records():
    return findAllCustomers()

@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    record = json.loads(request.data)
    print(record)
    return save_customer(name['name'], age['age'], address['address'])


@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    record = json.loads(request.data)
    print(record)
    return update_employee(name['name'], age['age'], address['address'])

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)
    print(record)
    delete_customer(name['name'])
    return findAllCustomers()



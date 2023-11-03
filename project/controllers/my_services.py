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

@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()


# Functions for employees

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


# Defining the Endpoint for implementing an endpoint 'order-car' where a customer-id, car-id is passed as paramteres
customer_bookings = {}
car_status = {}

@app.route('/order-car', methods=['POST'])
def order_car(car_id, customer_id):
    if customer_id in customer_bookings and car_id[customer_id]:
        return "Booking failed. You already have a car booking."
    if car_id not in car_status or car_status[car_id] == 'booked':
        car_status[car_id] = 'booked'
        return "The car you have requested is unfortunately not available."
    else:
        customer_bookings[customer_id] = car_id
        return f"Order placed by Customer ID:{customer_id} for car ID: {car_id}"


@app.route('/cancel-order-car', methods=['POST'])
def cancel_order():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    if customer_id in customer_bookings and customer_bookings[customer_id] == car_id:
        del customer_bookings[customer_id]
        car_status[car_id] = 'Available'
        return "Order canceled successfully"
    else:
        return "Customer does not have a booking for this car", 400


@app.route('/rent-car', methods =['POST'])
def rent_car():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    if customer_id in customer_bookings and customer_bookings[customer_id] == car_id:
        car_status[car_id] = 'Rented'
    else:
        return "Customer does not have a valid booking for this car.", 400


@app.route('/return-car', methods =['POST'])
def return_car():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    car_status_return = data.get('car_status')
    if customer_id in customer_bookings and customer_bookings[customer_id] == car_id:
        if car_status_return == 'ok':
            car_status[car_id] = 'Available'
        elif car_status_return == 'damaged':
            car_status[car_id] = 'Damaged'
        else:
            return 'Invalid.', 400

        del customer_bookings[customer_id]
        return 'Car has been successfully returned'
    else:
        return 'Invalid. Customer has no active bookings for this car', 400













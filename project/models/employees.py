from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://59586998.databases.neo4j.io"
AUTH = ("neo4j", "Us_fJ1oy7gyhh_zr9tGKY5wv-va2p9ARiO1FMGRSivs")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver


def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

def findAllEmployees():
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json


def save_employee(name, address, branch):
    employee = _get_connection().execute_query(
        "MERGE (a:Employee{name: $name, address: $address, branch:$branch}) RETURN a;", name=name,
        address=address, branch=branch)
    nodes_json = [node_to_json(record["a"]) for record in employee]
    print(nodes_json)
    return nodes_json


def update_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee{name: set a.name=$name, a.address=$address, a.branch=$branch}) "
                               "RETURN a;",
                               name=name,
                               address=address, branch=branch)
        print(employee)
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json


def delete_employee(name):
    _get_connection().execute_query("MATCH (a:employee{name: $name}) delete a;", name=name)


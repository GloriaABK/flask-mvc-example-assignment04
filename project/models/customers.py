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

def findAllCustomers():
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customer]
        print(nodes_json)
        return nodes_json


def save_customer(name, age, address):
    customer = _get_connection().execute_query(
        "MERGE (a:Employee{name: $name, address: $address, branch:$branch}) RETURN a;", name=name,
        age=age, address=address)
    nodes_json = [node_to_json(record["a"]) for record in customer]
    print(nodes_json)
    return nodes_json

def update_customer(name, age, address):
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer{name: set a.name=$name, a.age=$age, a.address=$address}) RETURN a;",
                               name=name,
                               age=age,
                               address=address)
        print(customer)
        nodes_json = [node_to_json(record["a"]) for record in customer]
        print(nodes_json)
        return nodes_json


def delete_customer(name):
    _get_connection().execute_query("MATCH (a:employee{name: $name}) delete a;", name=name)
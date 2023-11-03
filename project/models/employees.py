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
    with _get_connection().session() as session:
        employee = session.write_transaction(_save_employee, name, address, branch)
        return [node_to_json(record) for record in employee]


def _save_employee(tx, name, address, branch):
    result = tx.run("MERGE (a:Employee{name: $name, address: $address, branch:$branch}) RETURN a;", name=name,
                    address=address, branch=branch)
    return [node_to_json(record) for record in result]


def update_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee{name: SET a.name=$name, a.address=$address, a.branch=$branch}) "
                               "RETURN a;",
                               name=name,
                               address=address, branch=branch)
        print(employee)
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json


def delete_employee(name):
    with _get_connection().session() as session:
        session.write_transaction(_delete_employee, name)


def _delete_employee(tx, name):
    tx.run("MATCH (a:Employee {name: $name}) DELETE a", name=name)



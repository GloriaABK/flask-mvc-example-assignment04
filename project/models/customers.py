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
    with _get_connection().session() as session:
        customer = session.write_transaction(_save_customer, name, age, address)
        return [node_to_json(record) for record in customer]


def _save_customer(tx, name, age, address):
    result = tx.run("MERGE (a:customer{name: $name, age:$age, address: $address}) RETURN a;", name=name,
                    age=age, address=address)
    return [node_to_json(record) for record in result]


def update_customer(name, age, address):
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer{name: SET a.name=$name, a.age=$age, a.address=$address}) RETURN a;",
                               name=name,
                               age=age,
                               address=address)
        print(customer)
        nodes_json = [node_to_json(record["a"]) for record in customer]
        print(nodes_json)
        return nodes_json


def delete_customer(name):
    with _get_connection().session() as session:
        session.write_transaction(_delete_customer, name)


def _delete_customer(tx, name):
    tx.run("MATCH (a:employee{name: $name}) delete a;", name=name)



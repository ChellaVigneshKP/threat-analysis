import json
from rdflib import Graph
from neo4j import GraphDatabase

# Connect to Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Load and parse JSON-LD data
with open('https://d3fend.mitre.org/ontologies/d3fend.json', 'r') as file:
    json_ld_data = json.load(file)

# Convert JSON-LD to RDF graph
g = Graph().parse(data=json.dumps(json_ld_data), format='json-ld')

# Function to insert data into Neo4j
def insert_defense_data(tx, subj, label, type_, description):
    tx.run('''
        MERGE (n:Defense {id: $id})
        SET n.label = $label, n.type = $type, n.description = $description
        RETURN n
    ''', id=str(subj), label=label, type=type_, description=description)

# Insert defense data into Neo4j
with driver.session() as session:
    for subj, pred, obj in g:
        if str(pred) == 'http://www.w3.org/2000/01/rdf-schema#label':
            label = str(obj)
        elif str(pred) == 'http://www.w3.org/2000/01/rdf-schema#comment':
            description = str(obj)
        elif str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            type_ = str(obj)
        else:
            continue

        session.write_transaction(insert_defense_data, subj, label, type_, description)

driver.close()

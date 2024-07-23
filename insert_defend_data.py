import json
import requests
from rdflib import Graph
from neo4j import GraphDatabase

# Connect to Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "15Ch@05E"
driver = GraphDatabase.driver(uri, auth=(username, password))

# URL of the JSON-LD data
url = 'https://d3fend.mitre.org/ontologies/d3fend.json'

# Fetch the JSON-LD data from the URL
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Save JSON-LD data to a local file with UTF-8 encoding
with open('d3fend.json', 'w', encoding='utf-8') as file:
    file.write(response.text)

# Load and parse JSON-LD data
with open('d3fend.json', 'r', encoding='utf-8') as file:
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
        label = None
        type_ = None
        description = None

        if str(pred) == 'http://www.w3.org/2000/01/rdf-schema#label':
            label = str(obj)
        elif str(pred) == 'http://www.w3.org/2000/01/rdf-schema#comment':
            description = str(obj)
        elif str(pred) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            type_ = str(obj)

        if label or type_ or description:
            session.execute_write(insert_defense_data, subj, label, type_, description)

driver.close()
print("Data insertion completed successfully.")
import requests
from py2neo import Graph, Node

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "15Ch@05E"))


# Function to download and parse JSON data from URL
def fetch_attack_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}")
        return None

# Function to insert data into Neo4j
def insert_data_to_neo4j(data):
    # Create uniqueness constraints if they do not exist
    constraints = graph.run("SHOW CONSTRAINTS").data()
    print("Existing constraints:", constraints)
    constraint_definitions = [constraint['labelsOrTypes'][0] + constraint['properties'][0] for constraint in constraints]

    if 'Techniqueid' not in constraint_definitions:
        print("Creating constraint for Technique id...")
        graph.run("CREATE CONSTRAINT constraint_technique_id FOR (t:Technique) REQUIRE t.id IS UNIQUE")
    else:
        print("Constraint for Technique id already exists.")

    if 'DefensiveTechniqueid' not in constraint_definitions:
        print("Creating constraint for DefensiveTechnique id...")
        graph.run("CREATE CONSTRAINT constraint_defensive_technique_id FOR (d:DefensiveTechnique) REQUIRE d.id IS UNIQUE")
    else:
        print("Constraint for DefensiveTechnique id already exists.")

    # Parse and insert Techniques and their relationships
    for obj in data['objects']:
        if obj['type'] == 'attack-pattern':
            technique_node = Node("Technique", id=obj['id'], name=obj['name'], description=obj.get('description', ''))
            graph.merge(technique_node, "Technique", "id")



# URLs of the ATT&CK JSON data files
urls = [
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-15.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-15.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-14.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-14.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-13.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-13.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-12.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-12.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-11.3.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-11.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-11.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-11.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-10.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-10.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-9.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-8.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-8.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-8.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-7.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-7.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-7.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-6.3.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-6.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-6.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-6.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-5.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-5.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-5.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-4.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-3.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-2.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-1.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-15.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-15.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-14.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-14.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-13.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-13.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-12.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-12.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-11.3.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-11.2-beta.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-11.1-beta.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-11.0-beta.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-10.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-10.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-9.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-8.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-8.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-8.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-7.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-7.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-7.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-6.3.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-6.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-6.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-6.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-5.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-5.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-5.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-4.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-3.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-2.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack-1.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-15.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-15.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-14.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-13.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-13.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-12.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-12.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-11.3.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-11.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-11.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-11.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-10.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-10.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-9.0.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-8.2.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-8.1.json",
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack-8.0.json",

    # Add other URLs as needed
]

# Fetch and insert data from each URL
for url in urls:
    attack_data = fetch_attack_data(url)
    if attack_data:
        insert_data_to_neo4j(attack_data)

print("Data inserted successfully.")

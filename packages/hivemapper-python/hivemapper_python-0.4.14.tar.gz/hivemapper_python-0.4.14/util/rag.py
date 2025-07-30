import csv
from json import loads
from dotenv import load_dotenv
from tqdm import tqdm
from graphrag_sdk.orchestrator import Orchestrator
from graphrag_sdk.agents.kg_agent import KGAgent
from graphrag_sdk.models.openai import OpenAiGenerativeModel
from graphrag_sdk import (
    Ontology, Entity, Relation, Attribute, AttributeType, KnowledgeGraph, KnowledgeGraphModelConfig
)
import concurrent.futures

# Load environment variables
load_dotenv()

# Almanac Ontology
almanac_ontology = Ontology()

# Manually created Ontology by adding entities and relations
almanac_ontology.add_entity(
    Entity(
        label="Region",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="countries",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
            Attribute(
                name="description",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
        ],
    )
)

almanac_ontology.add_entity(
    Entity(
        label="Road",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="length",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
            Attribute(
                name="class",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="intersections",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
        ],
    )
)

almanac_ontology.add_entity(
    Entity(
        label="Intersection",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
        ],
    )
)

almanac_ontology.add_entity(
    Entity(
        label="Place",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="category",
                attr_type=AttributeType.NUMBER,
                required=False,
                unique=False,
            ),
            Attribute(
                name="addresses",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
        ],
    )
)


almanac_ontology.add_entity(
    Entity(
        label="SpeedLimit",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="speedLimit",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
            Attribute(
                name="speedType",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
        ],
    )
)

almanac_ontology.add_entity(
    Entity(
        label="TurnRestriction",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="turnRules",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
        ],
    )
)


almanac_ontology.add_entity(
    Entity(
        label="StopSign",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
        ],
    )
)


almanac_ontology.add_entity(
    Entity(
        label="TrafficLight",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
        ],
    )
)

almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_ROAD",
        source="Region",
        target="Road",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_INTERSECTION",
        source="Region",
        target="Intersection",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_PLACE",
        source="Region",
        target="Place",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_SPEEDLIMIT",
        source="Region",
        target="SpeedLimit",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_SPEEDLIMIT",
        source="Road",
        target="SpeedLimit",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_TURNRESTRICTION",
        source="Region",
        target="TurnRestriction",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_TURNRESTRICTION",
        source="Intersection",
        target="TurnRestriction",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_TRAFFICLIGHT",
        source="Region",
        target="TrafficLight",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_TRAFFICLIGHT",
        source="Intersection",
        target="TrafficLight",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_STOPSIGN",
        source="Region",
        target="StopSign",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONTAINS_STOPSIGN",
        source="Intersection",
        target="StopSign",
    )
)

almanac_ontology.add_relation(
    Relation(
        label="CONNECTS_INTERSECTION",
        source="Road",
        target="Intersection",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="CONNECTS_PLACE",
        source="Road",
        target="Place",
    )
)

# Define the model
model = OpenAiGenerativeModel("gpt-4o")

# Create the KG from the predefined ontology.
almanac_kg = KnowledgeGraph(
    name="almanac",
    ontology=almanac_ontology,
    model_config=KnowledgeGraphModelConfig.with_model(model),
    host='35.89.101.3'
)

print("Loading Regions...")
with open('Region.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'Region',
      {
        "oid": row[1],
        "name": row[2],
        "countries": row[3],
        "description": row[4],
      }
    )

print("Loading Roads...")
num_rows = 0
with open('Road.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
  num_rows = sum(1 for row in reader) - 1
  print(f'{num_rows} rows')

with open('Road.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)

  saw_header = False

  executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
  futures = []

  pbar = tqdm(num_rows)

  def go(row):
    almanac_kg.add_node(
      'Road',
      {
        "oid": row[1],
        "length": float(row[2]),
        "class": row[4],
        "intersections": int(row[5]),
        "name": row[6],
      }
    )
    pbar.update(1)

  for row in reader:
    if not saw_header:
      saw_header = True
      continue
    future = executor.submit(go, row)
    futures.append(future)

  for future in concurrent.futures.as_completed(futures):
    try:
      results = future.result()
    except Exception as e:
      print(e)
  pbar.close()

print("Loading Intersections...")
with open('Intersection.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
  num_rows = sum(1 for row in reader) - 1
  print(f'{num_rows} rows')
with open('Intersection.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')

  saw_header = False

  executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
  futures = []

  pbar = tqdm(num_rows)

  def go(row):
    almanac_kg.add_node(
      'Intersection',
      {
        "oid": row[1],
      }
    )

  for row in reader:
    if not saw_header:
      saw_header = True
      continue
    future = executor.submit(go, row)
    futures.append(future)

  for future in concurrent.futures.as_completed(futures):
    try:
      results = future.result()
    except Exception as e:
      print(e)

print("Loading Places...")
with open('Place.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
  num_rows = sum(1 for row in reader) - 1
  print(f'{num_rows} rows')
with open('Place.csv', newline='') as f:
  reader = csv.reader(f)
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'Place',
      {
        "oid": row[1],
        "name": row[3],
        "category": row[4],
        "addresses": row[5],
      }
    )

print("Loading SpeedLimits...")
with open('SpeedLimit.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'SpeedLimit',
      {
        "oid": row[1],
        "speedType": row[2],
        "speedLimit": row[3],
      }
    )

print("Loading TurnRestrictions...")
with open('TurnRestriction.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'TurnRestriction',
      {
        "oid": row[1],
        "turnRules": row[2],
      }
    )

print("Loading StopSigns...")
with open('StopSign.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'StopSign',
      {
        "oid": row[1],
      }
    )

print("Loading TrafficLights...")
with open('TrafficLight.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_node(
      'TrafficLight',
      {
        "oid": row[1],
      }
    )


print("Loading Region Roads...")
with open('REGION_CONTAINS_ROAD.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_ROAD',
      'Region',
      'Road',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Intersections...")
with open('REGION_CONTAINS_INTERSECTION.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_INTERSECTION',
      'Region',
      'Intersections',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Places...")
with open('REGION_CONTAINS_PLACE.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_PLACE',
      'Region',
      'Place',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Speed Limits...")
with open('REGION_CONTAINS_SPEEDLIMIT.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_SPEEDLIMIT',
      'Region',
      'SpeedLimit',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Turn Restrictions...")
with open('REGION_CONTAINS_TURNRESTRICTION.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_TURNRESTRICTION',
      'Region',
      'TurnRestriction',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Stop Sign...")
with open('REGION_CONTAINS_STOPSIGN.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_STOPSIGN',
      'Region',
      'StopSign',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Region Traffic Light...")
with open('REGION_CONTAINS_TRAFFICLIGHT.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_TRAFFICLIGHT',
      'Region',
      'TrafficLight',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Road Intersections...")
with open('ROAD_CONNECTS_INTERSECTION.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONNECTS_INTERSECTION',
      'Road',
      'Intersections',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Road Places...")
with open('ROAD_CONNECTS_PLACE.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONNECTS_PLACE',
      'Road',
      'Place',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Road SpeedLimits...")
with open('ROAD_CONTAINS_SPEEDLIMIT.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_SPEEDLIMIT',
      'Road',
      'SpeedLimit',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Intersection Turn Restrictions...")
with open('INTERSECTION_CONTAINS_TURNRESTRICTION.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_TURNRESTRICTION',
      'Intersection',
      'TurnRestriction',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Intersection Stop Sign...")
with open('INTERSECTION_CONTAINS_STOPSIGN.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_STOPSIGN',
      'Intersection',
      'StopSign',
      { "oid": row[0] },
      { "oid": row[1] },
    )

print("Loading Intersection TrafficLights...")
with open('INTERSECTION_CONTAINS_TRAFFICLIGHT.csv', newline='') as f:
  reader = csv.reader(f, quotechar='"')
  saw_header = False
  for row in tqdm(reader):
    if not saw_header:
      saw_header = True
      continue
    almanac_kg.add_edge(
      'CONTAINS_TRAFFICLIGHT',
      'Intersection',
      'TrafficLight',
      { "oid": row[0] },
      { "oid": row[1] },
    )

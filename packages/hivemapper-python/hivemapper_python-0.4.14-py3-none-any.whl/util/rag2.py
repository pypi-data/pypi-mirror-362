from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from json import dumps

from dotenv import load_dotenv
from graphrag_sdk.models.openai import OpenAiGenerativeModel
from graphrag_sdk import (
  Ontology, Entity, Relation, Attribute, AttributeType, KnowledgeGraph, KnowledgeGraphModelConfig
)

# Load environment variables
load_dotenv()

# Almanac Ontology
almanac_ontology = Ontology()

def str_attr(name, required = True, unique = False):
  return Attribute(
    name=name,
    attr_type=AttributeType.STRING,
    required=required,
    unique=unique)

H3_KEYS = [f'h3L{i}' for i in range(3, 12)]
H3_ATTRIBUTES = [
  str_attr(key) for key in H3_KEYS
]
OID_ATTR = str_attr('oid', True, True)
LOC_ATTR = Attribute(
  name="loc",
  attr_type=AttributeType.POINT,
  required=True,
  unique=False,
)
AZI_ATTR = Attribute(
  name="azimuth",
  attr_type=AttributeType.NUMBER,
  required=True,
  unique=False,
)
LAST_OBSERVED_ATTR = Attribute(
  name="lastObservedAt",
  attr_type=AttributeType.DATE,
  required=True,
  unique=False,
)
MF_ATTRIBUTES = [OID_ATTR, LOC_ATTR, AZI_ATTR, LAST_OBSERVED_ATTR]
NAME_ATTR = str_attr('name')
PHI_ATTR = Attribute(
  name="phi_vision_output",
  attr_type=AttributeType.TEXT,
  required=False,
  unique=False,
)

# Manually created Ontology by adding entities and relations
almanac_ontology.add_entity(
  Entity(
    label="Region",
    attributes=[
      OID_ATTR,
      NAME_ATTR,
      str_attr('shortName'),
      str_attr('description'),
    ],
    description="A Region is usually a city or metro area that contains roads, intersetions, places, speed limit signs, stop signs, traffic lights, and turn restriction signs."
  )
)

almanac_ontology.add_entity(
  Entity(
    label="Intersection",
    attributes=[
      OID_ATTR,
      LOC_ATTR,
    ] + H3_ATTRIBUTES,
    description="Intersections are connected by Roads. Intersections can have places, stop signs, turn restrictions, and traffic lights."
  )
)

almanac_ontology.add_entity(
  Entity(
    label="Place",
    attributes=[
      OID_ATTR,
      LOC_ATTR,
      NAME_ATTR,
      str_attr('category', False)
      str_attr('address', False)
      Attribute(
        name="text",
        attr_type=AttributeType.TEXT,
        required=True,
        unique=False,
      ),
    ] + H3_ATTRIBUTES,
    description="A Place has a category and a name and are connected by roads.  Places can be schools."
  )
)

almanac_ontology.add_entity(
  Entity(
    label="TurnRestriction",
    attributes=[
      str_attr('rule')
      Attribute(
        name="on_red",
        attr_type=AttributeType.BOOLEAN,
        required=True,
        unique=False,
      ),
      Attribute(
        name="turn_restriction",
        attr_type=AttributeType.STRING,
        required=False,
        unique=False,
      ),
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A turn restriction.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="StopSign",
    attributes= [  
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A stop sign.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="TrafficLight",
    attributes=[
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A traffic light.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="Billboard",
    attributes=[
      PHI_ATTR,
      # str_attr('description', False),
      str_attr('product', False),
      str_attr('advertisingEntity', False),
      str_attr('billboardOwner', False)
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A billboard advertisement. Billboards have a phi_vision_output attribute containing the advertiser, advertisment content, etc.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="TollPrice",
    attributes=[
      PHI_ATTR,
      # str_attr('description', False),
      str_attr('tollPriceInfo', False),
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A sign showing toll prices. TollPrices have a phi_vision_output attribute containing prices and applicable roads or lanes.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="GasPrice",
    attributes=[
      PHI_ATTR,
      # str_attr('description', False),
      str_attr('owner', False),
      str_attr('gasPrices', False),
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A gas station sign showing gas prices. GasPrices have a phi_vision_output attribute containing prices for different types of gasolene.",
  )
)

almanac_ontology.add_entity(
  Entity(
    label="HeightRestriction",
    attributes=[
      PHI_ATTR,
      # str_attr('description', False),
      str_attr('heightRestrictionString', False),
      str_attr('heightRestrictionValue', False),
    ] + MF_ATTRIBUTES + H3_ATTRIBUTES,
    description="A gas station sign showing gas prices. GasPrices have a phi_vision_output attribute containing prices for different types of gasolene.",
  )
)

almanac_ontology.add_relation(
  Relation(
    label="HAS_INTERSECTION",
    source="Region",
    target="Intersection",
  )
)
almanac_ontology.add_relation(
  Relation(
    label="HAS_PLACE",
    source="Region",
    target="Place",
  )
)
def add_road_relation(road_class, description = 'A road segment that connects two intersections.'):
  almanac_ontology.add_relation(
    Relation(
      label=f'ROAD_{road_class.upper()}',
      source="Intersection",
      target="Intersection",
      attributes=[
        OID_ATTR,
        NAME_ATTR,
        LOC_ATTR,
        Attribute(
          name="speedLimit",
          attr_type=AttributeType.NUMBER,
          required=False,
          unique=False,
        ),
        Attribute(
          name="schoolZone",
          attr_type=AttributeType.BOOLEAN,
          required=True,
          unique=False,
        ),
        str_attr('regulatorySpeedLimitMF', False),
        str_attr('class'),
        Attribute(
          name="length",
          attr_type=AttributeType.NUMBER,
          required=True,
          unique=False,
        ),
      ] + H3_ATTRIBUTES,
    )
  )
add_road_relation(
  'motorway',
  'A restricted access major divided highway, normally with 2 or more running lanes plus emergency hard shoulder. Equivalent to the Freeway, Autobahn, etc.')
add_road_relation(
  'trunk',
  'The most important roads in a country\'s system that aren\'t motorways. (Need not necessarily be a divided highway.)')
add_road_relation(
  'primary',
  'The next most important roads in a country\'s system. (Often link larger towns.)')
add_road_relation(
  'secondary',
  'The next most important roads in a country\'s system. (Often link towns.)')
add_road_relation(
  'tertiary',
  'The next most important roads in a country\'s system. (Often link smaller towns and villages)')
add_road_relation(
  'unclassified',
  'The least important through roads in a country\'s system – i.e. minor roads of a lower classification than tertiary, but which serve a purpose other than access to properties. (Often link villages and hamlets.) The word \'unclassified\' is a historical artefact of the UK road system and does not mean that the classification is unknown.')
add_road_relation(
  'residential',
  'Roads which serve as an access to housing, without function of connecting settlements. Often lined with housing.')
add_road_relation(
    'service',
    'For access roads to, or within an industrial estate, camp site, business park, car park, alleys, etc.')

# almanac_ontology.add_relation(
#   Relation(
#     label="IS_NEAR_PLACE",
#     source="Intersection",
#     target="Place",
#   )
# )
# almanac_ontology.add_relation(
#   Relation(
#     label="NEAREST_INTERSECTION",
#     source="Place",
#     target="Intersection",
#   )
# )
# almanac_ontology.add_relation(
#   Relation(
#     label="HAS_STOPSIGN",
#     source="Intersection",
#     target="StopSign",
#   )
# )
# almanac_ontology.add_relation(
#   Relation(
#     label="HAS_TURNRESTRICTION",
#     source="Intersection",
#     target="TurnRestriction",
#   )
# )
# almanac_ontology.add_relation(
#   Relation(
#     label="HAS_TRAFFICLIGHT",
#     source="Intersection",
#     target="TrafficLight",
#   )
# )

# Define the model
model = OpenAiGenerativeModel("gpt-4o")

# Create the KG from the predefined ontology.
almanac_kg = KnowledgeGraph(
  name="almanac2",
  ontology=almanac_ontology,
  model_config=KnowledgeGraphModelConfig.with_model(model),
  host='10.0.0.132'
)

chat = almanac_kg.chat_session()

app = FastAPI()

class Item(BaseModel):
    prompt: str
    cells: List[str]
    res: str

@app.get('/ping')
def test():
    return "pong"

@app.post('/routeintelligence')
def route_intel(item: Item):
    print(item)
    route = dumps({"cells":item.cells, "res":item.res})
    query = f'Route: {route}\nPrompt:{item.prompt}\nShow the results.'
    try:
        fc, cypher = chat.send_message(query)
    except Exception as e:
        print(e)
        import traceback
        print(traceback.format_exc())

        return { 'error': e }
    return { 'fc': fc, 'cypher': cypher }

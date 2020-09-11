from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI

import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_md
nlp = spacy.load('en_core_web_md')


#init app
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://localhost:3000",
    "https://spacy-entity-recognition-api.herokuapp.com/ "
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entity(BaseModel):
    entity_type: str
    text: str
    
#Routes 
@app.post('/recognize_entity/')
def recognize_entity(entity: Entity):
    if entity.entity_type:
        doc = nlp(entity.text)
        d = []
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=('named entity', 'output'))
            ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
            PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
            GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
            MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
            LOC_named_entity = df.loc[df['named entity'] == 'LOC']['output']
            PRODUCT_named_entity = df.loc[df['named entity'] == 'PRODUCT']['output']
            EVENT_named_entity = df.loc[df['named entity'] == 'EVENT']['output']
            WORK_OF_ART_named_entity = df.loc[df['named entity'] == 'WORK_OF_ART']['output']
            LAW_named_entity = df.loc[df['named entity'] == 'LAW']['output']
            FAC_named_entity = df.loc[df['named entity'] == 'FAC']['output']

        if entity.entity_type == 'organizations':
            results = ORG_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'persons':
            results = PERSON_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'geopolitical':
            results = GPE_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'money':
            results = MONEY_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'locations':
            results = LOC_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'products':
            results = PRODUCT_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'events':
            results = EVENT_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'laws':
            results = LAW_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'fac':
            results = FAC_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
        elif entity.entity_type == 'work of art':
            results = WORK_OF_ART_named_entity
            num_of_results = len(results)
            return {'results': results, 'num_of_results': num_of_results}
    
    # return {'results': results, 'num_of_results': num_of_results}

if  __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)    

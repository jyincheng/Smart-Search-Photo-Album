import json
import boto3
import time
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection

esEndPoint = "https://search-photos-qhkfovk66fopo2depkb4a4euzm.us-east-1.es.amazonaws.com"

def set_response(code, body):
     return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    print("#####START#####")
    search = event['queryStringParameters']
    
    if not search:
        return set_response(400, "Bad request, there was nothing in the query params")
    
    esClient = Elasticsearch(esEndPoint, use_ssl=True, verify_certs=True, connection_class=RequestsHttpConnection, http_auth=('esuser', 'Aws.!2345'))
    print("es connected")
    
    query_text = search['q']
    
    keywords = []
    if ' ' in query_text:
        print(f"Start Lex {query_text}")
        lexClient = boto3.client('lex-runtime')
        print(lexClient)
        response = lexClient.post_text( botName = 'search_bot',
            botAlias = 'v_c',
            userId = 'lexuser',
            inputText = query_text
        )
        print(response)
        
        slots = response['slots']
        # Find me tree -> Find me {objecta -> tree} 
        
        keywords = [s for _, s in slots.items() if s]
    else:
        keywords.append(query_text)
    
    # for _, s in slots.items():
    #     if s : 
    #         keywords.append(s)

    print(f"Keywords: {keywords}")
    if not keywords:
        return set_response(400, keywords)
    
    queries = []
    for keyword in keywords:
        queries.append({"match": {"labels": keyword}})
    
    final_query = {"query": {"bool": {"should": queries}}}
    
    res = esClient.search(index="album", body=final_query)
    
    images = []
    for img in res['hits']['hits']:
        objectKey = img['_source']['objectKey']
        bucket = img['_source']['bucket']
        image_url = f"https://{bucket}.s3.amazonaws.com/{objectKey}"
        images.append(image_url)
    
    images = list(set(images))
    print(f"{images}")
    
    return set_response(200, images)


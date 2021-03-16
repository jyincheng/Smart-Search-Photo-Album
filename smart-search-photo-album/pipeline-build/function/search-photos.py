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
    
    # if query_text == "voiceSearch":
    #     transcribe = boto3.client('transcribe')
    #     job_name = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()).replace(":", "-").replace(" ", "")
    #     job_uri = "https://s3.amazonaws.com/b2-photo/test.mp3"
    #     transcribe.start_transcription_job(
    #         TranscriptionJobName=job_name,
    #         Media={'MediaFileUri': job_uri},
    #         MediaFormat='mp3',
    #         LanguageCode='en-US'
    #     )
    #     while True:
    #         status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    #         if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
    #             break
    #         print("Not ready yet...")
    #         time.sleep(5)

    #     print("Transcript URL: ", status)
    #     transcriptURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    #     trans_text = requests.get(transcriptURL).json()
        
    #     print("Transcripts: ", trans_text)
    #     print(trans_text["results"]['transcripts'][0]['transcript'])
        
    #     s3Client = boto3.client('s3')
    #     response = s3Client.delete_object(
    #         Bucket='b2-photo',
    #         Key='test.mp3'
    #     )
    #     query_text = trans_text["results"]['transcripts'][0]['transcript']
    #     s3Client.put_object(Body=query_text, Bucket='b2-photo', Key='test.txt')

    #     return {
    #       'statusCode': 200,
    #       'headers': {
    #         "Access-Control-Allow-Origin": "*"
    #       },
    #       'body': "transcribe done"
    #     }
        
    # if query_text == "voiceResult":
    #     s3Client = boto3.client('s3')
    #     data = s3Client.get_object(Bucket='b2-photo', Key='test.txt')
    #     query_text = data.get('Body').read().decode('utf-8')

    #     print("Voice query: ", query_text)
    #     s3Client.delete_object(
    #       Bucket='b2-photo',
    #       Key='test.txt'
    #     )
    
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
    
    print(f"{images}")
    
    return set_response(200, images)


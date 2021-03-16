import json
import time
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection

esEndPoint = "https://search-photos-qhkfovk66fopo2depkb4a4euzm.us-east-1.es.amazonaws.com"

def lambda_handler(event, context):
    print("#####PIPELINETEST#####")

    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    photo = record['s3']['object']['key']
    
    s3Client = boto3.resource('s3')
    object = s3Client.Object(bucket, photo)
    print("s3 connected")
    
    if photo == "test.mp3":
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT',
                'Access-Control-Allow-Headers': 'Content-Type'
             },
            'body': json.dumps('Hello from Lambda!')
        }
        
    rekClient = boto3.client('rekognition')
    esClient = Elasticsearch(esEndPoint, use_ssl=True, verify_certs=True, connection_class=RequestsHttpConnection, http_auth=('esuser', 'Aws.!2345'))
    print("es connected")
    
    # esClient.indices.delete(index="album", ignore=[404, 400])
    
    print(f"Bucket: {bucket}, Photo: {photo}")
    try:
        print("#####TRY#####")
        response = rekClient.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, MaxLabels=10, MinConfidence=90)
        
        labels = [label['Name'] for label in response['Labels']]

        # labels = []
        # for label in response['Labels']:
        #     if label['Confidence'] >= 90:
        #         labels.append(label['Name'])
        
        customLabels = []
        if hasattr(object.metadata, 'customlabels'):
            customLabels = object.metadata['customlabels'].split(', ')
        
        labels += customLabels
        
        print(f"labels: {labels}")
        
        data = {
            "objectKey": photo,
            "bucket": bucket,
            "createdTimestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "labels": labels
        }

        print(data)
        
        encoded_body = json.dumps(data)
        
        esClient.index(index="album", doc_type="photo", body=encoded_body)
        
        print("#####END#####")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT',
                'Access-Control-Allow-Headers': 'Content-Type'
             },
            'body': json.dumps('Hello from Lambda!')
        }
    except Exception as e:
        print("Error " + str(e))

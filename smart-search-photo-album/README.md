# CloudComputing_Clever_Photo_Album #

## Overview ##
Customer Service is a core service for a lot of businesses around the world, and it is getting disrupted at the moment by Natural Language Processing-powered applications. The [Clever_Photo_Album](https://cloud-computing-a2-b1.s3.amazonaws.com/index.html) is a serverless, micro service-driven web application that offers users an intelligent album. It not only allows users to upload their photos but search by natural language. Besides, this album supports customized labels assigned by users.

## Demo ##
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/cat_and_dog.png)

## Application (Language & Tools) ##
1) Frontend: CSS, HTML, JavaScript
2) Backend: AWS Serverless ([S3](https://aws.amazon.com/s3/), [Lambda](https://aws.amazon.com/lambda/), [API Gateway](https://aws.amazon.com/apigateway/), [Lex](https://aws.amazon.com/lex/), webkitSpeechRecognition, [Rekognition](https://aws.amazon.com/rekognition/), [ElasticSearch](https://aws.amazon.com/es/), [Codebuild](https://docs.aws.amazon.com/codebuild/), [Cloudformation](https://aws.amazon.com/cloudformation/)), Swagger API, PyThon


## Architecture ##
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/architecture.png)
1) User -> Frontend (chat.html / AWS S3): user input "hello" to initiate the conversation
2) Frontend -> API: send user's messages to API.
3) API -> Put images into B2 and get photo path by LF2
4) LF1 -> Insert photos' indices
5) LF2 -> Search photos
6) Lex -> Retrieve objects from natural language
7) Rekognition -> Return objects in images.
8) webkitSpeechRecognition -> Speech to texts conversion.
9) ES -> Search photo's indices
10) CodeBuild -> Github pushes update lambda automatically.
11) Cloudformation -> Deploy all facilities except Lex by one button.


## Description ##
#### 1) [S3](https://aws.amazon.com/s3/) - B1
- Store the frontend files.
- Generate SDK from AWS API Gateway and store it into js folder.
- Create CORS policy.

#### 2) [S3](https://aws.amazon.com/s3/) - B2
- Store image files.
- Trigger LF1.

#### 3) [API Gateway](https://aws.amazon.com/apigateway/)
- Create a new API by importing swagger API.
- Set PUT method triggering Bucket B2.
- Set GET method and integrate LF2.
- Set OPTIONS method and its response method with HTTP status 200.
- Enable CORS.
- Deploy API.
- Generate SDK for frontend.

#### 4) [Lambda](https://aws.amazon.com/lambda/) - LF1
- Get photo labels from AWS Rekognition
- Insert photos' indices into elasticsearch

#### 5) [Lex](https://aws.amazon.com/lex/)
- Retrieve objects from natural language.
- Support at most two objects.

#### 6) [Lambda](https://aws.amazon.com/lambda/) - LF2
- Use Lex to get objects' names, put them into elasticsearch, then return the image path.

#### 7) [Rekognition](https://aws.amazon.com/rekognition/)
- Standard application with confidence level 90.

#### 8) [ElasticSearch](https://console.aws.amazon.com/es/home)
- Store photos with labels.

#### 9) webkitSpeechRecognition
- Converts speech to texts.

#### 10) [CodeBuild](https://aws.amazon.com/CodeBuild/)
- Build lambda Code in pipeline.

#### 11) [Cloudformation](https://aws.amazon.com/Cloudformation/) 
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/cloudformation.png)
Quick/Automatic deployment by cloudformation

*AWS Region: US-east-1 (N. Virginia)


## Contributor ##
#### [Tim Kao](https://github.com/tim-kao) (UNI: sk4920)
#### [Yin Cheng](https://github.com/jyincheng)(UNI: cc4717)

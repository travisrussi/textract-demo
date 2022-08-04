import random

def start_job(client, bucketName, fileName):
    try:
        response = client.start_document_text_detection(
                   DocumentLocation={'S3Object': {'Bucket': bucketName, 'Name': fileName} },
                #    FeatureTypes=["TABLES"],
                   ClientRequestToken=str(random.randint(1,1e10)))

        # jobId = response["JobId"]
        # metaData = response["ResponseMetadata"]

        jobId = response['JobId']
        print("jobId: "+ jobId)
    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    return jobId

def check_status(client, jobId):
    try:
        response = client.get_document_text_detection(JobId=jobId)
        # print("get_response:\n=================\n"+ response)

        # jobStatus = response["JobStatus"]
        # detectDocumentTextModelVersion = response["DetectDocumentTextModelVersion"]
        # responseMetadata = response["ResponseMetadata"]

        jobStatus = response["JobStatus"]
        print("jobStatus: " + jobStatus)
    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    return jobStatus

def get_result(client, jobId):
    try:
        response = client.get_document_text_detection(JobId=jobId)
        # print("get_response:\n=================\n"+ response)

        # documentMetadata = response["DocumentMetadata"]
        # jobStatus = response["JobStatus"]
        # blocks = response["Blocks"]
        # detectDocumentTextModelVersion = response["DetectDocumentTextModelVersion"]
        # responseMetadata = response["ResponseMetadata"]

        blocks = response["Blocks"]
        print("blocks: " + blocks)
    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    return blocks

def get_response(client, jobId):
    try:
        response = client.get_document_text_detection(JobId=jobId)
        # print("get_response:\n=================\n"+ response)

        # documentMetadata = response["DocumentMetadata"]
        # jobStatus = response["JobStatus"]
        # blocks = response["Blocks"]
        # detectDocumentTextModelVersion = response["DetectDocumentTextModelVersion"]
        # responseMetadata = response["ResponseMetadata"]
    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    return response
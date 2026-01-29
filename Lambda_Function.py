import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    # !!! CHANGE THIS TO YOUR BUCKET NAME !!!
    BUCKET_NAME = "my-photo-uploader-2026" 
    
    # Get details from the website request
    params = event.get('queryStringParameters', {})
    file_name = params.get('filename', 'image.jpg')
    file_type = params.get('type', 'image/jpeg')

    try:
        # Generate the temporary upload link
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name, 'ContentType': file_type},
            ExpiresIn=300
        )
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            },
            'body': json.dumps({'uploadUrl': url})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}
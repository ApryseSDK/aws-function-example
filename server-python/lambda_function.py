# This example shows how to create AWS Lambda functions using PDFTron SDK.
# A REST API request was posted with base64 encoded data by the client.
# The request would be processed by the server and a response with base64 encoded data of OfficeToPDF output would be sent to the client.

from base64 import b64encode, b64decode
import json

from PDFNetPython3 import *

def lambda_handler(event, context):
    if event["httpMethod"] == "GET":
        return {
            'statusCode': 200,
            'body': json.dumps('Hello, please send base64 doc to use this Lambda function!')
        }

    elif event["httpMethod"] == "POST":
        try:
            body = json.loads(event["body"])
            base64str = body["file"]["data"]
            filename = body["file"]["filename"]
            base64_bytes = b64decode(base64str)
            # save input doc
            output_path = '/tmp/'
            input_filename = filename.split('.')[0] + '.docx'
            with open(output_path + input_filename, 'wb') as open_file:
                byte_content = open_file.write(base64_bytes)
            # Start with a PDFDoc
            PDFNet.Initialize()
            pdfdoc = PDFDoc()
            # perform the conversion with no optional parameters
            Convert.OfficeToPDF(pdfdoc, output_path + input_filename, None)
            # save the result
            output_filename = filename.split('.')[0] + '.pdf'
            pdfdoc.Save(output_path + output_filename, SDFDoc.e_linearized)

            # sending data
            with open(output_path + output_filename, 'rb') as open_file:
                byte_content = open_file.read()
            base64_bytes = b64encode(byte_content)
            base64_string = base64_bytes.decode('utf-8')

            print("Sending " + output_filename )
            message = {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(base64_string),
            }
            return message
        except Exception as e:
            print(e)
            message = {
                'statusCode': 500,
                'body': e
                }
            return (message)

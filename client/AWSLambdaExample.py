#--------------------------------------------------------------------------------------------------------------
# This example shows how to post an office document to server via a REST API request using base64 encoding
# and then wait for the response from server and finally save the received pdf data
#--------------------------------------------------------------------------------------------------------------

from base64 import b64encode, b64decode
from json import dumps, loads
import argparse, os, sys
import requests

def execute(url, input_path, output_path, filename):
    try:
        # post a request
        with open(input_path + filename, 'rb') as open_file:
            byte_content = open_file.read()
        base64_bytes = b64encode(byte_content)
        base64_string = base64_bytes.decode('utf-8')
        raw_data = {
            "@type": "File",
            "title": "Sending base64 encoded office data.",
            "file": {
                "encoding": "base64",
                "data": base64_string,
                "filename": filename,
                "content-type": "application/pdf"
            }
        }

        res = requests.post(url,  headers={ 'Accept': 'application/json', 'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', }, json=raw_data)
        print("\nPosting a request to %s \n..." % res.url)
       
        # wait for response
        print("\nWaiting for response...\n")
        print(res.json())
        base64str = res.json()
        base64_bytes = b64decode(base64str)
        output_filename = filename.split('.')[0] + '.pdf'
        with open(output_path + output_filename, 'wb') as open_file:
            byte_content = open_file.write(base64_bytes)

        print("\nSaving output in %s%s ..." % (output_path, output_filename))
        print("\nDone!")
        return 0

    except Exception as e:
        print(e)
        return 1

def main():
    parser = argparse.ArgumentParser(description="Example of posting a request to PDFNet.OfficeToPDF() AWS Lambda Function.")
    parser.add_argument('--url',help="URL of PDFNet's AWS Lambda functions.", default ='<YOUR PUBLISHED FUNCTION URL>', dest='url')
    parser.add_argument('--input_path', '-i' ,help="Input path where office files are stored.", default ='./input/', dest='input_path')
    parser.add_argument('--output_path','-o',help='Output path where Office2PDF files are stored.', default ='./output/',dest='output_path')
    parser.add_argument('--filename', '-f', help='Input filename.', default ='simple-word_2007.docx', dest='filename')
    args = parser.parse_args()
    url = args.url
    input_path = args.input_path
    output_path = args.output_path
    filename = args.filename
    return execute(url, input_path, output_path, filename)

if __name__ == '__main__':
    sys.exit(main())
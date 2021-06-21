Prerequisite: Python
- Install requests package if applicable:
    $python -m pip install requests

Usage: AWSLambdaExample.py [-h] [--url URL] [--input_path INPUT_PATH]
                       [--output_path OUTPUT_PATH] [--filename FILENAME]

Example of calling PDFNet.OfficeToPDF() AWS Lambda functions.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL of PDFNet's AWS Lambda functions.
  --input_path INPUT_PATH, -i INPUT_PATH
                        Input dir where office files are stored.
  --output_path OUTPUT_PATH, -o OUTPUT_PATH
                        Output dir where Office2PDF files are stored.
  --filename FILENAME, -f FILENAME
                        Input filename.
                        
Example
$cd client
$python AWSLambdaExample.py --url <PUBLISHED FUNCTION URL> --input_path ./input/ --output_path ./output/ --filename simple-word_2007.docx

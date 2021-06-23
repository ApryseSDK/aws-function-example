// This example shows how to create AWS Lambda functions using PDFTron SDK.
// A REST API request was posted with base64 encoded data by the client.
// The request would be processed by the server and a response with base64 encoded data of OfficeToPDF output would be sent to the client.

const { PDFNet } = require('@pdftron/pdfnet-node');

exports.handler = async (event) => {
    let response = null;
    if(event["httpMethod"] != "POST")
    {
        response = {
            statusCode: 200,
            body: JSON.stringify('Hello, please send base64 doc to use this Lambda function!'),
        };
    }
    else
    {
        const main = async () => {
            // parsing
            let body = JSON.parse(event.body);
            let base64str = body.file.data;
            let filename = body.file.filename; 
            let base64_bytes = Buffer.from(base64str, 'base64');

            // save input doc to /tmp
            const outputPath = '/tmp/';
            const path = require('path');
            const inputFilename = path.parse(filename).name + '.docx';
            const fs = require('fs');
            fs.writeFileSync(outputPath + inputFilename, base64_bytes);
            // perform the conversion with no optional parameters
            const pdfdoc = await PDFNet.Convert.officeToPdfWithPath(outputPath + inputFilename);
            // save the result
            const outputFilename = path.parse(filename).name + '.pdf';
            await pdfdoc.save(outputPath + outputFilename, PDFNet.SDFDoc.SaveOptions.e_linearized);
            console.log('Saved ' + outputFilename);

            // sending data
            let buff = fs.readFileSync(outputPath + outputFilename);
            let base64_string = buff.toString('base64');
            response = {
                statusCode: 200,
                body: JSON.stringify(base64_string),
            };
        };
        await PDFNet.runWithCleanup(main).catch(function (error) {
        console.log('Error: ' + JSON.stringify(error));
        response = {
                statusCode: 500,
                body: JSON.stringify(error),
            };
        }).then(function () { PDFNet.shutdown(); });
    }
    return response;
};
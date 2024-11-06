
### Summary of the Lambda Function (EVTX-XML-LARGE)

This AWS Lambda function processes `.evtx` (Windows Event Log) files uploaded to an S3 bucket by:

1. **Extracting Event Logs**: Downloads the `.evtx` file from S3 and reads the log records in chunks.
2. **Chunking Records**: Processes records in chunks of 1,000 events at a time, converting each event record to XML format, removing unnecessary line breaks, and decoding HTML entities.
3. **Saving Chunks**: Writes each processed chunk to a temporary file.
4. **Uploading to S3**: Uploads each chunk as a new `.txt` file to the same S3 bucket with a modified filename to indicate the chunk number.
5. **Reinvoking Itself**: If there are remaining records to process, it reinvokes itself with updated parameters to process the next chunk.

### Steps to Upload a Lambda Function as a Zip File

To deploy this Lambda function, follow these steps:

#### 1. Prepare the Lambda Function Files

- Ensure your Lambda code and dependencies are in one folder.
- Include all necessary libraries (like `Evtx`) alongside the function code if not available in AWS Lambda's execution environment.

#### 2. Create a Zip File (If the file is not zipped already)

```bash
zip -r EVTX-XML-LARGE.zip .
```

This command zips all files in the current directory into `EVTX-XML-LARGE.zip`.

#### 3. Upload the Zip File to Lambda Console

1. Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select or create your Lambda function.
3. Under **Code source**, select **Upload from** > **.zip file**.
4. Click **Upload**, choose `EVTX-XML-LARGE.zip`, and save.

#### 4. (Optional) Use AWS CLI for Uploading

Alternatively, you can use the AWS CLI:

```bash
aws lambda update-function-code --function-name YOUR_FUNCTION_NAME --zip-file fileb://EVTX-XML-LARGE.zip
```

Replace `YOUR_FUNCTION_NAME` with your Lambda function's name. This command uploads and updates the function code in Lambda.

#### 5. Configure the Function

- Set **Memory** and **Timeout** values to handle larger `.evtx` files.
- - For ours the Memory is set to Maximum as it scales with CPU allocation and timeout is set to max at 15min.
- Ensure the Lambda function has permission to read/write to S3 by attaching an appropriate IAM role.

This should deploy and configure the Lambda function to start processing `.evtx` files when they are uploaded to the specified S3 bucket.

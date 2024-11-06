## Step 1: Set Up AWS OpenSearch Domain

1. **Log in** to the [AWS Management Console](https://aws.amazon.com/console/).
2. **Navigate** to **Amazon OpenSearch Service** under **Analytics**.
3. **Create a new domain** or select an existing domain to use for this pipeline.
4. Ensure that your domain has sufficient permissions and resources to handle log ingestion, processing, and anomaly detection.

## Step 2: Create IAM Roles for Pipeline Access

1. **Create an IAM role** with permissions to access your OpenSearch domain and any required S3 buckets.
2. Ensure the role has a trust relationship with `osis-pipelines.amazonaws.com`.
3. **Attach policies** that allow the role to:
   - Access and write to the OpenSearch domain.
   - Write to an S3 bucket for Dead Letter Queue (DLQ) if needed.

## Step 3: Define Your Pipeline Configuration

You will need to create a YAML configuration file that defines the structure of your OpenSearch pipeline.

### Example Configuration

Below is an example pipeline configuration:

```yaml
version: "2"
log-pipeline:
  source:
    http:
      path: "/syslog-pipeline/logs"
  processor:
    - grok:
        match:
          log: [ "%{SYSLOGBASE}" ]
  sink:
    - opensearch:
        hosts: [ "https://<your-opensearch-endpoint>" ]
        aws:
          sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
          region: "<your-region>"
          serverless: false
        index: "<your-index-name>"
        dlq:
          s3:
            bucket: "<your-s3-bucket>"
            region: "<your-region>"
            sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
```

### Configuration Breakdown

- **apache-log-pipeline-with-metrics**: Ingests Apache logs via HTTP, parses them using Grok, and stores them in an OpenSearch index.
- **log-to-metrics-pipeline**: Aggregates logs into metrics, storing them in a different OpenSearch index.
- **log-to-metrics-anomaly-detector-pipeline**: Runs anomaly detection on the metrics and stores the results in another OpenSearch index.

## Step 4: Deploy the Pipeline

1. **Log in** to the [OpenSearch Ingestion Service](https://opensearch.aws.amazon.com/).
2. **Create a new pipeline** and upload your YAML configuration file.
3. **Deploy** the pipeline by following the prompts.

![image](https://github.com/user-attachments/assets/5b89da60-85a4-4cc9-938c-079defe45d43)

## Step 5: Test the Pipeline

1. **Send test logs** to your pipeline’s HTTP endpoint.
2. **Verify** that logs are ingested, processed, and anomalies are detected by checking your OpenSearch Dashboards.

![image](https://github.com/user-attachments/assets/1772e0f8-f424-4705-96c7-bd6495178519)

## Step 6: Monitor and Maintain

1. Regularly **monitor the pipeline** for performance and anomalies.
2. **Adjust configurations** as needed to optimize performance or handle new log formats.

Here’s an expanded guide with additional sections on adding multiple sinks, custom Grok patterns, and routing within OpenSearch pipelines.

---
#Once The Basic Pipeline Is Created You Can Customize With

## Multiple Sinks, Grok Patterns, Routing

## Step 7: Add Multiple Sinks

Adding multiple sinks allows you to send logs to more than one destination, such as multiple OpenSearch indexes or an S3 bucket for backup.

### Adding Multiple Sinks Example

Update your pipeline configuration file to include additional sinks. For example, if you want to send logs to both an OpenSearch index and an S3 bucket:

```yaml
version: "2"
log-pipeline:
  source:
    http:
      path: "/syslog-pipeline/logs"
  processor:
    - grok:
        match:
          log: [ "%{SYSLOGBASE}" ]
  sink:
    - opensearch:
        hosts: [ "https://<your-opensearch-endpoint>" ]
        aws:
          sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
          region: "<your-region>"
          serverless: false
        index: "<your-index-name>"
    - s3:
        bucket: "<your-s3-bucket>"
        region: "<your-region>"
        sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
```

### Sink Breakdown

- **opensearch**: Sends logs to your OpenSearch index.
- **s3**: Stores logs in an S3 bucket, providing an additional backup.

> **Note:** Ensure each sink is appropriately configured with permissions and resource access in IAM.

---

## Step 8: Define Custom Grok Patterns

Custom Grok patterns allow you to parse specific log formats not covered by built-in patterns. This flexibility is particularly useful for unique log structures.

### Adding Custom Grok Patterns

1. In the **processor** section of your pipeline configuration, define custom Grok patterns under `patterns`:

   ```yaml
   processor:
     - grok:
         patterns:
           CUSTOM_LOG: "%{TIMESTAMP_ISO8601:timestamp} %{WORD:log_level} %{DATA:message}"
         match:
           log: [ "%{CUSTOM_LOG}" ]
   ```

2. **Explanation**:
   - **CUSTOM_LOG**: Defines a custom pattern. In this example, it captures an ISO8601 timestamp, a log level (e.g., INFO, ERROR), and the rest of the log as a message.
   - **match**: Specifies that `log` entries will be matched against the custom `CUSTOM_LOG` pattern.

> **Tip:** Add multiple patterns for various log structures as needed.

---

## Step 9: Implement Routing in OpenSearch Pipelines

Routing lets you direct logs to different sinks or processors based on certain conditions, such as the log type or content.

### Example of Routing Configuration

Below is an example of how to route logs based on specific log types (e.g., Apache vs. syslog) using conditions.

```yaml
version: "2"
log-pipeline:
  source:
    http:
      path: "/log-ingestion"
  processor:
    - grok:
        match:
          log: [ "%{SYSLOGBASE}" ]
        route:
          - condition: "'apache' in log"  # Check if the log contains 'apache'
            sink:
              opensearch:
                hosts: [ "https://<your-opensearch-endpoint>" ]
                aws:
                  sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
                  region: "<your-region>"
                  serverless: false
                index: "apache-logs-index"
          - condition: "'syslog' in log"  # Check if the log contains 'syslog'
            sink:
              opensearch:
                hosts: [ "https://<your-opensearch-endpoint>" ]
                aws:
                  sts_role_arn: "arn:aws:iam::<your-account-id>:role/<your-iam-role>"
                  region: "<your-region>"
                  serverless: false
                index: "syslog-index"
```

### Routing Breakdown

- **condition**: Defines criteria for routing. For example, if the log entry contains "apache," it will be routed to `apache-logs-index`.
- **sink**: Specifies the destination for each routed log type, with separate indexes for Apache and syslog logs.

> **Tip:** You can add more conditions and routes to handle different log sources or formats.

This setup enhances log processing flexibility, allowing for tailored log handling and storage across multiple AWS services.


<img width="1245" alt="Screenshot 2024-11-07 at 8 23 22 AM" src="https://github.com/user-attachments/assets/e1b53eda-bdde-4e8d-b892-57f125277293">
# Creating Security Alerts in OpenSearch

## Overview
This guide explains the process for setting up security alerts in OpenSearch to monitor and respond to significant events. Security alerts provide an automated way to track unusual activities, such as unauthorized access or data anomalies, and help ensure timely responses.

## Prerequisites
- An OpenSearch cluster with indexed log data.
- Access to OpenSearch Dashboards.
- Proper configurations for alerting and monitoring.

## Step-by-Step Process

### Step 1: Accessing the Alerting Plugin
1. Log in to your OpenSearch Dashboard instance.
2. Navigate to **Alerting** on the left panel.

### Step 2: Creating a Monitor
1. Click **Create Monitor** to start the process.
2. Choose the method for your monitor:
   - **Define using extraction query** or **Define using visual graph** based on your data needs.
3. Set a unique name for the monitor and specify the index pattern that the monitor will track.
4. Define a query to specify the conditions that trigger the alert (e.g., `event_id: 4656` for high access requests).

### Step 3: Setting Trigger Conditions
1. Scroll down to the **Triggers** section and click **Create Trigger**.
2. Name your trigger and set the severity (e.g., High, Medium, Low).
3. Enter a trigger condition using painless scripting (e.g., `ctx.results[0].hits.total.value > 5` to trigger an alert when more than 5 matching events are detected).
4. Define the action message to be sent when the alert is triggered.

### Step 4: Configuring Notification Channels
1. Select or create a notification channel (e.g., email, Slack, or webhooks) to receive alert notifications.
2. Add a detailed message template that includes relevant event details, such as:
    Monitor {{ctx.monitor.name}} triggered an alert.
      Trigger: {{ctx.trigger.name}}
      Severity: {{ctx.trigger.severity}}
      Event ID: {{ctx.results[0]._source.event_id}}
      Timestamp: {{ctx.results[0]._source.@timestamp}}

### Step 5: Saving and Activating the Monitor
1. Review the monitor configuration.
2. Click **Create** to save and activate the monitor.
3. Ensure the monitor is enabled for it to actively track conditions and send alerts.

## Example Use Case
- **Monitoring High Access Requests**: Create a monitor to detect unusual access patterns on sensitive objects, configured to send a Slack notification when triggered.

### Sample Alert Notification Template
High Access Requests Detected on Sensitive Object Monitor {{ctx.monitor.name}} just entered alert status. Please investigate the issue.

Trigger: {{ctx.trigger.name}}
Severity: {{ctx.trigger.severity}}
Period start: {{ctx.periodStart}}
Period end: {{ctx.periodEnd}}


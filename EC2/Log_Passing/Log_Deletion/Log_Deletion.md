
# Creating A System Service To Automatically Remove Files From A Directory

### Step 1: Create the Python Script

1. Save your Python script as `file_deletion_service.py` in a suitable directory, such as `/home/ec2-user/scripts/`.

### Step 2: Create a Systemd Service File

1. Open a new file in the systemd directory for defining the service:

   ```bash
   sudo nano /etc/systemd/system/file_deletion_service.service
   ```

2. Add the following configuration to define the service:

   ```ini
   [Unit]
   Description=File Deletion Service
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/ec2-user/scripts/file_deletion_service.py
   Restart=on-failure
   User=ec2-user
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```

   - Ensure `ExecStart` points to the correct path of your script and the Python interpreter.
   - Adjust `User` to the appropriate user (e.g., `ec2-user`).

### Step 3: Reload Systemd to Recognize the New Service

```bash
sudo systemctl daemon-reload
```

### Step 4: Start and Enable the Service

1. Start the service immediately:

   ```bash
   sudo systemctl start file_deletion_service
   ```

2. Enable the service to start on boot:

   ```bash
   sudo systemctl enable file_deletion_service
   ```

### Step 5: Check the Service Status

Verify that the service is running correctly:

```bash
sudo systemctl status file_deletion_service
```

You should see that the service is "active (running)" if it started successfully.

### Step 6: View Logs (Optional)

To monitor the output logs from your script, use `journalctl`:

```bash
sudo journalctl -u file_deletion_service.service -f
```

### Summary

Now, your Python script will run as a system service on AWS Linux 2, deleting files from `/var/log/s3_logs` based on the specified conditions. The service will automatically restart if it fails and will run on every boot.

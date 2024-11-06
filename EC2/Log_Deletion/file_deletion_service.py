import os
import time
import sched

# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

def delete_file(file_path):
    """Delete the specified file."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        print(f"File {file_path} does not exist.")

def schedule_file_deletion(file_path, delay):
    """Schedule the file to be deleted after a delay."""
    scheduler.enter(delay, 1, delete_file, (file_path,))
    print(f"File {file_path} will be deleted in {delay / 3600} hours.")
    scheduler.run()

def main():
    # Specify the directory path
    directory_path = '/var/log/s3_logs'

    # Time delay in seconds (6 hours = 21600 seconds)
    delay = 6 * 3600

    # Iterate over files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Ensure we're working with a file
        if os.path.isfile(file_path):
            # Get the creation time of the file
            creation_time = os.path.getctime(file_path)
            current_time = time.time()
            time_since_creation = current_time - creation_time

            if time_since_creation < delay:
                remaining_time = delay - time_since_creation
                schedule_file_deletion(file_path, remaining_time)
            else:
                delete_file(file_path)

if __name__ == "__main__":
    main()

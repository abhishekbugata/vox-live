import time
import os

# The source is your original big log file
SOURCE_LOG = "enterprise_log_full_v3.log" 
# The destination is what the dashboard will watch
LIVE_LOG = "live_stream.log"

def start_spitting():
    if not os.path.exists(SOURCE_LOG):
        print(f"Error: {SOURCE_LOG} not found!")
        return

    # Clear previous live logs if they exist
    if os.path.exists(LIVE_LOG):
        os.remove(LIVE_LOG)

    print("Vox Spitter started. Feeding logs every 5 seconds...")
    
    with open(SOURCE_LOG, "r") as f:
        for line in f:
            with open(LIVE_LOG, "a") as live_f:
                live_f.write(line)
                print(f"Feeding: {line.strip()}")
            time.sleep(5)  # Wait 5 seconds between lines

if __name__ == "__main__":
    start_spitting()
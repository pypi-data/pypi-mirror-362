import os
import time
import schedule
from dotenv import load_dotenv
from alert_processor import AlertProcessor

def run_alerts():
    """
    Run the alert processor
    """
    config_path = os.getenv("ALERT_CONFIG_PATH", "config/alert_config.json")
    processor = AlertProcessor(config_path)
    processor.process_alerts()

def main():
    """
    Main function that sets up scheduling and runs the alert processor
    """
    load_dotenv()
    
    # Initial run
    run_alerts()
    
    # Schedule alert checks based on the minimum interval from config
    schedule.every(0.5).minutes.do(run_alerts)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
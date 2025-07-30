import json
import os
from typing import Dict, Any
from clickhouse_client import ClickhouseClient
from slack_client import SlackClient
from state_manager import StateManager
from config import Config
from datetime import datetime

class AlertProcessor:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.clickhouse_client = ClickhouseClient()
        
        # Get Slack config with environment variable substitution
        slack_config = self.config.slack.model_dump()
        if "${SLACK_BOT_TOKEN}" in slack_config["bot_token"]:
            slack_config["bot_token"] = os.getenv("SLACK_BOT_TOKEN")
            if not slack_config["bot_token"]:
                raise ValueError("SLACK_BOT_TOKEN environment variable is required but not set")
        
        self.slack_client = SlackClient(**slack_config)
        self.state_manager = StateManager()

    def _load_config(self, config_path: str) -> Config:
        """
        Load and validate configuration
        """
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return Config.model_validate(config_data)

    def process_alerts(self) -> None:
        """
        Process all configured alerts
        """
        for alert in self.config.alerts:
            self._process_single_alert(alert.model_dump())

    def _process_single_alert(self, alert_config: Dict[str, Any]) -> None:
        """
        Process a single alert configuration
        """
        # Get the last processed score timestamp for this alert
        last_processed_time = self.state_manager.get_last_processed_time(alert_config["name"])
        
        # If no last processed time, use lookback_minutes for initial run
        if last_processed_time is None:
            metrics = self.clickhouse_client.get_metrics(
                score_name=alert_config["score_name"],
                minutes=alert_config["lookback_minutes"]
            )
        else:
            metrics = self.clickhouse_client.get_metrics(
                score_name=alert_config["score_name"],
                start_time=last_processed_time
            )

        # Track the latest score timestamp we've seen
        latest_timestamp = None

        for metric in metrics:
            if self._should_alert(alert_config, metric["metric_value"]):
                # Enrich the metric data with alert config for context
                alert_data = {
                    "name": alert_config["name"],
                    "alert_name": alert_config["name"],
                    "score_name": alert_config["score_name"],
                    "condition": alert_config["condition"],
                    "threshold": alert_config["threshold"],
                    "trace_id": metric["trace_id"],
                    "metric_value": metric["metric_value"],
                    "timestamp": metric["timestamp"],  # This is the score timestamp
                    "metadata": metric.get("metadata", {}),
                    "id": metric.get("id", "N/A"),
                    "data_type": metric.get("data_type", "numeric"),
                    "project_id": metric.get("project_id", "N/A"),
                    "environment": metric.get("environment", "production")
                }
                self.slack_client.send_alert(alert_config, alert_data)

            # Update latest score timestamp seen
            score_timestamp = metric["timestamp"]
            if latest_timestamp is None or score_timestamp > latest_timestamp:
                latest_timestamp = score_timestamp

        # Update the last processed time if we processed any metrics
        if latest_timestamp is not None:
            self.state_manager.update_last_processed_time(alert_config["name"], latest_timestamp)

    def _should_alert(self, alert_config: Dict[str, Any], value: float) -> bool:
        """
        Check if an alert should be triggered based on the condition and threshold
        """
        if alert_config["condition"] == "below":
            return value < alert_config["threshold"]
        else:  # above
            return value > alert_config["threshold"] 
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Any
from datetime import datetime

class SlackClient:
    def __init__(self, channel: str, bot_token: str):
        self.channel = channel
        self.client = WebClient(token=bot_token)

    def send_alert(self, alert_config: Dict[str, Any], alert_data: Dict[str, Any]) -> None:
        """
        Send an alert to Slack with detailed score information
        """
        try:
            # Format timestamps
            def format_ts(ts):
                if isinstance(ts, str):
                    return ts
                return ts.strftime("%Y-%m-%d %H:%M:%S UTC") if ts else "N/A"

            # Create main message blocks (only alert header and trace link)
            main_blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"⚠️ Score Alert: {alert_data['name']}"
                    }
                }
            ]

            # Add trace link if configured
            if os.getenv("LANGFUSE_HOST"):
                trace_url = f"{os.getenv('LANGFUSE_HOST')}/trace/{alert_data['trace_id']}"
                main_blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{trace_url}|View Trace in Langfuse>"
                    }
                })

            # Send main message
            main_message = self.client.chat_postMessage(
                channel=self.channel,
                blocks=main_blocks,
                text=f"Alert: {alert_data['name']} score is {alert_data['metric_value']}"  # Fallback text
            )

            # Create thread blocks with detailed information
            thread_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Alert Details*\n"
                               f"• Alert Name: `{alert_data['alert_name']}`\n"
                               f"• Condition: `{alert_data['condition']} {alert_data['threshold']}`"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Score Information*\n"
                               f"• ID: `{alert_data['id']}`\n"
                               f"• Name: `{alert_data['name']}`\n"
                               f"• Value: `{alert_data['metric_value']:.3f}`\n"
                               f"• Data Type: `{alert_data['data_type']}`\n"
                               f"• String Value: `{alert_data.get('string_value', 'N/A')}`\n"
                               f"• Source: `{alert_data.get('source', 'N/A')}`\n"
                               f"• Comment: `{alert_data.get('comment', 'N/A')}`"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Context*\n"
                               f"• Project ID: `{alert_data['project_id']}`\n"
                               f"• Environment: `{alert_data['environment']}`\n"
                               f"• Trace ID: `{alert_data['trace_id']}`\n"
                               f"• Session ID: `{alert_data.get('session_id', 'N/A')}`\n"
                               f"• Dataset Run ID: `{alert_data.get('dataset_run_id', 'N/A')}`\n"
                               f"• Observation ID: `{alert_data.get('observation_id', 'N/A')}`"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Timestamps*\n"
                               f"• Created: {format_ts(alert_data.get('created_at'))}\n"
                               f"• Updated: {format_ts(alert_data.get('updated_at'))}\n"
                               f"• Event Time: {format_ts(alert_data.get('event_ts'))}\n"
                               f"• Score Time: {format_ts(alert_data['timestamp'])}"
                    }
                }
            ]

            # Add metadata section if present
            if alert_data.get("metadata"):
                metadata_text = "\n".join([
                    f"• {key}: `{value}`" 
                    for key, value in alert_data["metadata"].items()
                ])
                thread_blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Additional Metadata*\n{metadata_text}"
                    }
                })

            # Add author and config information
            thread_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*System Information*\n"
                           f"• Author User ID: `{alert_data.get('author_user_id', 'N/A')}`\n"
                           f"• Config ID: `{alert_data.get('config_id', 'N/A')}`\n"
                           f"• Queue ID: `{alert_data.get('queue_id', 'N/A')}`"
                }
            })

            # Add trace link in thread as well
            if os.getenv("LANGFUSE_HOST"):
                trace_url = f"{os.getenv('LANGFUSE_HOST')}/trace/{alert_data['trace_id']}"
                thread_blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{trace_url}|View Trace in Langfuse>"
                    }
                })

            # Send thread message with all details
            self.client.chat_postMessage(
                channel=self.channel,
                thread_ts=main_message['ts'],  # This creates a thread
                blocks=thread_blocks,
                text="Alert details"  # Fallback text
            )

        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}") 
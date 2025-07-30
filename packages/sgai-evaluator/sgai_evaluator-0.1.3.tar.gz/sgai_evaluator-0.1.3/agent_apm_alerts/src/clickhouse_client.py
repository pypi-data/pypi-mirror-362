from clickhouse_driver import Client
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
from urllib.parse import urlparse

class ClickhouseClient:
    def __init__(self):
        # Parse CLICKHOUSE_MIGRATION_URL to get host and port
        migration_url = os.getenv('CLICKHOUSE_MIGRATION_URL', '')
        parsed_url = urlparse(migration_url.replace('clickhouse://', 'http://'))
        
        # Extract host from the URL (remove any user:pass@)
        host = parsed_url.hostname or 'clickhouse'
        
        self.client = Client(
            host=host,
            port=9000,  # Using native protocol port from MIGRATION_URL
            database=os.getenv('CLICKHOUSE_DB', 'langfuse'),
            user=os.getenv('CLICKHOUSE_USER', 'langfuse'),
            password=os.getenv('CLICKHOUSE_PASSWORD', '')
        )

    def get_metrics(self, score_name: str, minutes: Optional[int] = None, start_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Query metrics from Clickhouse scores table for the specified score name and time range
        
        Args:
            score_name: Name of the score to query
            minutes: Optional lookback period in minutes (used if start_time is None)
            start_time: Optional specific start time to query from (exclusive)
        """
        if start_time is None and minutes is not None:
            start_time = datetime.utcnow() - timedelta(minutes=minutes)
        elif start_time is None:
            start_time = datetime.utcnow() - timedelta(minutes=1)  # Default 1 minutes lookback
        
        query = """
            SELECT 
                id,
                timestamp,
                project_id,
                environment,
                trace_id,
                session_id,
                dataset_run_id,
                observation_id,
                name,
                value as metric_value,
                source,
                comment,
                metadata,
                author_user_id,
                config_id,
                data_type,
                string_value,
                queue_id,
                created_at,
                updated_at,
                event_ts,
                is_deleted
            FROM scores
            WHERE timestamp > %(start_time)s  -- Using strictly greater than for score timestamp
            AND name = %(score_name)s
            AND value IS NOT NULL
            AND is_deleted = 0
            ORDER BY timestamp ASC  -- Process older events first
        """
        
        results = self.client.execute(
            query,
            {
                "start_time": start_time,
                "score_name": score_name
            },
            settings={'use_numpy': False}
        )
        
        return [
            {
                "id": row[0],
                "timestamp": row[1],  # Score timestamp used for filtering
                "project_id": row[2],
                "environment": row[3],
                "trace_id": row[4],
                "session_id": row[5],
                "dataset_run_id": row[6],
                "observation_id": row[7],
                "name": row[8],
                "metric_value": float(row[9]),
                "source": row[10],
                "comment": row[11],
                "metadata": row[12],
                "author_user_id": row[13],
                "config_id": row[14],
                "data_type": row[15],
                "string_value": row[16],
                "queue_id": row[17],
                "created_at": row[18],
                "updated_at": row[19],
                "event_ts": row[20],
                "is_deleted": bool(row[21])
            }
            for row in results
        ] 
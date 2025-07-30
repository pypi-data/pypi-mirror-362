#!/usr/bin/env python3
"""
Simplified Automated Evaluation Pipeline for Langfuse
===================================================

This script automatically evaluates new traces using LLM-as-a-judge.
Run it periodically to evaluate new traces as they arrive.
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from langfuse import Langfuse
import openai
from evaluation_config import EvaluationConfig, EVALUATION_PROMPTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangfuseEvaluator:
    """Simple evaluator for Langfuse traces."""
    
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.langfuse = Langfuse(
            public_key=config.langfuse_public_key,
            secret_key=config.langfuse_secret_key,
            host=config.langfuse_host
        )
        openai.api_key = config.openai_api_key
        
    def get_new_traces(self, minutes_back: int = 5) -> List[Any]:
        """Fetch traces from the last N minutes."""
        try:
            time_threshold = datetime.now() - timedelta(minutes=minutes_back)
            traces = self.langfuse.fetch_traces(
                from_timestamp=time_threshold,
                limit=50
            ).data
            
            logger.info(f"Found {len(traces)} traces in last {minutes_back} minutes")
            return traces
            
        except Exception as e:
            logger.error(f"Error fetching traces: {e}")
            return []
    
    def evaluate_with_llm(self, input_text: str, output_text: str, criteria: str) -> Optional[float]:
        """Evaluate using LLM-as-a-judge."""
        try:
            prompt = EVALUATION_PROMPTS[criteria].format(
                input=input_text,
                output=output_text
            )
            
            response = openai.ChatCompletion.create(
                model=self.config.evaluation_model,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator. Respond with only a number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=10
            )
            
            score = float(response.choices[0].message.content.strip())
            return score if 0.0 <= score <= 1.0 else None
            
        except Exception as e:
            logger.error(f"Evaluation error for {criteria}: {e}")
            return None
    
    def extract_trace_content(self, trace) -> tuple[Optional[str], Optional[str]]:
        """Extract input and output from trace."""
        try:
            input_text = None
            output_text = None
            
            # Try direct access
            if hasattr(trace, 'input') and trace.input:
                input_text = str(trace.input)
            if hasattr(trace, 'output') and trace.output:
                output_text = str(trace.output)
            
            # If not found, look in observations
            if not input_text or not output_text:
                observations = getattr(trace, 'observations', [])
                for obs in observations:
                    if not input_text and hasattr(obs, 'input') and obs.input:
                        input_text = str(obs.input)
                    if not output_text and hasattr(obs, 'output') and obs.output:
                        output_text = str(obs.output)
            
            return input_text, output_text
            
        except Exception as e:
            logger.error(f"Error extracting trace content: {e}")
            return None, None
    
    def evaluate_trace(self, trace) -> Dict[str, float]:
        """Evaluate a single trace."""
        results = {}
        
        # Extract content
        input_text, output_text = self.extract_trace_content(trace)
        
        if not input_text or not output_text:
            logger.warning(f"Missing content for trace {trace.id}")
            return results
        
        # Evaluate each criteria
        for criteria in self.config.evaluation_criteria:
            score = self.evaluate_with_llm(input_text, output_text, criteria)
            if score is not None:
                results[criteria] = score
                logger.info(f"Trace {trace.id} - {criteria}: {score:.2f}")
        
        return results
    
    def save_scores(self, trace_id: str, scores: Dict[str, float]) -> None:
        """Save evaluation scores to Langfuse."""
        try:
            for criteria, score in scores.items():
                self.langfuse.score(
                    trace_id=trace_id,
                    name=criteria,
                    value=score,
                    comment=f"Auto-evaluation via {self.config.evaluation_model}"
                )
            
            self.langfuse.flush()
            logger.info(f"Saved {len(scores)} scores for trace {trace_id}")
            
        except Exception as e:
            logger.error(f"Error saving scores for trace {trace_id}: {e}")
    
    def run_evaluation_cycle(self, minutes_back: int = 5) -> None:
        """Run one evaluation cycle."""
        logger.info("Starting evaluation cycle")
        
        traces = self.get_new_traces(minutes_back)
        evaluated_count = 0
        
        for trace in traces:
            try:
                scores = self.evaluate_trace(trace)
                if scores:
                    self.save_scores(trace.id, scores)
                    evaluated_count += 1
                    
                # Small delay to avoid rate limits
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error evaluating trace {trace.id}: {e}")
        
        logger.info(f"Evaluated {evaluated_count} traces")
    
    def run_continuous(self, interval_minutes: int = 5) -> None:
        """Run continuous evaluation."""
        logger.info(f"Starting continuous evaluation every {interval_minutes} minutes")
        
        while True:
            try:
                self.run_evaluation_cycle(interval_minutes)
                logger.info(f"Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("Stopping evaluation")
                break
            except Exception as e:
                logger.error(f"Error in continuous evaluation: {e}")
                time.sleep(60)

def main():
    """Main entry point."""
    # Load configuration
    config = EvaluationConfig.from_env()
    
    if not config.validate():
        logger.error("Invalid configuration")
        return
    
    # Initialize evaluator
    evaluator = LangfuseEvaluator(config)
    
    # Run evaluation
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        evaluator.run_continuous(config.evaluation_interval_minutes)
    else:
        evaluator.run_evaluation_cycle(config.time_window_minutes)

if __name__ == "__main__":
    main() 
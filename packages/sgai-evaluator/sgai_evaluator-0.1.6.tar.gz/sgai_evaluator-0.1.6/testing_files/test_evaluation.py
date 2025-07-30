#!/usr/bin/env python3
"""
Quick test to add evaluation scores to existing traces
"""

import os
from langfuse import Langfuse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse client (will use environment variables)
langfuse = Langfuse()

def add_evaluation_score():
    """Add a test evaluation score to demonstrate the scoring system."""
    try:
        # First, let's fetch recent traces to get the trace ID
        print("🔍 Fetching recent traces...")
        traces = langfuse.fetch_traces(limit=10).data
        
        if not traces:
            print("❌ No traces found. Please run some traced operations first.")
            return
        
        # Get the first trace
        trace = traces[0]
        trace_id = trace.id
        print(f"📊 Found trace: {trace.name} (ID: {trace_id})")
        
        # Add a custom evaluation score
        print("➕ Adding evaluation score...")
        score_result = langfuse.score(
            trace_id=trace_id,
            name="helpfulness",
            value=0.85,
            comment="This trace demonstrates good helpfulness"
        )
        print(f"✅ Score added: {score_result}")
        
        # Add another score for quality
        quality_score = langfuse.score(
            trace_id=trace_id,
            name="quality",
            value=0.9,
            comment="High quality response"
        )
        print(f"✅ Quality score added: {quality_score}")
        
        # Flush to ensure scores are sent
        langfuse.flush()
        print("📤 Scores flushed to Langfuse")
        
        print("\n🎉 Success! Check your Langfuse dashboard:")
        print("   1. Go to the Scores section")
        print("   2. You should see 2 new scores")
        print("   3. Click on your trace to see the scores attached")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your API keys are correct and Langfuse is accessible")

if __name__ == "__main__":
    print("🧪 Testing Langfuse Evaluation System...")
    print("=" * 50)
    add_evaluation_score() 
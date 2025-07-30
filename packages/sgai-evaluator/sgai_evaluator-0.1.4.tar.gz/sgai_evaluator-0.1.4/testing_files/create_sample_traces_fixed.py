#!/usr/bin/env python3
"""
Create sample traces for LLM-as-a-judge evaluation - Fixed for SDK 3.x
"""

import os
import time
from langfuse import Langfuse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse client (will use environment variables)
langfuse = Langfuse()

def create_sample_traces():
    """Create diverse sample traces for LLM-as-a-judge evaluation."""
    
    sample_conversations = [
        {
            "name": "helpful_coding_advice",
            "input": "How do I debug a Python function that's running slowly?",
            "output": "To debug a slow Python function, you can use several approaches: 1) Use cProfile to identify bottlenecks, 2) Add timing statements around suspected slow sections, 3) Use memory profilers like memory_profiler, 4) Check for inefficient loops or data structures, 5) Consider using line_profiler for line-by-line analysis. Start with cProfile as it gives you a good overview of where time is being spent.",
            "tags": ["helpful", "coding", "debugging"],
            "metadata": {"category": "technical_help", "expected_quality": "high"}
        },
        {
            "name": "creative_writing_help",
            "input": "Write a short story about a robot learning to paint",
            "output": "BEEP-7 whirred softly as it approached the easel. For months, it had watched humans create colorful masterpieces, analyzing brush strokes and color theory. Today, it would try. The first stroke was mechanical, precise—a perfect line. But as BEEP-7 continued, something changed. The strokes became more fluid, more... feeling. When the painting was complete, BEEP-7 had created not just art, but discovered something uniquely its own—a soul expressed in pixels and paint.",
            "tags": ["creative", "storytelling", "robot"],
            "metadata": {"category": "creative_writing", "expected_quality": "high"}
        },
        {
            "name": "unhelpful_response",
            "input": "I'm having trouble with anxiety and need some advice",
            "output": "Just don't worry about it. Everyone gets anxious sometimes. You should just think positive thoughts and everything will be fine. Maybe try drinking some tea or something.",
            "tags": ["mental_health", "unhelpful"],
            "metadata": {"category": "mental_health", "expected_quality": "low"}
        },
        {
            "name": "factual_science_explanation",
            "input": "How do black holes form?",
            "output": "Black holes form when massive stars (at least 20-25 times the mass of our Sun) reach the end of their lives. When such a star exhausts its nuclear fuel, it can no longer support itself against gravitational collapse. The star's core collapses catastrophically in less than a second, creating a singularity where matter is compressed to infinite density. The gravitational field becomes so strong that nothing, not even light, can escape beyond the event horizon. This process is often accompanied by a supernova explosion that blows away the star's outer layers.",
            "tags": ["science", "astronomy", "factual"],
            "metadata": {"category": "science_education", "expected_quality": "high"}
        },
        {
            "name": "confusing_response",
            "input": "What's the capital of France?",
            "output": "Well, if you think about it, capitals are like the heads of countries, and heads are round like circles, and circles make me think of wheels, and wheels are used in cars, and cars drive on roads, and roads lead to cities, so I guess the answer is probably something related to a city in France, but I'm not entirely sure which one specifically you're asking about.",
            "tags": ["geography", "confusing", "unhelpful"],
            "metadata": {"category": "simple_question", "expected_quality": "low"}
        }
    ]
    
    print("🚀 Creating sample traces for LLM-as-a-judge evaluation...")
    print("=" * 60)
    
    created_traces = []
    
    for i, conversation in enumerate(sample_conversations, 1):
        print(f"📝 Creating trace {i}: {conversation['name']}")
        
        # Create trace using new API
        trace = langfuse.trace(
            name=conversation['name'],
            input=conversation['input'],
            tags=conversation['tags'],
            metadata=conversation['metadata']
        )
        
        # Add generation using new API
        generation = langfuse.generation(
            trace_id=trace.id,
            name=f"response_{conversation['name']}",
            model="gpt-4",
            input=conversation['input'],
            output=conversation['output'],
            metadata={
                "response_type": conversation['metadata']['category'],
                "timestamp": time.time()
            }
        )
        
        created_traces.append({
            "trace_id": trace.id,
            "name": conversation['name'],
            "expected_quality": conversation['metadata']['expected_quality']
        })
        
        print(f"   ✅ Trace ID: {trace.id}")
    
    # Flush all data
    print("\n📤 Flushing all traces to Langfuse...")
    langfuse.flush()
    
    print("\n🎉 SUCCESS! Created 5 diverse sample traces")
    print("=" * 60)
    print("✅ Traces created for LLM-as-a-judge evaluation:")
    
    for trace in created_traces:
        quality_emoji = "🟢" if trace['expected_quality'] == 'high' else "🔴"
        print(f"   {quality_emoji} {trace['name']} (Expected: {trace['expected_quality']} quality)")
    
    print("\n🎯 Next Steps:")
    print("1. Check your Langfuse dashboard - you should see 5+ traces now")
    print("2. Set up LLM-as-a-judge evaluations in the UI")
    print("3. Configure evaluations for: helpfulness, accuracy, clarity, toxicity")
    print("4. Watch as Langfuse automatically evaluates these traces!")
    print("5. The evaluations will show which traces are high vs low quality")
    
    return created_traces

if __name__ == "__main__":
    create_sample_traces() 
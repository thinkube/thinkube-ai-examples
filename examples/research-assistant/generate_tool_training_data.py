#!/usr/bin/env python3
"""
Generate synthetic tool-use training data using gpt-oss-20b.

This script generates diverse examples across multiple domains to teach
a model WHEN and HOW to use tools, without overfitting to specific content.
"""

import os
import json
import random
from openai import OpenAI

# Connect to LiteLLM
client = OpenAI(
    base_url=os.environ.get('LITELLM_ENDPOINT', 'https://litellm.cmxela.com'),
    api_key=os.environ.get('LITELLM_MASTER_KEY', 'sk-test')
)

# Tool definitions (same as notebook 03)
TOOLS = [
    {
        "name": "search_papers",
        "description": "Search vector database for papers matching a semantic query",
        "parameters": {"query": "string - what to search for"}
    },
    {
        "name": "get_paper_details",
        "description": "Get full content of a specific paper by title",
        "parameters": {"paper_title_fragment": "string - part of the paper title"}
    },
    {
        "name": "log_to_mlflow",
        "description": "Log research findings to MLflow experiment",
        "parameters": {
            "experiment_name": "string - name of experiment",
            "run_name": "string - name of this run",
            "findings_summary": "string - summary to log"
        }
    }
]

# Diverse domains to prevent overfitting
DOMAINS = [
    "machine learning",
    "protein folding",
    "climate modeling",
    "quantum computing",
    "autonomous vehicles",
    "natural language processing",
    "computer vision",
    "drug discovery",
    "robotics",
    "renewable energy",
    "genomics",
    "materials science",
    "financial modeling",
    "epidemiology",
    "neural architecture search"
]

# Query templates for search_papers
SEARCH_TEMPLATES = [
    "Find papers about {topic}",
    "Search for research on {topic}",
    "What papers exist about {topic}?",
    "Look up papers related to {topic}",
    "I need papers on {topic}",
    "Can you find research about {topic}?",
    "Search the database for {topic}",
    "What's the latest research on {topic}?",
    "Find me papers discussing {topic}",
    "Look for papers that cover {topic}"
]

# Topics per domain (varied)
TOPICS = {
    "machine learning": ["transformer architectures", "attention mechanisms", "gradient descent optimization", "batch normalization", "dropout regularization"],
    "protein folding": ["alpha helix prediction", "protein-protein interactions", "molecular dynamics", "sequence alignment", "structure determination"],
    "climate modeling": ["carbon cycle simulation", "ocean temperature prediction", "atmospheric CO2 levels", "ice sheet dynamics", "weather pattern analysis"],
    "quantum computing": ["qubit error correction", "quantum entanglement", "superconducting circuits", "quantum algorithms", "decoherence mitigation"],
    "autonomous vehicles": ["lidar perception", "path planning algorithms", "sensor fusion", "pedestrian detection", "lane keeping systems"],
    "natural language processing": ["text summarization", "sentiment analysis", "named entity recognition", "machine translation", "question answering"],
    "computer vision": ["object detection", "image segmentation", "facial recognition", "pose estimation", "optical flow"],
    "drug discovery": ["molecular docking", "ADMET prediction", "virtual screening", "lead optimization", "pharmacokinetics modeling"],
    "robotics": ["motion planning", "grasp detection", "SLAM algorithms", "inverse kinematics", "reinforcement learning for control"],
    "renewable energy": ["solar cell efficiency", "wind turbine optimization", "energy storage systems", "grid integration", "photovoltaic materials"],
    "genomics": ["gene expression analysis", "variant calling", "CRISPR editing", "single-cell sequencing", "epigenetic modifications"],
    "materials science": ["crystal structure prediction", "polymer synthesis", "nanomaterial properties", "alloy design", "thin film deposition"],
    "financial modeling": ["risk assessment", "portfolio optimization", "market prediction", "credit scoring", "algorithmic trading"],
    "epidemiology": ["disease spread modeling", "vaccine effectiveness", "contact tracing", "mortality prediction", "outbreak detection"],
    "neural architecture search": ["search space design", "performance prediction", "multi-objective optimization", "hardware-aware NAS", "one-shot methods"]
}


def generate_search_example(domain, topic):
    """Generate a search_papers tool-use example."""
    template = random.choice(SEARCH_TEMPLATES)
    user_query = template.format(topic=f"{topic} in {domain}")
    
    prompt = f"""Generate a training example for a tool-using AI assistant.

User query: "{user_query}"

The assistant should:
1. Call the search_papers tool with an appropriate query
2. Receive results (generate 2-3 realistic but fictional paper titles/abstracts)
3. Summarize the findings naturally

Output ONLY valid JSON in this exact format:
{{
  "tool_call": {{"name": "search_papers", "arguments": {{"query": "your search query"}}}},
  "tool_result": "2-3 fictional papers with titles, authors, years, and brief descriptions",
  "assistant_response": "natural summary of what was found"
}}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.8
    )
    
    try:
        import re
        json_match = re.search(r'\{[\s\S]*\}', response.choices[0].message.content)
        if json_match:
            data = json.loads(json_match.group())
            data["user_query"] = user_query
            return data
    except:
        pass
    return None


def generate_details_example(domain, topic):
    """Generate a get_paper_details tool-use example."""
    fake_paper = f"{topic.title()}: A Comprehensive Study"
    user_query = f"Get me the details of the paper about {topic}"
    
    prompt = f"""Generate a training example for a tool-using AI assistant.

User query: "{user_query}"
Paper to look up: "{fake_paper}"

The assistant should:
1. Call get_paper_details tool with the paper title
2. Receive the paper content (generate realistic fictional abstract + key points)
3. Summarize the paper naturally

Output ONLY valid JSON:
{{
  "tool_call": {{"name": "get_paper_details", "arguments": {{"paper_title_fragment": "fragment to search"}}}},
  "tool_result": "Full paper details with title, authors, abstract, key findings",
  "assistant_response": "natural summary of the paper"
}}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.8
    )
    
    try:
        import re
        json_match = re.search(r'\{[\s\S]*\}', response.choices[0].message.content)
        if json_match:
            data = json.loads(json_match.group())
            data["user_query"] = user_query
            return data
    except:
        pass
    return None


def generate_mlflow_example(domain, topic):
    """Generate a log_to_mlflow tool-use example."""
    user_query = f"Log my analysis of {topic} research to MLflow"
    
    prompt = f"""Generate a training example for a tool-using AI assistant.

User query: "{user_query}"
Domain: {domain}

The assistant should:
1. Call log_to_mlflow tool with experiment_name, run_name, and findings_summary
2. Receive confirmation
3. Acknowledge the logging

Output ONLY valid JSON:
{{
  "tool_call": {{"name": "log_to_mlflow", "arguments": {{"experiment_name": "name", "run_name": "name", "findings_summary": "summary text"}}}},
  "tool_result": "Confirmation message from MLflow",
  "assistant_response": "natural acknowledgment"
}}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.8
    )
    
    try:
        import re
        json_match = re.search(r'\{[\s\S]*\}', response.choices[0].message.content)
        if json_match:
            data = json.loads(json_match.group())
            data["user_query"] = user_query
            return data
    except:
        pass
    return None


def convert_to_training_format(example):
    """Convert our format to OpenAI tool-use training format."""
    if not example:
        return None
        
    tool_call = example.get("tool_call", {})
    
    return {
        "messages": [
            {"role": "user", "content": example["user_query"]},
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": f"call_{random.randint(1000,9999)}",
                    "type": "function",
                    "function": {
                        "name": tool_call.get("name", ""),
                        "arguments": json.dumps(tool_call.get("arguments", {}))
                    }
                }]
            },
            {
                "role": "tool",
                "tool_call_id": f"call_{random.randint(1000,9999)}",
                "content": example.get("tool_result", "")
            },
            {"role": "assistant", "content": example.get("assistant_response", "")}
        ]
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="tool_training_data.jsonl")
    parser.add_argument("--count", type=int, default=500)
    args = parser.parse_args()
    
    print(f"Generating {args.count} tool-use training examples...")
    print(f"Output: {args.output}")
    
    examples = []
    generators = [
        (generate_search_example, 0.5),   # 50% search
        (generate_details_example, 0.3),  # 30% details
        (generate_mlflow_example, 0.2)    # 20% mlflow
    ]
    
    i = 0
    while len(examples) < args.count:
        domain = random.choice(DOMAINS)
        topic = random.choice(TOPICS[domain])
        
        # Pick generator based on weights
        r = random.random()
        if r < 0.5:
            gen = generate_search_example
        elif r < 0.8:
            gen = generate_details_example
        else:
            gen = generate_mlflow_example
        
        try:
            example = gen(domain, topic)
            if example:
                training_example = convert_to_training_format(example)
                if training_example:
                    examples.append(training_example)
                    print(f"[{len(examples)}/{args.count}] Generated {gen.__name__} for {domain}/{topic}")
        except Exception as e:
            print(f"Error: {e}")
        
        i += 1
        if i > args.count * 3:  # Safety limit
            print("Reached safety limit, stopping")
            break
    
    # Write to file
    with open(args.output, 'w') as f:
        for ex in examples:
            f.write(json.dumps(ex) + '\n')
    
    print(f"\n✓ Generated {len(examples)} examples")
    print(f"✓ Saved to {args.output}")


if __name__ == "__main__":
    main()

"""
Utility script to query and analyze the generated folder-structure JSON files.
Use this to search, filter, and extract information from the scanned documents.
"""

import json
import sys
from pathlib import Path

def load_structure(json_file):
    """Load the generated structure JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_files_with_field(data, field_name):
    """Find all files that have a specific extracted field."""
    results = []
    
    def traverse(node):
        if isinstance(node, dict):
            if 'file_list' in node:
                for file_obj in node['file_list']:
                    if 'extracted_fields' in file_obj and field_name in file_obj['extracted_fields']:
                        results.append(file_obj)
            for value in node.values():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    
    traverse(data)
    return results

def search_by_value(data, search_term):
    """Search for files containing a value (case-insensitive)."""
    results = []
    
    def traverse(node, path=""):
        if isinstance(node, dict):
            if 'file_list' in node:
                for file_obj in node['file_list']:
                    content = json.dumps(file_obj).lower()
                    if search_term.lower() in content:
                        results.append(file_obj)
            for key, value in node.items():
                traverse(value, f"{path}.{key}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                traverse(item, f"{path}[{i}]")
    
    traverse(data)
    return results

def find_similar_groups(data):
    """Group files by similarity relationships."""
    similarity_groups = {}
    
    def traverse(node):
        if isinstance(node, dict):
            if 'file_list' in node:
                for file_obj in node['file_list']:
                    if 'similar_documents' in file_obj:
                        file_name = file_obj['name']
                        similarity_groups[file_name] = file_obj['similar_documents']
            for value in node.values():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    
    traverse(data)
    return similarity_groups

def extract_all_fields(data, field_name):
    """Extract all values for a specific field across all files."""
    values = []
    
    def traverse(node):
        if isinstance(node, dict):
            if 'file_list' in node:
                for file_obj in node['file_list']:
                    if 'extracted_fields' in file_obj:
                        if field_name in file_obj['extracted_fields']:
                            values.append({
                                'file': file_obj['name'],
                                'value': file_obj['extracted_fields'][field_name]['value'],
                                'confidence': file_obj['extracted_fields'][field_name]['confidence']
                            })
            for value in node.values():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    
    traverse(data)
    return values

def print_summary(json_file):
    """Print a summary of the structure file."""
    data = load_structure(json_file)
    
    file_count = 0
    summary_count = 0
    extraction_count = 0
    similarity_count = 0
    
    def traverse(node):
        nonlocal file_count, summary_count, extraction_count, similarity_count
        if isinstance(node, dict):
            if 'file_list' in node:
                for file_obj in node['file_list']:
                    file_count += 1
                    if 'ai_summary' in file_obj:
                        summary_count += 1
                    if 'extracted_fields' in file_obj:
                        extraction_count += 1
                    if 'similar_documents' in file_obj:
                        similarity_count += 1
            for value in node.values():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    
    traverse(data)
    
    print(f"\n{'='*60}")
    print(f"Folder Scan Summary: {json_file}")
    print(f"{'='*60}")
    print(f"Generated: {data.get('generated_at')}")
    print(f"GUID: {data.get('guid')}")
    print(f"\nStatistics:")
    print(f"  Total Files: {file_count}")
    print(f"  Files with AI Summaries: {summary_count}")
    print(f"  Files with Extracted Fields: {extraction_count}")
    print(f"  Files with Similarity Matches: {similarity_count}")
    print(f"\nModels Used:")
    print(f"  AI Summaries: {data.get('ollama_generative_model', 'N/A')}")
    print(f"  Embeddings: {data.get('ollama_embedding_model', 'N/A')}")
    print(f"{'='*60}\n")

# Example usage
if __name__ == "__main__":
    # Example: python query_output.py "structure.json"
    
    json_file = "structure.json"  # Change to your output file
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    
    # Check if file exists
    if not Path(json_file).exists():
        print(f"Error: File '{json_file}' not found")
        sys.exit(1)
    
    data = load_structure(json_file)
    
    # Print summary
    print_summary(json_file)
    
    # Example queries
    print("\n📊 EXAMPLE QUERIES:\n")
    
    # 1. Find all files with pricing information
    print("1. Files with PRICING information:")
    pricing_files = find_files_with_field(data, 'pricing')
    for f in pricing_files[:3]:  # Show first 3
        print(f"   - {f['name']}: {f['extracted_fields']['pricing']['value'][:80]}...")
    
    # 2. Find all parties mentioned
    print("\n2. All PARTIES mentioned in documents:")
    parties = extract_all_fields(data, 'parties')
    for p in parties[:3]:  # Show first 3
        print(f"   - {p['file']}: {p['value'][:80]}...")
    
    # 3. Find similar document groups
    print("\n3. Document SIMILARITY GROUPS:")
    similarity_groups = find_similar_groups(data)
    for doc_name, similar_docs in list(similarity_groups.items())[:3]:  # Show first 3
        print(f"   - {doc_name}:")
        for sim_doc in similar_docs[:2]:
            print(f"     → {sim_doc['name']} (similarity: {sim_doc['similarity']})")
    
    # 4. Search for specific term
    print("\n4. Search results for 'invoice':")
    results = search_by_value(data, 'invoice')
    print(f"   Found in {len(results)} file(s)")
    if results:
        print(f"   - {results[0]['name']}")
    
    print("\n" + "="*60)
    print("\n💡 TIP: Use this script to:")
    print("   - Search for specific documents or values")
    print("   - Find duplicate or similar documents")
    print("   - Extract specific fields across all documents")
    print("   - Generate reports from the scanned data")
    print("   - Analyze document relationships")
    print("\n")

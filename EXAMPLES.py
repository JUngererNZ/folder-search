#!/usr/bin/env python3
"""
Quick Start Example - Enhanced Folder Search
Shows practical examples of how to use the system
"""

def example_1_basic_scan():
    """Example 1: Run a basic folder scan"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Folder Scan")
    print("=" * 60)
    
    print("""
This is the simplest way to use the system:

    python folder_search.py

When prompted:
    1. Enter folder path: C:\\Your\\Documents
    2. Generate AI summaries? y
    3. Use embeddings? y

Output: Documents-structure.json with all analysis
    """)

def example_2_find_pricing():
    """Example 2: Find all pricing information"""
    print("=" * 60)
    print("EXAMPLE 2: Extract All Pricing Information")
    print("=" * 60)
    
    print("""
from query_output import load_structure, find_files_with_field
import json

# Load the results
data = load_structure("Documents-structure.json")

# Find all files with pricing
pricing_files = find_files_with_field(data, 'pricing')

# Display results
for file_obj in pricing_files:
    price_info = file_obj['extracted_fields']['pricing']
    print(f"{file_obj['name']}: {price_info['value']}")
    print(f"  Confidence: {price_info['confidence']}")
    """)

def example_3_find_duplicates():
    """Example 3: Find and eliminate duplicate documents"""
    print("=" * 60)
    print("EXAMPLE 3: Find Duplicate Documents")
    print("=" * 60)
    
    print("""
from query_output import load_structure, find_similar_groups

# Load results
data = load_structure("Documents-structure.json")

# Find similarity groups
similar = find_similar_groups(data)

# Display groups
for main_doc, similar_docs in similar.items():
    if similar_docs:  # Has similar documents
        print(f"\\n{main_doc} is similar to:")
        for sim_doc in similar_docs:
            print(f"  - {sim_doc['name']} (similarity: {sim_doc['similarity']})")
    """)

def example_4_search():
    """Example 4: Search for specific content"""
    print("=" * 60)
    print("EXAMPLE 4: Search for Specific Content")
    print("=" * 60)
    
    print("""
from query_output import load_structure, search_by_value

# Load results
data = load_structure("Documents-structure.json")

# Search for term
results = search_by_value(data, "FML Freight")

# Display results
print(f"Found '{term}' in {len(results)} file(s):")
for result in results:
    print(f"  - {result['name']}")
    """)

def example_5_export_to_csv():
    """Example 5: Export extracted data to CSV"""
    print("=" * 60)
    print("EXAMPLE 5: Export to CSV for Excel")
    print("=" * 60)
    
    print("""
from query_output import load_structure, extract_all_fields
import csv

# Load results
data = load_structure("Documents-structure.json")

# Extract all pricing
pricing_data = extract_all_fields(data, 'pricing')

# Export to CSV
with open('pricing_report.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['file', 'value', 'confidence'])
    writer.writeheader()
    writer.writerows(pricing_data)

print("Exported to pricing_report.csv")
    """)

def example_6_custom_analysis():
    """Example 6: Custom analysis workflow"""
    print("=" * 60)
    print("EXAMPLE 6: Custom Analysis Workflow")
    print("=" * 60)
    
    print("""
from query_output import load_structure
import json

# Load results
data = load_structure("Documents-structure.json")

# Analyze
total_files = 0
files_with_summaries = 0
files_with_pricing = 0

for item in data.get('file_list', []):
    total_files += 1
    if 'ai_summary' in item:
        files_with_summaries += 1
    if 'extracted_fields' in item and 'pricing' in item['extracted_fields']:
        files_with_pricing += 1

# Report
print(f"Total files analyzed: {total_files}")
print(f"Files with summaries: {files_with_summaries}")
print(f"Files with pricing: {files_with_pricing}")
    """)

def example_7_integration():
    """Example 7: Database integration"""
    print("=" * 60)
    print("EXAMPLE 7: Save to Database")
    print("=" * 60)
    
    print("""
from query_output import load_structure
import sqlite3

# Load results
data = load_structure("Documents-structure.json")

# Create database
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE documents (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        document_type TEXT,
        pricing TEXT,
        parties TEXT,
        dates TEXT
    )
''')

# Insert data
for file_obj in data.get('file_list', []):
    fields = file_obj.get('extracted_fields', {})
    pricing = fields.get('pricing', {}).get('value', '')
    parties = fields.get('parties', {}).get('value', '')
    dates = fields.get('dates', {}).get('value', '')
    
    cursor.execute('''
        INSERT INTO documents (filename, document_type, pricing, parties, dates)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_obj['name'], file_obj['extension'], pricing, parties, dates))

conn.commit()
conn.close()
print("Data saved to documents.db")
    """)

def main():
    """Run all examples"""
    examples = [
        example_1_basic_scan,
        example_2_find_pricing,
        example_3_find_duplicates,
        example_4_search,
        example_5_export_to_csv,
        example_6_custom_analysis,
        example_7_integration,
    ]
    
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "ENHANCED FOLDER SEARCH - EXAMPLES" + " " * 11 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    for example_func in examples:
        example_func()
        print()
    
    print("=" * 60)
    print("For more information, see README.md or ENHANCED_FEATURES.md")
    print("=" * 60)

if __name__ == "__main__":
    main()

# 🚀 Enhanced Folder Search - Complete Documentation

## Overview

This project contains an **AI-powered document scanning and analysis system** that:
- 📄 Extracts and analyzes document content from PDF, DOCX, XLSX, TXT, and MD files
- 🧠 Generates intelligent structured summaries using AI (llama3)
- 🔍 Automatically extracts key fields (pricing, parties, dates, scope, terms)
- 🔗 Detects document similarities and relationships
- 📊 Outputs all findings as organized JSON for further processing

## 🎯 Quick Start

### Prerequisites
```bash
# Install Ollama: https://ollama.ai
# Pull required models:
ollama pull llama3:latest
ollama pull mxbai-embed-large:latest

# Start Ollama service:
ollama serve
```

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python folder_search.py

# Follow prompts:
# 1. Enter folder path
# 2. Enable AI summaries? (y/n)
# 3. Enable embeddings/field extraction? (y/n)
```

## 📁 Project Structure

```
folder-search/
├── folder_search.py              # Main scanning script
├── query_output.py               # Query and analyze results
├── requirements.txt              # Python dependencies
├── ENHANCED_FEATURES.md          # Feature documentation
├── IMPLEMENTATION_SUMMARY.md     # Technical details
└── README.md                     # This file
```

## 🔧 Core Features

### 1. Document Text Extraction
- **PDF**: Full text extraction using pypdf
- **DOCX**: Paragraph-by-paragraph extraction
- **XLSX**: Cell-level content extraction
- **TXT/MD**: Direct file reading with UTF-8 support

### 2. Intelligent Field Extraction
Automatically identifies and extracts:

| Field | Examples |
|-------|----------|
| **Pricing** | "$1,500", "USD 5000", "charges" |
| **Parties** | "Company XYZ", "Vendor ABC", "Client Name" |
| **Dates** | "2026-02-28", "valid until", "delivery date" |
| **Scope** | "shipment contents", "services", "items" |
| **Terms** | "payment terms", "policy", "requirements" |

**Each extraction includes confidence score (0-1)**

### 3. AI-Generated Summaries
Creates structured JSON with:
- Document title and type
- 2-3 key information points
- Involved parties
- Main purpose
- Recommended next steps

### 4. Document Similarity Analysis
- Compares documents using semantic embeddings
- Identifies duplicates and related documents
- Returns similarity scores (0-1)
- Helps identify patterns and relationships

### 5. Comprehensive Metadata
- File information (size, type, path)
- Generation timestamp and unique GUID
- Model information used
- Processing status

## 📊 Output Format

### Basic File Object
```json
{
  "name": "estimate.pdf",
  "path": "C:\\Documents\\estimate.pdf",
  "extension": ".pdf",
  "size_bytes": 50000,
  "size_human": "48.83 KB",
  "extracted_fields": {
    "pricing": {
      "value": "Total: $1,500.00",
      "confidence": 0.85
    },
    "parties": {
      "value": "FML Freight Solutions",
      "confidence": 0.85
    },
    "dates": {
      "value": "Valid until: 2026-02-28",
      "confidence": 0.85
    },
    "scope": {
      "value": "Freight services from JNB to CPT",
      "confidence": 0.85
    },
    "terms": {
      "value": "Payment within 30 days",
      "confidence": 0.85
    }
  },
  "ai_summary": {
    "title": "Freight Estimate",
    "type": "Logistics Document",
    "key_info": [
      "Cost estimation for cargo transport",
      "Route: Johannesburg to Cape Town",
      "Valid for 60 days"
    ],
    "parties": [
      {"name": "FML Freight Solutions", "role": "Provider"},
      {"name": "Customer ABC", "role": "Client"}
    ],
    "purpose": "To provide pricing for freight services",
    "next_steps": [
      {"action": "Review estimate details"},
      {"action": "Confirm booking if acceptable"},
      {"action": "Process payment upon confirmation"}
    ]
  },
  "similar_documents": [
    {
      "name": "estimate_2025_001.pdf",
      "similarity": 0.92,
      "path": "C:\\Documents\\Archive\\estimate_2025_001.pdf"
    },
    {
      "name": "quote_2025_002.pdf",
      "similarity": 0.88,
      "path": "C:\\Documents\\Archive\\quote_2025_002.pdf"
    }
  ]
}
```

### Root Structure
```json
{
  "folder_name": {
    "subfolder": {...},
    "file_list": [...],
    "generated_at": "2026-01-29T13:00:55.847963",
    "guid": "65462308",
    "ai_summaries_enabled": true,
    "embeddings_enabled": true,
    "ollama_generative_model": "llama3:latest",
    "ollama_embedding_model": "mxbai-embed-large:latest",
    "last_modified": "2026-01-29T11:48:20.950021"
  }
}
```

## 🔍 Analyzing Results

### Using the Query Script
```bash
python query_output.py "C:\path\to\structure.json"
```

### Example Queries

**Find all pricing information:**
```python
from query_output import load_structure, find_files_with_field
data = load_structure("structure.json")
pricing_files = find_files_with_field(data, 'pricing')
```

**Search for specific term:**
```python
from query_output import search_by_value
results = search_by_value(data, 'invoice')
```

**Find document groups:**
```python
from query_output import find_similar_groups
groups = find_similar_groups(data)
```

## ⚙️ Configuration

### Models Configuration
Edit `folder_search.py` to change models:
```python
OLLAMA_GENERATIVE_MODEL = 'llama3:latest'      # For summaries
OLLAMA_EMBEDDING_MODEL = 'mxbai-embed-large:latest'  # For embeddings
```

### Custom Field Extraction
Add or modify extraction queries:
```python
EXTRACTION_QUERIES = {
    'your_field': ['keyword1', 'keyword2', 'keyword3'],
}
```

### Adjust Thresholds
```python
# Document similarity threshold (0-1):
if similarity > 0.75:  # Increase for stricter matching

# File size limit for summaries:
text_to_summarize = text[:2000]  # Increase/decrease as needed

# Request timeout:
timeout=120  # Seconds
```

## 📈 Performance Tips

1. **First Run**: Slower (models loading) - subsequent runs faster
2. **Large Files**: Automatically truncated to 2000 chars for summaries
3. **Many Files**: Process in batches to avoid memory issues
4. **Timeouts**: Increase timeout for slower hardware: `timeout=300`
5. **Memory**: Embeddings are cached - don't worry about repeated usage

## 🐛 Troubleshooting

### Error: "Could not connect to Ollama"
```bash
# Make sure Ollama is running:
ollama serve

# Check if Ollama is accessible:
curl http://localhost:11434/api/tags
```

### Error: "Read timed out"
- Normal for large or complex documents
- Try: `timeout=180` in the script
- Or use faster model: `mistral:latest`

### Error: "Model not found"
```bash
# Pull the model:
ollama pull llama3:latest
ollama pull mxbai-embed-large:latest

# List available models:
ollama list
```

### No summaries generated
- Check if file is readable (try opening manually)
- Try increasing timeout
- Check available memory

## 🔐 Data Privacy

- All processing happens **locally** on your machine
- No data is sent to external servers
- All Ollama models run offline
- Output JSON files can be encrypted or moved as needed

## 📝 Supported File Types

| Type | Extensions | Status | Notes |
|------|-----------|--------|-------|
| PDF | .pdf | ✅ Full Support | Text extraction from all pages |
| Word | .docx | ✅ Full Support | Paragraph extraction |
| Excel | .xlsx | ✅ Full Support | Cell content from all sheets |
| Text | .txt | ✅ Full Support | Direct file reading |
| Markdown | .md | ✅ Full Support | Formatting preserved |

## 🚀 Advanced Usage

### Batch Processing Multiple Folders
```python
import os
from folder_search import get_folder_structure

folders = [
    "C:\\Documents\\2025",
    "C:\\Documents\\2024",
    "C:\\Documents\\Archive"
]

for folder in folders:
    structure, embeddings = get_folder_structure(folder, generate_summaries=True, use_embeddings=True)
    # Process results...
```

### Custom Analysis
```python
from query_output import load_structure, extract_all_fields

data = load_structure("structure.json")

# Extract all pricing information
pricing_data = extract_all_fields(data, 'pricing')

# Generate report
for item in pricing_data:
    print(f"{item['file']}: {item['value']} (confidence: {item['confidence']})")
```

### Database Integration
```python
import json
import sqlite3

data = load_structure("structure.json")

# Insert into database
conn = sqlite3.connect('documents.db')
for file_obj in data.get('file_list', []):
    # Extract and insert relevant fields
    pass
```

## 📊 Use Cases

1. **Legal Document Analysis** - Extract parties, dates, terms automatically
2. **Invoice Processing** - Identify amounts, vendors, dates
3. **Duplicate Detection** - Find and consolidate similar documents
4. **Data Organization** - Categorize documents by content
5. **Compliance Reporting** - Extract relevant fields for audit
6. **Knowledge Management** - Index and search document content
7. **Contract Management** - Extract key terms and dates

## 🤝 Integration Examples

### With Pandas
```python
import pandas as pd
from query_output import load_structure, extract_all_fields

data = load_structure("structure.json")
pricing = extract_all_fields(data, 'pricing')
df = pd.DataFrame(pricing)
df.to_csv('pricing_report.csv', index=False)
```

### With Elasticsearch
```python
from elasticsearch import Elasticsearch
es = Elasticsearch()

data = load_structure("structure.json")
for file_obj in traverse_files(data):
    es.index(index="documents", body=file_obj)
```

## 📚 Model Information

### llama3:latest
- **Purpose**: Text generation and summarization
- **Size**: ~8GB
- **Speed**: Medium
- **Quality**: Excellent
- **Alternatives**: mistral (faster), neural-chat (medium)

### mxbai-embed-large:latest
- **Purpose**: Semantic embeddings for similarity
- **Size**: ~2GB
- **Speed**: Fast
- **Quality**: Good for similarity detection
- **Alternatives**: nomic-embed-text, all-minilm

## 📖 Resources

- [Ollama Documentation](https://ollama.ai)
- [Available Models](https://ollama.ai/library)
- [pypdf Documentation](https://pypdf.readthedocs.io)
- [python-docx Documentation](https://python-docx.readthedocs.io)

## 📄 License

This project uses open-source models and libraries. See individual dependencies for their licenses.

## 🎉 Features Summary

✅ Multi-format document extraction
✅ AI-powered intelligent summarization
✅ Semantic field extraction
✅ Document similarity detection
✅ Comprehensive metadata tracking
✅ JSON output for easy integration
✅ Offline privacy-first processing
✅ Customizable extraction rules
✅ Batch processing capability
✅ Graceful error handling

---

**Version**: 2.0 (Enhanced with Embeddings & Similarity Detection)
**Last Updated**: January 29, 2026
**Status**: Production Ready ✅

For questions or issues, refer to IMPLEMENTATION_SUMMARY.md or ENHANCED_FEATURES.md

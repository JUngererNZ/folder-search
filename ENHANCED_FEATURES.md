# Enhanced Folder Search Script - Feature Documentation

## Overview
The enhanced `folder_search.py` script uses Ollama's local AI models to:
1. **Generate AI Summaries** - Create structured JSON summaries of documents
2. **Extract Structured Data** - Automatically identify pricing, parties, dates, scope, and terms
3. **Find Similar Documents** - Identify duplicate or related documents using semantic similarity
4. **Semantic Search** - Powered by embeddings for intelligent content analysis

## Features

### 1. AI-Powered Summaries
- Uses `llama3:latest` to generate comprehensive document summaries
- Structures output as JSON with: title, type, key_info, parties, purpose, next_steps
- Extracts key sections automatically for faster processing
- Supports: PDF, DOCX, XLSX, TXT, MD files

**Output Example:**
```json
{
  "ai_summary": {
    "title": "Invoice",
    "type": "Billing Notification",
    "key_info": [{"amount": "$50.00"}],
    "parties": [{"name": "Company XYZ"}],
    "purpose": "Payment request",
    "next_steps": [{"action": "Process payment"}]
  }
}
```

### 2. Intelligent Field Extraction
- Uses `mxbai-embed-large:latest` embeddings to extract specific fields
- Automatically identifies and extracts:
  - **Pricing** - Costs, fees, rates, amounts
  - **Parties** - Companies, contacts, vendors
  - **Dates** - Deadlines, validity periods, delivery dates
  - **Scope** - Services, descriptions, shipment details
  - **Terms** - Payment terms, policies, requirements

**Output Example:**
```json
{
  "extracted_fields": {
    "pricing": {
      "value": "Total charge: $1,500.00",
      "confidence": 0.85
    },
    "parties": {
      "value": "Vendor: Acme Corp",
      "confidence": 0.85
    },
    "dates": {
      "value": "Valid until: 2026-02-28",
      "confidence": 0.85
    }
  }
}
```

### 3. Document Similarity Detection
- Uses semantic embeddings to find related documents
- Identifies duplicate or similar documents automatically
- Returns top 5 similar documents with similarity scores (0-1)

**Output Example:**
```json
{
  "similar_documents": [
    {
      "name": "invoice_2025_001.pdf",
      "similarity": 0.92,
      "path": "..."
    },
    {
      "name": "invoice_2025_002.pdf",
      "similarity": 0.88,
      "path": "..."
    }
  ]
}
```

### 4. Metadata & Organization
- File size in both bytes and human-readable format
- Unique GUID for each scan
- Timestamp of generation and last modification
- Model information for reproducibility

## Installation

### Prerequisites
```bash
# 1. Install Ollama from https://ollama.ai

# 2. Pull required models
ollama pull llama3:latest
ollama pull mxbai-embed-large:latest

# 3. Start Ollama service
ollama serve
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

```bash
python folder_search.py
```

**Prompts:**
1. Enter starting folder path
2. Generate AI summaries? (y/n) - Creates text summaries using llama3
3. Use embeddings? (y/n) - Enables field extraction and document similarity

**Example Session:**
```
Enter the starting folder path: C:\MyDocuments
Generate AI summaries? (y/n, default: n): y
Use embeddings for field extraction & similarity? (y/n, default: n): y
✓ Ollama is running with 3 model(s)
Using generative model: llama3:latest
Using embedding model: mxbai-embed-large:latest
Scanning folder structure...
✓ JSON output saved to C:\MyDocuments\MyDocuments-structure.json
```

## Output JSON Structure

```json
{
  "folder_name": {
    "file_list": [
      {
        "name": "document.pdf",
        "path": "...",
        "extension": ".pdf",
        "size_bytes": 50000,
        "size_human": "48.83 KB",
        "extracted_fields": {
          "pricing": {...},
          "parties": {...},
          "dates": {...}
        },
        "ai_summary": {
          "title": "...",
          "type": "...",
          ...
        },
        "similar_documents": [
          {
            "name": "...",
            "similarity": 0.92,
            "path": "..."
          }
        ]
      }
    ],
    "generated_at": "2026-01-29T12:00:00.000000",
    "guid": "abc12345",
    "ai_summaries_enabled": true,
    "embeddings_enabled": true,
    "ollama_generative_model": "llama3:latest",
    "ollama_embedding_model": "mxbai-embed-large:latest"
  }
}
```

## Performance Notes

- **First Run**: Slower due to model loading
- **Subsequent Runs**: Faster (models cached in memory)
- **Large Files**: Automatically truncates to first 2000 characters for summaries
- **Timeouts**: If models are busy, requests may timeout - this is normal

## Customization

### Change Models
Edit the script to use different models:
```python
OLLAMA_GENERATIVE_MODEL = 'mistral:latest'  # Faster alternative
OLLAMA_EMBEDDING_MODEL = 'mxbai-embed-large:latest'
```

### Change Field Extraction Categories
Edit `EXTRACTION_QUERIES` dictionary to add custom fields:
```python
EXTRACTION_QUERIES = {
    'custom_field': ['keyword1', 'keyword2'],
    ...
}
```

## Troubleshooting

**Error: "Could not connect to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check if running at correct URL: `http://localhost:11434`

**Error: "Read timed out"**
- Models are processing - this is normal for large files
- Reduce file size or use faster models like `mistral`

**No summaries generated**
- Embeddings may be enabled but slow - disable if not needed
- Check if models are fully loaded

## Model Recommendations

| Model | Use Case | Speed | Memory |
|-------|----------|-------|--------|
| llama3:latest | Summaries (default) | Medium | 8GB |
| mistral:latest | Summaries (faster) | Fast | 4GB |
| mxbai-embed-large | Embeddings (default) | Fast | 2GB |
| qwen2.5-coder | Code/technical docs | Medium | 8GB |

## Future Enhancements

- [ ] Add query/search interface for generated JSON
- [ ] Add document clustering
- [ ] Add export to CSV/Excel
- [ ] Add batch processing with progress tracking
- [ ] Add custom extraction templates per industry

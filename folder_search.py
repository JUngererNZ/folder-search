import os
import json
import datetime
import uuid
import subprocess
import requests
from pathlib import Path

# Document extraction libraries
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.md'}
OLLAMA_MODEL = 'llama2'  # Change to your preferred model
OLLAMA_URL = 'http://localhost:11434'

def extract_text_from_file(file_path):
    """Extract text content from various document types."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    try:
        if ext == '.txt' or ext == '.md':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif ext == '.pdf' and pypdf:
            text = ""
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        
        elif ext == '.docx' and Document:
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        
        elif ext == '.xlsx' and openpyxl:
            workbook = openpyxl.load_workbook(file_path)
            text = ""
            for sheet in workbook.sheetnames:
                ws = workbook[sheet]
                text += f"\n--- Sheet: {sheet} ---\n"
                for row in ws.iter_rows(values_only=True):
                    text += '\t'.join([str(cell) if cell is not None else "" for cell in row]) + "\n"
            return text
        
        else:
            return None
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def generate_summary_with_ollama(text, file_name):
    """Generate detailed AI summary using local Ollama."""
    if not text or len(text.strip()) < 100:
        return None
    
    # Truncate text if too long (limit to ~4000 chars to avoid timeout)
    text = text[:4000]
    
    prompt = f"""Analyze the following document ({file_name}) and provide a comprehensive structured summary. 
    
If it's a freight/logistics document, structure it with: meta, service_provider, client, scope_of_work, charges, inclusions, exclusions, operational_conditions, documentation_requirements, payment_and_terms.

If it's another type of document, provide: overview, key_sections, main_points, important_details, action_items (if applicable).

Document content:
{text}

Provide the summary as a JSON structure with appropriate sections for this document type. Be detailed and comprehensive."""

    try:
        response = requests.post(
            f'{OLLAMA_URL}/api/generate',
            json={'model': OLLAMA_MODEL, 'prompt': prompt, 'stream': False},
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        summary_text = result.get('response', '')
        
        # Try to parse as JSON, otherwise return as text
        try:
            return json.loads(summary_text)
        except json.JSONDecodeError:
            return {"raw_summary": summary_text}
    
    except requests.exceptions.ConnectionError:
        print(f"Warning: Could not connect to Ollama at {OLLAMA_URL}. Make sure Ollama is running.")
        return None
    except Exception as e:
        print(f"Error generating summary with Ollama: {e}")
        return None

def get_file_info(file_path, generate_ai_summary=True):
    """Get detailed file information including AI summary."""
    try:
        stat_info = os.stat(file_path)
        file_size_bytes = stat_info.st_size
        file_size_human = format_file_size(file_size_bytes)
        
        _, ext = os.path.splitext(file_path)
        
        file_info = {
            "name": os.path.basename(file_path),
            "path": file_path,
            "extension": ext.lower(),
            "size_bytes": file_size_bytes,
            "size_human": file_size_human
        }
        
        # Generate AI summary if enabled and file type is supported
        if generate_ai_summary and ext.lower() in SUPPORTED_EXTENSIONS:
            text_content = extract_text_from_file(file_path)
            if text_content:
                summary = generate_summary_with_ollama(text_content, os.path.basename(file_path))
                if summary:
                    file_info["ai_summary"] = summary
        
        return file_info
    
    except Exception as e:
        print(f"Error getting file info for {file_path}: {e}")
        return None

def format_file_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def get_folder_structure(root_dir, max_depth=6, generate_summaries=True):
    def _walk(dir_path, depth):
        if depth > max_depth:
            return None
        structure = {}
        files_list = []
        try:
            entries = os.listdir(dir_path)
        except PermissionError:
            return None
        for entry in entries:
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                sub = _walk(full_path, depth + 1)
                if sub is not None:
                    structure[entry] = sub
            else:
                file_info = get_file_info(full_path, generate_ai_summary=generate_summaries)
                if file_info:
                    files_list.append(file_info)
        if files_list:
            structure['file_list'] = files_list
        return structure
    return _walk(root_dir, 0)

if __name__ == "__main__":
    start_folder = input("Enter the starting folder path: ")
    if not os.path.isdir(start_folder):
        print("Invalid directory")
        exit()
    
    generate_ai = input("Generate AI summaries? (y/n, default: n): ").lower().strip() == 'y'
    
    if generate_ai:
        print("Checking Ollama connection...")
        try:
            response = requests.get(f'{OLLAMA_URL}/api/tags', timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    print(f"✓ Ollama is running with {len(models)} model(s)")
                    print(f"Using model: {OLLAMA_MODEL}")
                else:
                    print(f"⚠ Ollama is running but no models found. Please pull a model first.")
                    print(f"Run: ollama pull {OLLAMA_MODEL}")
                    generate_ai = False
            else:
                print("⚠ Ollama connection failed")
                generate_ai = False
        except Exception as e:
            print(f"⚠ Could not connect to Ollama: {e}")
            print(f"Make sure Ollama is running at {OLLAMA_URL}")
            generate_ai = False
    
    print("\nScanning folder structure...")
    structure = get_folder_structure(start_folder, 4, generate_summaries=generate_ai)
    
    folder_name = os.path.basename(start_folder)
    output_file = os.path.join(start_folder, f"{folder_name}-structure.json")
    
    last_modified = None
    if os.path.exists(output_file):
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(output_file)).isoformat()
    
    generated_at = datetime.datetime.now().isoformat()
    short_guid = str(uuid.uuid4())[:8]
    
    structure['generated_at'] = generated_at
    structure['guid'] = short_guid
    structure['ai_summaries_enabled'] = generate_ai
    
    if last_modified:
        structure['last_modified'] = last_modified
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print(f"✓ JSON output saved to {output_file}")
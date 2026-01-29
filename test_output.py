import json

data = json.load(open('C:/Users/Jason/OneDrive - FML Freight Solutions/VAL-DE-VIE/VAL-DE-VIE-structure.json'))
files = [f for f in data.get('file_list', []) if 'extracted_fields' in f]
print(f'Files with extracted fields: {len(files)}')
print('\nMetadata:')
print(f'Generated: {data.get("generated_at")}')
print(f'GUID: {data.get("guid")}')
print(f'AI Summaries: {data.get("ai_summaries_enabled")}')
print(f'Embeddings: {data.get("embeddings_enabled")}')
print(f'Generative Model: {data.get("ollama_generative_model")}')
print(f'Embedding Model: {data.get("ollama_embedding_model")}')

print('\n\nSample extracted fields from first file:')
if files:
    print(json.dumps(files[0]['extracted_fields'], indent=2))

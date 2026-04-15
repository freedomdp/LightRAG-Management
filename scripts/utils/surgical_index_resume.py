import urllib.request
import json
import os
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:9621/documents/text"
STATUS_FILE = "rag_storage/kv_store_doc_status.json"

def get_pending_files():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE, 'r') as f:
        data = json.load(f)
    return {k: v.get('file_path') for k, v in data.items() if v.get('status') == 'pending'}

def ingest_file(filepath):
    logger.info(f"Surgical Ingest: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        payload = {
            "text": content,
            "file_source": filepath
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=1200) as response:
            res_data = json.loads(response.read().decode())
            status = res_data.get("status")
            logger.info(f"Response for {filepath}: {status}")
            return True
    except Exception as e:
        logger.error(f"Error ingesting {filepath}: {e}")
        return False

def main():
    target_files = [
        "docs/knowledge/ai_factory_1.8_manifesto.md",
        "docs/knowledge/browseract_encyclopedia_youtube_ru.md",
        "docs/knowledge/browseract_integration_n8n_ru.md",
        "docs/knowledge/business_value_ai_agents.md",
        "docs/knowledge/hlv_architecture_expert_guide.md",
        "docs/knowledge/hlv_sdd_core_expert_system.md",
        "docs/knowledge/human_in_the_loop_patterns.md",
        "docs/knowledge/money_framework_roberts.md",
        "docs/knowledge/omnichannel_identity_resolution.md",
        "docs/knowledge/seo_training/ai_hallucinations_and_guardrails.md",
        "docs/knowledge/seo_training/seo_workflow_and_task_boundaries.md",
        "docs/knowledge/seo_training/technical_seo_checklist_2026.md",
        "docs/knowledge/seo_training/wp_seo_no_plugins_code.md"
    ]

    logger.info(f"Starting surgical indexing for {len(target_files)} target files...")
    
    for filepath in target_files:
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            continue
            
        success = ingest_file(filepath)
        if success:
            logger.info(f"Successfully sent {filepath}. Waiting 30s for stable indexing...")
            time.sleep(30)
        else:
            logger.error(f"Failed to send {filepath}. Moving to next.")

if __name__ == "__main__":
    main()

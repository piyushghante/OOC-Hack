from typing import Any, Dict, List, Tuple
from transformers import PreTrainedTokenizerBase
from model_manager import generate_text
from bs4 import BeautifulSoup

def summarize_rfp(model: Any, tokenizer: PreTrainedTokenizerBase, rfp_chunks: List[str]) -> str:
    chunk_summaries = []
    for chunk in rfp_chunks:
        prompt = f"""Summarize the following section of a Request for Proposal (RFP):

{chunk}

Summary:"""
        summary = generate_text(model, tokenizer, prompt, max_length=250, temperature=0.3)
        chunk_summaries.append(summary)
    
    if len(chunk_summaries) > 1:
        combined = "\n\n".join(chunk_summaries)
        meta_prompt = f"""Below are summaries of RFP sections. Create a concise overall summary (300-500 words):

{combined}

Overall Summary:"""
        return generate_text(model, tokenizer, meta_prompt, max_length=600, temperature=0.3)
    elif chunk_summaries:
        return chunk_summaries[0]
    else:
        return "No RFP content provided."

def extract_eligibility_criteria(model: Any, tokenizer: PreTrainedTokenizerBase, rfp_chunks: List[str]) -> List[Dict[str, str]]:
    all_criteria = []
    for chunk in rfp_chunks:
        prompt = f"""Extract key eligibility requirements from the following RFP section. For each, provide:
1. Description
2. Importance (Critical, Important, Nice-to-have)

RFP Section:
{chunk}

Eligibility Criteria:"""
        text = generate_text(model, tokenizer, prompt, max_length=600, temperature=0.3)
        all_criteria.extend(parse_criteria_text(text))
    return deduplicate_criteria(all_criteria)

def parse_criteria_text(text: str) -> List[Dict[str, str]]:
    lines = text.split('\n')
    results = []
    current = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit() and '. ' in line:
            if current: results.append(current)
            parts = line.split(' - ', 1)
            desc = parts[0][line.find('.')+1:].strip()
            importance = parts[1].strip() if len(parts) > 1 else extract_importance(desc)
            current = {"description": desc, "importance": importance}
        elif line.startswith('- ') or line.startswith('• '):
            if current: results.append(current)
            parts = line[2:].split(' - ', 1)
            desc = parts[0].strip()
            importance = parts[1].strip() if len(parts) > 1 else extract_importance(desc)
            current = {"description": desc, "importance": importance}
        elif current:
            current["description"] += " " + line
    if current: results.append(current)
    for r in results:
        r["importance"] = normalize_importance(r["importance"])
    return results

def extract_importance(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["must", "required", "mandatory", "critical"]): return "Critical"
    if any(k in text for k in ["important", "should"]): return "Important"
    if any(k in text for k in ["nice", "prefer", "optional"]): return "Nice-to-have"
    return "Important"

def normalize_importance(imp: str) -> str:
    imp = imp.lower()
    if any(k in imp for k in ["critical", "required", "must", "mandatory"]): return "Critical"
    if any(k in imp for k in ["important", "should"]): return "Important"
    if any(k in imp for k in ["nice", "prefer", "optional"]): return "Nice-to-have"
    return "Important"

def deduplicate_criteria(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = []
    unique = []
    for item in items:
        desc = item["description"].lower()
        if any(similarity(desc, s) > 0.7 for s in seen): continue
        seen.append(desc)
        unique.append(item)
    return unique

def similarity(a: str, b: str) -> float:
    w1, w2 = set(a.split()), set(b.split())
    return len(w1 & w2) / max(len(w1), len(w2))

def evaluate_company_eligibility(model: Any, tokenizer: PreTrainedTokenizerBase, criteria: List[Dict[str, str]], company_chunks: List[str]) -> str:
    criteria_text = "\n".join(f"{i+1}. {c['description']} - {c['importance']}" for i, c in enumerate(criteria))
    company_text = "\n\n".join(company_chunks)
    prompt = f"""Evaluate if the company meets these RFP criteria. Be extremely strict.

Mark:
- FULLY MEETS: Only if clear, explicit evidence exists
- DOES NOT MEET: If evidence is missing, unclear, partial, or not stated

Eligibility Criteria:
{criteria_text}

Company Profile:
{company_text}

Evaluation (each criterion individually):"""
    return generate_text(model, tokenizer, prompt, max_length=1024, temperature=0.3)

def determine_verdict(model: Any, tokenizer: PreTrainedTokenizerBase, criteria: List[Dict[str, str]], evaluation: str) -> Dict[str, str]:
    eval_lower = evaluation.lower()
    critical_fails = sum(1 for line in eval_lower.split('\n') if "critical" in line and "does not meet" in line)
    important_fails = sum(1 for line in eval_lower.split('\n') if "important" in line and "does not meet" in line)
    fully_met = sum(1 for line in eval_lower.split('\n') if "fully meets" in line)
    
    if critical_fails > 0:
        return {
            "decision": "NOT ELIGIBLE",
            "reasoning": "Company fails to meet one or more critical criteria, which are mandatory."
        }
    elif important_fails > 0:
        return {
            "decision": "NOT ELIGIBLE",
            "reasoning": "Company fails to meet important eligibility requirements. All must be clearly satisfied."
        }
    elif fully_met < len(criteria):
        return {
            "decision": "NOT ELIGIBLE",
            "reasoning": "Company does not fully meet all eligibility criteria with clear, explicit evidence."
        }
    else:
        return {
            "decision": "ELIGIBLE",
            "reasoning": "Company fully satisfies all eligibility requirements with clear evidence."
        }

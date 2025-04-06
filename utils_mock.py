from typing import Dict, List

def get_app_info() -> str:
    """
    Get information about the application.
    
    Returns:
        str: Formatted application information string
    """
    return """
    RFP Analyzer v0.1.0
    Mode: Local (Privacy-preserving)
    Status: Mock version active
    """

def format_eligibility_criteria(criteria: List[Dict[str, str]]) -> str:
    """
    Format the eligibility criteria into a readable HTML string.
    
    Args:
        criteria: List of criteria with descriptions and importance
        
    Returns:
        str: HTML-formatted criteria
    """
    if not criteria:
        return "<p>No criteria extracted</p>"
    
    html = '<div class="criteria-list">'
    
    for criterion in criteria:
        importance = criterion.get("importance", "Important")
        description = criterion.get("description", "")
        
        # Set color based on importance
        if importance == "Critical":
            color = "red"
        elif importance == "Important":
            color = "orange"
        else:  # Nice-to-have
            color = "blue"
        
        html += f"""
        <div class="criterion">
            <p><strong style="color: {color};">{importance}:</strong> {description}</p>
        </div>
        """
    
    html += '</div>'
    return html

def format_verdict(verdict: Dict[str, str]) -> str:
    """
    Format the eligibility verdict into a highlighted HTML string.
    
    Args:
        verdict: Dictionary with decision and reasoning
        
    Returns:
        str: HTML-formatted verdict
    """
    if not verdict:
        return "<p>No verdict available</p>"
    
    decision = verdict.get("decision", "UNCLEAR")
    reasoning = verdict.get("reasoning", "")
    
    # Set color based on decision
    if decision == "ELIGIBLE":
        color = "green"
        emoji = "✅"
    elif decision == "NOT ELIGIBLE":
        color = "red"
        emoji = "❌"
    else:
        color = "orange"
        emoji = "⚠️"
    
    html = f"""
    <div class="verdict">
        <h3 style="color: {color};">{emoji} {decision}</h3>
        <div class="reasoning">
            <p>{reasoning}</p>
        </div>
    </div>
    """
    
    return html
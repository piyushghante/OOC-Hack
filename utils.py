import re
from typing import Any, Dict, List

def get_app_info() -> str:
    """
    Get information about the application.
    
    Returns:
        str: Formatted application information string
    """
    # Format the info string
    info = """
RFP Analyzer Application
------------------------
Version: 1.0.0
Mode: Demo (Using mock data)
Privacy: All processing done locally
    """
    
    return info

def format_eligibility_criteria(criteria: List[Dict[str, str]]) -> str:
    """
    Format the eligibility criteria into a readable HTML string.
    
    Args:
        criteria: List of criteria with descriptions and importance
        
    Returns:
        str: HTML-formatted criteria
    """
    if not criteria:
        return "No eligibility criteria were identified."
    
    html = '<div class="criteria-list" style="margin: 20px 0;">'
    
    for criterion in criteria:
        importance = criterion["importance"]
        description = criterion["description"]
        
        # Determine color and style based on importance
        if importance == "Critical":
            color = "#721c24"  # Red for critical
            bg_color = "#f8d7da"
        elif importance == "Important":
            color = "#004085"  # Blue for important
            bg_color = "#cce5ff"
        else:  # "Nice-to-have"
            color = "#0c5460"  # Teal for nice-to-have
            bg_color = "#d1ecf1"
        
        html += f'''
        <div style="padding: 10px; margin-bottom: 10px; background-color: {bg_color}; border-radius: 4px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>{description}</span>
                <span style="color: {color}; font-weight: bold; margin-left: 10px;">({importance})</span>
            </div>
        </div>'''
    
    html += "</div>"
    
    return html

def format_verdict(verdict: Dict[str, str]) -> str:
    """
    Format the eligibility verdict into a highlighted HTML string.
    
    Args:
        verdict: Dictionary with decision and reasoning
        
    Returns:
        str: HTML-formatted verdict
    """
    decision = verdict["decision"]
    reasoning = verdict["reasoning"]
    
    # Determine color based on decision
    if decision == "ELIGIBLE":
        color = "#155724"  # Green for eligible
        bg_color = "#d4edda"
    elif decision == "NOT ELIGIBLE":
        color = "#721c24"  # Red for not eligible
        bg_color = "#f8d7da"
    else:
        color = "#856404"  # Yellow for unclear
        bg_color = "#fff3cd"
    
    html = f"""
    <div style="padding: 15px; background-color: {bg_color}; border-radius: 5px; margin: 15px 0;">
        <h3 style="color: {color}; text-align: center; font-size: 1.5em; margin-bottom: 15px;">
            {decision}
        </h3>
        <p>{reasoning}</p>
    </div>
    """
    
    return html

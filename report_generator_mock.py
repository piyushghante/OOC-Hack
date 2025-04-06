from typing import Dict, List

def generate_report(
    summary: str,
    criteria: List[Dict[str, str]],
    evaluation: str,
    verdict: Dict[str, str]
) -> str:
    """
    Generate an HTML report summarizing the RFP analysis.
    
    Args:
        summary: RFP summary
        criteria: List of eligibility criteria
        evaluation: Company evaluation against criteria
        verdict: Final verdict with decision and reasoning
        
    Returns:
        str: HTML report
    """
    # Format the criteria for HTML
    criteria_html = ""
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
        
        criteria_html += f"""
        <tr>
            <td style="color: {color}; font-weight: bold;">{importance}</td>
            <td>{description}</td>
        </tr>
        """
    
    # Get verdict info
    decision = verdict.get("decision", "UNCLEAR")
    reasoning = verdict.get("reasoning", "")
    
    # Set color based on decision
    if decision == "ELIGIBLE":
        verdict_color = "green"
        verdict_icon = "✅"
    elif decision == "NOT ELIGIBLE":
        verdict_color = "red"
        verdict_icon = "❌"
    else:
        verdict_color = "orange"
        verdict_icon = "⚠️"
    
    # Create the HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RFP Eligibility Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                border: 1px solid #ddd;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #2c3e50;
                margin-top: 30px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            .verdict {{
                margin: 30px 0;
                padding: 15px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .conclusion {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
                color: {verdict_color};
            }}
            footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>RFP Eligibility Analysis Report</h1>
            
            <h2>RFP Summary</h2>
            <p>{summary}</p>
            
            <h2>Eligibility Criteria</h2>
            <table>
                <thead>
                    <tr>
                        <th>Importance</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {criteria_html}
                </tbody>
            </table>
            
            <h2>Company Evaluation</h2>
            <p>{evaluation}</p>
            
            <h2>Final Verdict</h2>
            <div class="verdict">
                <div class="conclusion">{verdict_icon} {decision}</div>
                <p>{reasoning}</p>
            </div>
            
            <footer>
                <p>Generated with RFP Eligibility Analyzer - A privacy-preserving tool for evaluating RFP eligibility</p>
                <p>All analysis was performed locally on your device. No data was sent to external servers.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html
from typing import Dict, List
import datetime

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
    # Determine verdict class for styling
    verdict_class = ""
    if verdict["decision"] == "ELIGIBLE":
        verdict_class = "eligible"
    elif verdict["decision"] == "NOT ELIGIBLE":
        verdict_class = "not-eligible"
    else:
        verdict_class = "unclear"
    
    # Format criteria into HTML
    criteria_html = ""
    for i, criterion in enumerate(criteria):
        importance_class = criterion["importance"].lower().replace("-", "")
        criteria_html += f"""
        <div class="criterion {importance_class}">
            <span class="number">{i+1}</span>
            <div class="content">
                <p>{criterion["description"]}</p>
                <span class="badge {importance_class}">{criterion["importance"]}</span>
            </div>
        </div>
        """
    
    # Current date/time for the report
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build the HTML report
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RFP Eligibility Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .verdict {{
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
            text-align: center;
        }}
        .eligible {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }}
        .not-eligible {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }}
        .unclear {{
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
        }}
        .decision {{
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .criterion {{
            display: flex;
            margin-bottom: 15px;
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .number {{
            background-color: #3498db;
            color: white;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
        }}
        .content {{
            flex-grow: 1;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            font-size: 0.8em;
            border-radius: 3px;
            margin-top: 5px;
        }}
        .critical {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .important {{
            background-color: #cce5ff;
            color: #004085;
        }}
        .nicetohave {{
            background-color: #d1ecf1;
            color: #0c5460;
        }}
        pre {{
            white-space: pre-wrap;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
    </style>
</head>
<body>
    <header>
        <h1>RFP Eligibility Analysis Report</h1>
        <p class="timestamp">Generated on: {now}</p>
    </header>

    <div class="section">
        <h2>RFP Summary</h2>
        <p>{summary}</p>
    </div>

    <div class="section">
        <h2>Eligibility Criteria</h2>
        <p>The following criteria were extracted from the RFP document:</p>
        <div class="criteria-list">
            {criteria_html}
        </div>
    </div>

    <div class="section">
        <h2>Company Evaluation</h2>
        <pre>{evaluation}</pre>
    </div>

    <div class="verdict {verdict_class}">
        <div class="decision">{verdict["decision"]}</div>
        <p>{verdict["reasoning"]}</p>
    </div>

    <footer>
        <p><strong>Note:</strong> This analysis was performed using a local language model. While efforts have been made to ensure accuracy, manual verification of the results is recommended.</p>
    </footer>
</body>
</html>
"""
    
    return html

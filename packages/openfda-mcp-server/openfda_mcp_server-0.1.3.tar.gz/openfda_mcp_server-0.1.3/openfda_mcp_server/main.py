"""Main MCP server for drug safety and recall analysis using openFDA APIs."""

from collections import Counter
from mcp.server.fastmcp import FastMCP
from mcp_server_demo.openfda_client import OpenFDAClient


mcp = FastMCP("drug-safety")
client = OpenFDAClient()


@mcp.tool("search_drug_events", description="Search adverse events for a drug")
def search_drug_events(drug: str = "aspirin", limit: int = 5):
    results = client.search(f'patient.drug.medicinalproduct:"{drug}"', limit=limit)

    summary = []
    for i, r in enumerate(results):
        reactions = [rx.get("reactionmeddrapt", "") for rx in r.get("patient", {}).get("reaction", [])]
        summary.append(f"{i+1}. Reported on {r.get('receivedate')} — Reactions: {', '.join(reactions)}")

    return {"summary": f"Showing {len(results)} recent adverse event reports for {drug}", "events": summary}


@mcp.tool("common_reactions", description="Get most common reactions for a drug")
def common_reactions(drug: str = "aspirin", limit: int = 20):
    results = client.search(f'patient.drug.medicinalproduct:"{drug}"', limit=limit)

    all_reactions = []
    for r in results:
        reactions = r.get("patient", {}).get("reaction", [])
        all_reactions.extend([rx.get("reactionmeddrapt", "") for rx in reactions])

    counter = Counter(all_reactions)
    top_reactions = counter.most_common(5)
    summary = [f"{i+1}. {name} ({count} reports)" for i, (name, count) in enumerate(top_reactions)]

    return {"summary": f"Top reported reactions for {drug}", "top_reactions": summary}


@mcp.tool("recall_alerts", description="Check if a drug has been recalled")
def recall_alerts(drug: str = "aspirin", limit: int = 5):
    """Fetch recent recalls for a specific drug using the FDA API."""
    results = client.search(f'product_description:"{drug}"', category="drug", endpoint="enforcement", limit=limit)

    if not results:
        return {"summary": f"No recent recalls found for {drug}."}

    summary = []
    for r in results:
        summary.append(f"- {r['recall_number']}: {r['reason_for_recall']} (Initiated: {r['recall_initiation_date']})")

    return {"summary": f"Recent recalls related to {drug}", "recalls": summary}


@mcp.tool("event_timeline", description="Count drug adverse events by year")
def event_timeline(drug: str = "aspirin", limit: int = 100):
    results = client.search(f'patient.drug.medicinalproduct:"{drug}"', limit=limit)

    years = [r.get("receivedate", "")[:4] for r in results if "receivedate" in r]
    year_count = Counter(years)

    summary = [f"{year}: {count} reports" for year, count in sorted(year_count.items())]
    return {"summary": f"Event counts by year for {drug}", "timeline": summary}


@mcp.tool("serious_event_breakdown", description="Breakdown of serious vs non-serious adverse events")
def serious_event_breakdown(drug: str = "aspirin", limit: int = 50):
    results = client.search(f'patient.drug.medicinalproduct:"{drug}"', limit=limit)
    serious = sum(1 for r in results if r.get("serious", "0") == "1")
    non_serious = len(results) - serious

    return {
        "summary": f"Adverse event seriousness breakdown for {drug}",
        "serious": serious,
        "non_serious": non_serious,
    }


@mcp.tool("drug_label_info", description="Get drug labeling details from FDA")
def drug_label_info(drug: str = "metformin", limit: int = 1):
    """Fetch drug label information from the FDA API."""
    if not drug:
        return {"summary": "No drug name provided."}

    results = client.search(f'openfda.generic_name:"{drug}"', category="drug", endpoint="label", limit=limit)

    if not results:
        return {"summary": f"No label info found for {drug}"}

    label = results[0]
    return {
        "summary": f"Label summary for {drug}",
        "indications": label.get("indications_and_usage", ["N/A"])[0],
        "dosage": label.get("dosage_and_administration", ["N/A"])[0],
        "warnings": label.get("warnings", ["None provided"])[0],
    }


@mcp.prompt("prompt:risk-evaluation-prompt", description="Guide for evaluating a drug's safety profile")
def risk_evaluation_prompt():
    return {
        "template": """
Evaluate the risk level for the drug **{{ drug }}** based on the following:

- Number of adverse events reported
- Presence of serious reactions
- Any recall notices
- Warnings from FDA label

Return a short paragraph summarizing safety, followed by a numerical risk rating (Low, Moderate, High).
        """,
        "inputs": ["drug"],
    }


@mcp.prompt("prompt:drug-safety-evaluation", description="Summarize overall safety profile of a drug")
def safety_eval_prompt():
    return {
        "template": """
Analyze the safety profile of **{{ drug }}** using:

- Adverse events summary
- Recalls (if any)
- Label warnings

Conclude with:  
- A risk level (Low/Moderate/High)  
- Short explanation  
""",
        "inputs": ["drug"],
    }


@mcp.prompt("prompt:recall-impact-assessment", description="Help assess the significance of a drug recall")
def recall_impact_prompt():
    return {
        "template": """
Given the recall report for **{{ brand_name }}**, evaluate:

- Severity level (Class I, II, III)
- Number of affected lots or units
- Manufacturer involved
- Dates and distribution scope

Summarize the impact in 2–3 bullet points.
""",
        "inputs": ["brand_name"],
    }


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")

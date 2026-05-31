import httpx
from typing import List, Dict, Any

async def web_search(query: str) -> List[Dict[str, Any]]:
    """
    Simplified web search using Google's Programmable Search or fallback to mock
    In production, integrate with a real search API
    """
    # For MVP, we'll use a mock search that returns sample results
    # In production, replace with actual search API (Google Custom Search, Bing, etc.)
    
    credible_domains = [
        "monitor.co.ug", "ntv.co.ug", "ugandaradionetwork.com",
        "ubos.org", "health.go.ug", "afro.who.int", "upf.go.ug"
    ]
    
    # Mock search results - in production, this would be real API calls
    mock_results = []
    for domain in credible_domains[:2]:
        mock_results.append({
            "url": f"https://{domain}/search?q={query.replace(' ', '+')}",
            "title": f"Relevant information about {query[:50]}",
            "snippet": f"According to official sources, this claim has been verified..."
        })
    
    return mock_results
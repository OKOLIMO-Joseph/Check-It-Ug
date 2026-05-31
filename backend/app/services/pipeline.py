import google.generativeai as genai
from app.config import settings
from app.models.claim import Verdict, Lang, VerdictResponse
from app.services.search import web_search
import json
from typing import Dict, Any

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class FactCheckPipeline:
    def __init__(self):
        # Use Gemini 1.5 Flash for cost-effectiveness
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def extract_claim(self, raw_text: str) -> Dict[str, str]:
        """Step 1: Extract core claim from raw message"""
        prompt = f"""Extract the core factual claim from this message. Return ONLY valid JSON:
{{
    "claim": "extracted claim here",
    "claim_type": "health|political|economic|event|other"
}}

Message: {raw_text}"""
        
        response = self.model.generate_content(prompt)
        # Clean response (remove markdown if present)
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned)
    
    async def verify_claim(self, claim: str) -> Dict[str, Any]:
        """Step 2+3: Search and verify claim"""
        
        # Perform web search
        search_results = await web_search(claim)
        
        # Format search results for Gemini
        sources_text = "\n".join([f"- {r['url']}: {r['snippet']}" for r in search_results])
        
        prompt = f"""Fact-check this claim against credible Ugandan sources. Return ONLY valid JSON:
{{
    "verdict": "true|false|misleading|unverifiable",
    "confidence": 0.85,
    "reasoning": "One paragraph summary of findings",
    "sources": ["url1", "url2"]
}}

Claim: {claim}

Relevant sources from credible Ugandan media and official sources:
{sources_text}

Priority sources: Daily Monitor, NTV Uganda, Uganda Radio Network, UBOS, Ministry of Health, WHO Uganda"""
        
        response = self.model.generate_content(prompt)
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned)
    
    async def format_explanation(self, verdict_data: Dict[str, Any], lang: Lang) -> str:
        """Step 4: Format explanation in target language"""
        language_map = {
            Lang.en: "English",
            Lang.lg: "Luganda",
            Lang.nyn: "Runyankole"
        }
        
        prompt = f"""Write a 2-sentence plain-language explanation of this fact-check result for a Ugandan audience with primary school education. Use {language_map[lang]} language.

Verdict: {verdict_data['verdict']}
Confidence: {verdict_data['confidence']}
Reasoning: {verdict_data['reasoning']}

Return ONLY valid JSON: {{"explanation": "your explanation here"}}"""
        
        response = self.model.generate_content(prompt)
        cleaned = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned)['explanation']
    
    async def run_pipeline(self, text: str, lang: Lang) -> VerdictResponse:
        """Run complete fact-checking pipeline"""
        
        # Step 1: Extract claim
        claim_data = await self.extract_claim(text)
        claim_normalised = claim_data['claim']
        
        # Step 2-3: Verify claim with search
        verification = await self.verify_claim(claim_normalised)
        
        # Step 4: Format explanation in target language
        explanation = await self.format_explanation(verification, lang)
        
        return VerdictResponse(
            verdict=Verdict(verification['verdict']),
            confidence=verification['confidence'],
            explanation=explanation,
            sources=verification.get('sources', []),
            claim_normalised=claim_normalised,
            lang=lang,
            cached=False
        )

pipeline = FactCheckPipeline()
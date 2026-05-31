const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ClaimRequest {
  text: string;
  lang: string;
  source: string;
}

export interface VerdictResponse {
  verdict: string;
  confidence: number;
  explanation: string;
  sources: string[];
  claim_normalised: string;
  lang: string;
  cached: boolean;
}

export async function checkClaim(req: ClaimRequest): Promise<VerdictResponse> {
  const response = await fetch(`${API_URL}/api/v1/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req)
  });
  
  if (!response.ok) {
    throw new Error('Failed to check claim');
  }
  
  return response.json();
}

export async function getTrends(days: number = 7, token: string) {
  const response = await fetch(`${API_URL}/api/v1/trends?days=${days}&token=${token}`);
  return response.json();
}
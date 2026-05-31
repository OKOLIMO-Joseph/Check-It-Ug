interface VerdictCardProps {
  result: {
    verdict: string;
    confidence: number;
    explanation: string;
    sources: string[];
    claim_normalised: string;
  };
}

export default function VerdictCard({ result }: VerdictCardProps) {
  const getVerdictConfig = () => {
    const configs = {
      true: { color: 'bg-green-100 border-green-500', icon: '✅', label: 'TRUE' },
      false: { color: 'bg-red-100 border-red-500', icon: '❌', label: 'FALSE' },
      misleading: { color: 'bg-amber-100 border-amber-500', icon: '⚠️', label: 'MISLEADING' },
      unverifiable: { color: 'bg-gray-100 border-gray-500', icon: '❓', label: 'UNVERIFIABLE' }
    };
    return configs[result.verdict as keyof typeof configs] || configs.unverifiable;
  };

  const getConfidenceLabel = () => {
    if (result.confidence >= 0.8) return 'High confidence';
    if (result.confidence >= 0.5) return 'Medium confidence';
    return 'Low confidence';
  };

  const config = getVerdictConfig();

  return (
    <div className={`max-w-2xl mx-auto mt-6 p-6 rounded-lg border-l-8 ${config.color} bg-white shadow-md`}>
      <div className="flex items-center gap-3 mb-4">
        <span className="text-3xl">{config.icon}</span>
        <h2 className="text-2xl font-bold">{config.label}</h2>
        <span className="ml-auto text-sm text-gray-600">{getConfidenceLabel()}</span>
      </div>
      
      <p className="text-gray-800 mb-4 leading-relaxed">{result.explanation}</p>
      
      <div className="text-sm text-gray-600 mb-3">
        <span className="font-medium">Claim understood as:</span> {result.claim_normalised}
      </div>
      
      {result.sources.length > 0 && (
        <div className="mt-4 pt-3 border-t border-gray-200">
          <h3 className="text-sm font-semibold mb-2">Sources:</h3>
          <ul className="space-y-1">
            {result.sources.map((source, idx) => (
              <li key={idx}>
                <a href={source} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm break-all">
                  {source}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
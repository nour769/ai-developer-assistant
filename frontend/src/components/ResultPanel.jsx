export default function ResultPanel({ loading, error, result, feature }) {
  if (loading) {
    return (
      <div className="loading-row">
        <span className="loading-dot" />
        <span className="loading-dot" />
        <span className="loading-dot" />
        <span>{loadingLabel(feature)}</span>
      </div>
    );
  }

  if (error) {
    return <div className="error-banner">{error}</div>;
  }

  if (!result) {
    return (
      <div className="empty-state">
        <div className="icon">◍</div>
        Importe un projet, puis pose une question ou choisis une action
        à gauche pour explorer le code.
      </div>
    );
  }

  return <div className="result-card">{result}</div>;
}

function loadingLabel(feature) {
  const labels = {
    explain: "Lecture du code…",
    search: "Recherche dans le projet…",
    doc: "Rédaction de la documentation…",
    recommend: "Analyse en cours…",
    overview: "Construction de la vue d'ensemble…",
  };
  return labels[feature] || "Traitement…";
}
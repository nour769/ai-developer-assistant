import { useState } from "react";
import UploadZone from "./components/UploadZone.jsx";
import ResultPanel from "./components/ResultPanel.jsx";
import {
  ingestProject,
  explain,
  generateDoc,
  recommend,
  getOverview,
  downloadReadme,
  deployment,
} from "./api.js";

const FEATURES = [
  { id: "explain", label: "Expliquer", icon: "→", needsQuestion: true, category: "Analyse" },
  { id: "doc", label: "Documenter", icon: "¶", needsQuestion: false, category: "Génération" },
  { id: "recommend", label: "Recommander", icon: "!", needsQuestion: false, category: "Génération" },
  { id: "overview", label: "Vue d'ensemble", icon: "▤", needsQuestion: false, category: "Génération" },
  { id: "deployment", label: "Architecture", icon: "⚙", needsQuestion: false, category: "Déploiement", hasParams: true },
];

const HANDLERS = { explain, doc: generateDoc, recommend, deployment };

// Requête envoyée par défaut pour les fonctionnalités "one-click" qui
// s'appuient sur generateDoc()/recommend() -- ces deux fonctions backend
// attendent toujours une "question" pour faire leur retrieval, donc on en
// fournit une par défaut qui cible l'ensemble du projet plutôt que
// d'obliger l'utilisateur à taper quelque chose.
const DEFAULT_QUERIES = {
  doc: "Documente l'ensemble du projet.",
  recommend: "Analyse l'ensemble du projet et propose des recommandations d'amélioration (optimisation, bonnes pratiques, vulnérabilités).",
};

// Libellé du bouton "one-click" affiché dans le panneau principal pour
// chaque fonctionnalité qui n'a pas besoin de saisie utilisateur.
const ONE_CLICK_LABELS = {
  overview: "Générer la vue d'ensemble",
  doc: "Télécharger la documentation",
  recommend: "Lancer l'analyse du projet",
};

export default function App() {
  const [uploadStatus, setUploadStatus] = useState(null);
  const [activeFeature, setActiveFeature] = useState("explain");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  
  // Paramètres pour deployment
  const [deployService, setDeployService] = useState("AWS");
  const [deployUsage, setDeployUsage] = useState("small");
  const [deployProjectName, setDeployProjectName] = useState("Mon Projet");

  const handleUpload = async (file) => {
    setUploadStatus({ state: "loading" });
    setResult(null);
    try {
      const data = await ingestProject(file);
      setUploadStatus({ state: "success", ...data });
      setDeployProjectName(file.name.replace(".zip", ""));
    } catch (e) {
      setUploadStatus({ state: "error", message: e.message });
    }
  };

  // Exécute une fonctionnalité donnée avec une question donnée.
  // Séparé de runFeature() pour pouvoir être appelé directement au clic
  // sur un bouton de la sidebar (features one-click), sans attendre un
  // second clic sur "Lancer".
  const executeFeature = async (featureId, questionValue) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      if (featureId === "doc") {
        // Télécharge le README au lieu de l'afficher
        await downloadReadme();
        setResult("✓ Documentation téléchargée avec succès !");
      } else if (featureId === "overview") {
        const data = await getOverview();
        setResult(data.result);
      } else if (featureId === "deployment") {
        const data = await deployment(deployProjectName, deployService, deployUsage);
        setResult(data.result);
      } else {
        const data = await HANDLERS[featureId](questionValue);
        setResult(data.result);
      }
    } catch (e) {
      setError(e.message || "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  };

  // Appelé par le bouton "Lancer" du panneau principal pour explain/search
  // (features qui nécessitent une saisie utilisateur).
  const runFeature = () => {
    const feature = FEATURES.find((f) => f.id === activeFeature);
    if (feature.needsQuestion && !question.trim()) return;

    const effectiveQuestion = feature.needsQuestion
      ? question
      : DEFAULT_QUERIES[activeFeature];

    executeFeature(activeFeature, effectiveQuestion);
  };

  // Appelé directement au clic sur un bouton de la sidebar.
  const handleNavClick = (feature) => {
    setActiveFeature(feature.id);
    setResult(null);
    setError(null);

    // Overview, Doc et Recommend s'exécutent immédiatement au clic,
    // sans attendre de saisie utilisateur.
    if (!feature.needsQuestion) {
      executeFeature(feature.id, DEFAULT_QUERIES[feature.id]);
    }
  };

  const currentFeature = FEATURES.find((f) => f.id === activeFeature);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <svg width="50" height="40" viewBox="0 0 100 80" style={{ marginRight: '8px' }}>
            {/* Triangle jaune EY */}
            <polygon points="20,10 60,10 20,50" fill="#ffed00" />
            {/* Texte EY */}
            <text x="20" y="68" fontFamily="Arial, sans-serif" fontSize="48" fontWeight="900" fill="white">EY</text>
          </svg>
        </div>
        <div style={{ fontSize: '11px', color: '#999999', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
          Shape the future
        </div>

        <UploadZone onUpload={handleUpload} status={uploadStatus} />

        <nav className="feature-nav">
          <div className="feature-nav-label">Actions</div>
          {FEATURES.map((f) => (
            <button
              key={f.id}
              className={`feature-btn ${activeFeature === f.id ? "active" : ""}`}
              onClick={() => handleNavClick(f)}
            >
              <span className="icon">{f.icon}</span>
              {f.label}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main">
        {currentFeature.needsQuestion && (
          <div className="query-bar">
            <input
              className="query-input"
              placeholder={placeholderFor(activeFeature)}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && runFeature()}
            />
            <button
              className="query-submit"
              onClick={runFeature}
              disabled={loading || !question.trim()}
            >
              Lancer
            </button>
          </div>
        )}

        {currentFeature.id === "deployment" && (
          <div className="query-bar deployment-params">
            <div className="param-group">
              <label>Service Cloud:</label>
              <select value={deployService} onChange={(e) => setDeployService(e.target.value)}>
                <option value="AWS">AWS</option>
                <option value="Azure">Azure</option>
                <option value="Private">Serveur Privé</option>
              </select>
            </div>
            <div className="param-group">
              <label>Volume d'usage:</label>
              <select value={deployUsage} onChange={(e) => setDeployUsage(e.target.value)}>
                <option value="small">Petit (&lt; 1k req/day)</option>
                <option value="huge">Énorme (&gt; 100k req/day)</option>
              </select>
            </div>
            <button
              className="query-submit"
              onClick={() => executeFeature("deployment", "")}
              disabled={loading}
            >
              Générer l'architecture
            </button>
          </div>
        )}

        {!currentFeature.needsQuestion && activeFeature !== "deployment" && (
          <div className="query-bar">
            <button
              className="query-submit"
              onClick={() => executeFeature(activeFeature, DEFAULT_QUERIES[activeFeature])}
              disabled={loading}
            >
              {ONE_CLICK_LABELS[activeFeature]}
            </button>
          </div>
        )}

        <ResultPanel
          loading={loading}
          error={error}
          result={result}
          feature={activeFeature}
        />
      </main>
    </div>
  );
}

function placeholderFor(feature) {
  const map = {
    explain: "Que fait la fonction login ?",
  };
  return map[feature] || "Pose ta question…";
}

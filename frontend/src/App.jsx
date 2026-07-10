import { useState } from "react";
import UploadZone from "./components/UploadZone.jsx";
import ResultPanel from "./components/ResultPanel.jsx";
import {
  ingestProject,
  explain,
  search,
  generateDoc,
  recommend,
  getOverview,
} from "./api.js";

const FEATURES = [
  { id: "explain", label: "Expliquer", icon: "→", needsQuestion: true },
  { id: "search", label: "Rechercher", icon: "◎", needsQuestion: true },
  { id: "doc", label: "Documenter", icon: "¶", needsQuestion: true },
  { id: "recommend", label: "Analyser", icon: "!", needsQuestion: true },
  { id: "overview", label: "Vue d'ensemble", icon: "▤", needsQuestion: false },
];

const HANDLERS = { explain, search, doc: generateDoc, recommend };

export default function App() {
  const [uploadStatus, setUploadStatus] = useState(null);
  const [activeFeature, setActiveFeature] = useState("explain");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async (file) => {
    setUploadStatus({ state: "loading" });
    setResult(null);
    try {
      const data = await ingestProject(file);
      setUploadStatus({ state: "success", ...data });
    } catch (e) {
      setUploadStatus({ state: "error", message: e.message });
    }
  };

  const runFeature = async () => {
    const feature = FEATURES.find((f) => f.id === activeFeature);
    if (feature.needsQuestion && !question.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data =
        activeFeature === "overview"
          ? await getOverview()
          : await HANDLERS[activeFeature](question);
      setResult(data.result);
    } catch (e) {
      setError(e.message || "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  };

  const currentFeature = FEATURES.find((f) => f.id === activeFeature);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-dot" />
          AI Developer Assistant
        </div>

        <UploadZone onUpload={handleUpload} status={uploadStatus} />

        <nav className="feature-nav">
          <div className="feature-nav-label">Actions</div>
          {FEATURES.map((f) => (
            <button
              key={f.id}
              className={`feature-btn ${activeFeature === f.id ? "active" : ""}`}
              onClick={() => {
                setActiveFeature(f.id);
                setResult(null);
                setError(null);
              }}
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

        {!currentFeature.needsQuestion && (
          <div className="query-bar">
            <button className="query-submit" onClick={runFeature} disabled={loading}>
              Générer la vue d'ensemble
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
    search: "vérification des identifiants",
    doc: "documente check_credentials",
    recommend: "auth.py",
  };
  return map[feature] || "Pose ta question…";
}
import { useState, useEffect } from "react";
import "../styles/ProjectHistory.css";

export default function ProjectHistory({ onProjectSelect, currentProjectId }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/projects");
      const data = await response.json();
      setProjects(data.projects || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleActivate = async (projectId) => {
    try {
      const response = await fetch(
        `http://localhost:8000/projects/${projectId}/activate`,
        { method: "POST" }
      );
      const data = await response.json();
      
      if (!response.ok) {
        // Erreur du serveur
        setError(`⚠️ ${data.detail || data.message || "Erreur lors de l'activation"}`);
        return;
      }
      
      if (onProjectSelect) {
        onProjectSelect(projectId, data.message);
      }
      setError(null);
      loadProjects(); // Rafraîchit la liste pour montrer le projet actif
    } catch (e) {
      setError(`❌ Erreur: ${e.message}`);
    }
  };

  const formatDate = (isoDate) => {
    const date = new Date(isoDate);
    return date.toLocaleDateString("fr-FR", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return <div className="project-history-container">⏳ Chargement...</div>;
  }

  if (projects.length === 0) {
    return (
      <div className="project-history-container">
        <p className="empty-state">Aucun projet pour le moment</p>
      </div>
    );
  }

  return (
    <div className="project-history-container">
      <h3>📁 Projets précédents</h3>
      {error && <div className="error-message">{error}</div>}

      <div className="projects-list">
        {projects.map((project) => (
          <div
            key={project.id}
            className={`project-item ${
              project.is_active ? "active" : ""
            }`}
          >
            <div
              className="project-header"
              onClick={() =>
                setExpandedId(expandedId === project.id ? null : project.id)
              }
            >
              <div className="project-name-section">
                {project.is_active && <span className="active-badge">✓ ACTIF</span>}
                <span className="project-name">{project.name}</span>
                <span className="project-date">{formatDate(project.uploaded_at)}</span>
              </div>
              <button
                className="activate-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleActivate(project.id);
                }}
                disabled={project.is_active}
              >
                {project.is_active ? "✓ Activé" : "Activer"}
              </button>
            </div>

            {expandedId === project.id && (
              <div className="project-details">
                <p>
                  <strong>📦 Chunks:</strong> {project.chunks_count || 0}
                </p>
                <p>
                  <strong>🆔 Collection:</strong> {project.collection_id.slice(0, 8)}...
                </p>
                <p>
                  <strong>📅 Uploadé:</strong> {new Date(project.uploaded_at).toLocaleString("fr-FR")}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      <button className="refresh-btn" onClick={loadProjects}>
        🔄 Rafraîchir
      </button>
    </div>
  );
}

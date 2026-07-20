const BASE_URL = "http://localhost:8000";

async function post(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Erreur ${res.status}`);
  }
  return res.json();
}

export async function ingestProject(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/ingest`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Erreur ${res.status}`);
  }
  return res.json();
}

export const explain = (question) => post("/explain", { question });
export const search = (question) => post("/search", { question });
export const generateDoc = (question) => post("/doc", { question });
export const recommend = (question) => post("/recommend", { question });
export const deployment = (projectName, service, usageLevel) => 
  post("/deployment", { project_name: projectName, service, usage_level: usageLevel });

export async function getOverview() {
  const res = await fetch(`${BASE_URL}/overview`);
  if (!res.ok) throw new Error("Erreur overview");
  return res.json();
}

export async function listProjects() {
  const res = await fetch(`${BASE_URL}/projects`);
  if (!res.ok) throw new Error("Erreur listing projets");
  return res.json();
}

export async function getProject(projectId) {
  const res = await fetch(`${BASE_URL}/projects/${projectId}`);
  if (!res.ok) throw new Error("Erreur récupération projet");
  return res.json();
}

export async function exportProject(projectId) {
  const res = await fetch(`${BASE_URL}/projects/${projectId}/export`);
  if (!res.ok) throw new Error("Erreur export projet");
  
  const data = await res.json();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `project-export-${projectId}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export async function downloadReadme() {
  const res = await fetch(`${BASE_URL}/readme/download`);
  if (!res.ok) throw new Error("Erreur téléchargement README");
  
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "PROJECT_README.md";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}
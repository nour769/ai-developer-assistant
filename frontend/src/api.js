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

export async function getOverview() {
  const res = await fetch(`${BASE_URL}/overview`);
  if (!res.ok) throw new Error("Erreur overview");
  return res.json();
}
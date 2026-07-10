import { useRef, useState } from "react";

export default function UploadZone({ onUpload, status }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = (file) => {
    if (file && file.name.endsWith(".zip")) onUpload(file);
  };

  return (
    <div>
      <div
        className={`upload-zone ${dragging ? "dragging" : ""} ${
          status?.state === "loading" ? "scanning" : ""
        }`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFile(e.dataTransfer.files[0]);
        }}
      >
        {status?.state === "loading"
          ? "Analyse du projet en cours…"
          : "Glisse un .zip ici ou clique pour importer"}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept=".zip"
        hidden
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {status?.state === "success" && (
        <div className="project-status" style={{ marginTop: 10 }}>
          <strong>{status.chunks_created} chunks</strong> indexés depuis{" "}
          {status.files_found} fichier(s).
        </div>
      )}
      {status?.state === "error" && (
        <div className="error-banner" style={{ marginTop: 10 }}>
          {status.message}
        </div>
      )}
    </div>
  );
}
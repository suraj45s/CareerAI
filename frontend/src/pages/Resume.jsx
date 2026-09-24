import { useEffect, useState } from "react";

function Resume() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [resume, setResume] = useState(null);
  useEffect(() => {
  const fetchResume = async () => {
    const token = localStorage.getItem("access_token");

    const response = await fetch(
      "http://127.0.0.1:8000/resume",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (response.ok) {
      setResume(data);
    }
  };

  fetchResume();
}, []);
const handleViewResume = async () => {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    "http://127.0.0.1:8000/resume/view",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    alert("Unable to open resume");
    return;
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  window.open(url, "_blank");
};

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a PDF file.");
      return;
    }

    const token = localStorage.getItem("access_token");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/upload-resume",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      }
    );

    const data = await response.json();

    if (response.ok) {
      setMessage("Resume uploaded successfully!");
    } else {
      setMessage(data.detail || "Upload failed.");
    }
  };

  return (
    <div>
      <h1>Upload Resume</h1>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button type="submit">
          Upload Resume
        </button>
      </form>
     {resume && (
  <div>
    <h2>My Resume</h2>

    <p>📄 {resume.file_name}</p>

    <button onClick={handleViewResume}>
  View Resume
</button>
  </div>
)}

      {message && <p>{message}</p>}
    </div>
  );
}

export default Resume;
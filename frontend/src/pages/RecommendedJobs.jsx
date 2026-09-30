import { useEffect, useState } from "react";

function RecommendedJobs() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchRecommendedJobs = async () => {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "http://127.0.0.1:8000/recommended-jobs",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.ok) {
        setJobs(data);
      }
    };

    fetchRecommendedJobs();
  }, []);

  return (
    <div>
      <h1>Recommended Jobs</h1>

      {jobs.map((job) => (
        <div key={job.id}>
          <h2>{job.title}</h2>

          <p>
            <strong>Company:</strong> {job.company}
          </p>

          <p>
            <strong>Location:</strong> {job.location}
          </p>

          <p>
            <strong>Required Skills:</strong> {job.required_skills}
          </p>

          <p>
            <strong>Match:</strong> {job.match_percentage}%
          </p>

          <a
            href={job.apply_url}
            target="_blank"
            rel="noreferrer"
          >
            Apply
          </a>
        </div>
      ))}
    </div>
  );
}

export default RecommendedJobs;
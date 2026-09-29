import { useEffect, useState } from "react";

function Jobs() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      const response = await fetch(
        "http://127.0.0.1:8000/jobs"
      );

      const data = await response.json();

      if (response.ok) {
        setJobs(data);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div>
      <h1>Available Jobs</h1>

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
            <strong>Description:</strong> {job.description}
          </p>

          <p>
            <strong>Required Skills:</strong>{" "}
            {job.required_skills}
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

export default Jobs;
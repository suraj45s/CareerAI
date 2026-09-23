import { useEffect, useState } from "react";
import "../App.css";

function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("access_token");

      const response = await fetch("http://127.0.0.1:8000/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setProfile(data);
      } else {
        console.error(data);
      }
    };

    fetchProfile();
  }, []);

  if (!profile) {
    return <h2>Loading profile...</h2>;
  }

  return (
    <div className="profile-page">
      <h1>My Profile</h1>

      <p><strong>Name:</strong> {profile.name}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <p><strong>Phone:</strong> {profile.phone}</p>
      <p><strong>College:</strong> {profile.college}</p>
      <p><strong>Degree:</strong> {profile.degree}</p>
      <p><strong>Branch:</strong> {profile.branch}</p>
      <p><strong>Graduation Year:</strong> {profile.graduation_year}</p>
      <p><strong>Skills:</strong> {profile.skills}</p>
      <p><strong>GitHub:</strong> {profile.github}</p>
      <p><strong>LinkedIn:</strong> {profile.linkedin}</p>
    </div>
  );
}

export default Profile;
import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [posts, setPosts] = useState([]);
  const [file, setFile] = useState(null);
  const [desc, setDesc] = useState("");

  useEffect(() => {
    fetch('http://localhost:8000/posts')
      .then(res => res.json())
      .then(data => setPosts(data))
      .catch(err => console.error('Error fetching posts:', err));
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("desc", desc);
    formData.append("photo", file);

    await fetch("http://localhost:8000/posts", {
      method: "POST",
      body: formData
    });

    setFile(null);
    setDesc("");
    location.reload(); // crude but effective for refreshing post list
  };

  return (
    <div className="p-4">
      <h1>SpotMap Prototype</h1>

      <form onSubmit={handleUpload} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Description"
          value={desc}
          onChange={e => setDesc(e.target.value)}
          required
        />
        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
          required
        />
        <button type="submit">Upload</button>
      </form>

      {posts.map(post => (
        <div key={post.id} style={{ marginBottom: '1rem' }}>
          <img
            src={`http://localhost:8000/uploads/${post.photo}`}
            alt={post.desc}
            style={{ maxWidth: '300px' }}
          />
          <p>{post.desc}</p>
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
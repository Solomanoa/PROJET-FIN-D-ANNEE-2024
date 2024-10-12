// src/App.jsx
import { useState } from 'react';
import './App.css';

function App() {
  const [name, setName] = useState("");
  const [fname, setFname] = useState("");
  const [image, setImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(""); // Pour afficher les messages d'erreur

  const addUser = async () => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('fname', fname);
    formData.append('image', image); // Assurez-vous que c'est un fichier

    try {
      const response = await fetch("http://127.0.0.1:8000/user/register/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('User registered:', data);
      setErrorMessage(""); // Réinitialise le message d'erreur
    } catch (err) {
      console.error('Error registering user:', err);
      setErrorMessage("Failed to register user. Please try again."); // Affiche un message d'erreur
    }
  };

  return (
    <>
      <h1>User Registration</h1>
      <div>
        <input 
          type="text"
          placeholder="Name"
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="First Name"
          onChange={(e) => setFname(e.target.value)}
        />
        
        {/* Champ d'upload d'image */}
        <input 
          type="file" 
          accept="image/*" 
          onChange={(e) => setImage(e.target.files[0])} // Gérer l'upload d'image
        />

        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>} {/* Affiche le message d'erreur */}

        <button onClick={addUser}>Register User</button>
      </div>
    </>
  );
}

export default App;

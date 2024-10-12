import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';

const LoginPage = () => {
  const [image, setImage] = useState(null);
  const [authResult, setAuthResult] = useState('');
  const [userInfo, setUserInfo] = useState(null); // Stocker les infos de l'utilisateur authentifié
  const webcamRef = useRef(null);

  // Capture l'image depuis la webcam et la transforme en Blob
  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();

    // Conversion de l'image base64 en Blob (objet binaire)
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        setImage(blob);  // Enregistre l'image capturée sous forme de Blob
      });
  };

  // Envoie l'image capturée au backend pour authentification
  const handleAuth = async () => {
    if (!image) {
      setAuthResult('Aucune image capturée');
      return;
    }

    const formData = new FormData();
    formData.append('image', image, 'capture.jpg'); // Ajout d'un nom de fichier par défaut

    try {
      const response = await fetch('http://localhost:8000/utilisateur/authenticate-face/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Échec de l\'authentification');
      }

      const data = await response.json();

      if (data.user_info) {
        setUserInfo(data.user_info);  // Stocke les informations de l'utilisateur
        setAuthResult(data.message);  // Affiche le message d'authentification réussie
      } else {
        setAuthResult(data.message);  // Affiche le message d'échec d'authentification
      }
    } catch (error) {
      setAuthResult('Échec de l\'authentification. Veuillez réessayer.');
    }
  };

  return (
    <div>
      <h1>Authentification Faciale</h1>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={320}
        height={240}
      />
      <button onClick={capture}>Capturer l'image</button>

      {image && (
        <div>
          <h2>Image Capturée :</h2>
          <img src={URL.createObjectURL(image)} alt="Image capturée" />
          <button onClick={handleAuth}>Authentifier</button>
        </div>
      )}

      {authResult && <p>{authResult}</p>}

      {/* Affichage des informations de l'utilisateur authentifié */}
      {userInfo && (
        <div>
          <h2>Informations de l'utilisateur :</h2>
          <p>Email : {userInfo.email}</p>
          <p>Nom : {userInfo.nom}</p>
          <p>Prénom : {userInfo.prenom}</p>
          <p>Pseudo : {userInfo.pseudo}</p>
          <p>Téléphone : {userInfo.tel}</p>
          <p>Matricule : {userInfo.matricule}</p>
        </div>
      )}
    </div>
  );
};

export default LoginPage;

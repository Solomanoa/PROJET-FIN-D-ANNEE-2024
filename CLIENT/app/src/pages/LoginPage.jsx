import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';  // Importez useNavigate pour la redirection


const LoginPage = () => {
  const [image, setImage] = useState(null);
  const [authResult, setAuthResult] = useState('');
  const [userInfo, setUserInfo] = useState(null); // Stocker les infos de l'utilisateur authentifié
  const [isWebcamVisible, setIsWebcamVisible] = useState(true); // Contrôle la visibilité de la webcam
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  // Capture l'image depuis la webcam et la transforme en Blob
  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();

    // Conversion de l'image base64 en Blob (objet binaire)
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        setImage(blob);  // Enregistre l'image capturée sous forme de Blob
        setIsWebcamVisible(false);  // Cache la webcam après la capture
        handleAuth(blob);  // Lancer l'authentification immédiatement après la capture
      });
  };

  // Envoie l'image capturée au backend pour authentification
  const handleAuth = async (capturedImage) => {
    if (!capturedImage) {
      setAuthResult('Aucune image capturée');
      return;
    }

    const formData = new FormData();
    formData.append('image', capturedImage, 'capture.jpg'); // Ajout d'un nom de fichier par défaut

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
        
        // Rediriger vers la page dashboard après 2 secondes
        setTimeout(() => {
          navigate('/dashboard');  // Redirige vers la page "dashboard"
        }, 2000);
      
      } else {
        setAuthResult(data.message);  // Affiche le message d'échec d'authentification
      }
    } catch (error) {
      setAuthResult('Échec de l\'authentification. Veuillez réessayer.');
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (webcamRef.current) {
        capture();
      }
    }, 5000);  // Capture toutes les 5 secondes
  
    return () => clearInterval(interval);  // Nettoie l'intervalle si le composant est démonté
  }, []);
  return (
    <div>
      <h1>Authentification Faciale</h1>
      {isWebcamVisible && (
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={320}
          height={240}
        />
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

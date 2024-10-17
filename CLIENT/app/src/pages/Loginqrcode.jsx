import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import jsQR from 'jsqr';
import { useNavigate } from 'react-router-dom';

const QrCodeAuthPage = () => {
  const [authResult, setAuthResult] = useState('');
  const [userInfo, setUserInfo] = useState(null); // Stocker les infos de l'utilisateur authentifié
  const [isWebcamVisible, setIsWebcamVisible] = useState(true); // Contrôle la visibilité de la webcam
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  // Fonction pour scanner le QR code
  const scanQRCode = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      const image = new Image();
      image.src = imageSrc;

      image.onload = () => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = image.width;
        canvas.height = image.height;
        context.drawImage(image, 0, 0);
        
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code) {
          handleAuth(code.data); // Lancer l'authentification avec les données du QR code
        }
      };
    }
  };

  const handleAuth = async (qrData) => {
    const formData = new FormData();
    formData.append('qr_data', qrData); // Ajoutez les données du QR code au FormData
  
    try {
      const response = await fetch('http://localhost:8000/utilisateur/authenticate-qrcode/', {
        method: 'POST',
        body: formData,
      });
  
      const data = await response.json();
      console.log('Response data:', data);  // Log pour voir la réponse
  
      // Vérifiez directement si les données sont présentes
      if (data && data.id) {
        setUserInfo(data);  // Stocke les informations de l'utilisateur
        setAuthResult('Authentification réussie');
        
        // Rediriger vers la page dashboard après 2 secondes
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      } else {
        setAuthResult('Échec de l\'authentification');
      }
    } catch (error) {
      setAuthResult('Échec de l\'authentification. Veuillez réessayer.');
    }
  };
  
  // Capture automatiquement et scanne le QR code toutes les 5 secondes
  useEffect(() => {
    const timer = setInterval(() => {
      scanQRCode();
    }, 5000);  // Scanne toutes les 5 secondes

    return () => clearInterval(timer);  // Nettoie le timer si le composant est démonté
  }, []);

  return (
    <div>
      <h1>Authentification par QR Code</h1>
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
         
          <p>Nom : {userInfo.nom}</p>
          <p>Prénom : {userInfo.prenom}</p>
        
        </div>
      )}
    </div>
  );
};

export default QrCodeAuthPage;

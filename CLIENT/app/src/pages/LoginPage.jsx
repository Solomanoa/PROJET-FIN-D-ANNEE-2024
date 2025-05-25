import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  // Vos états et fonctions existants restent inchangés
  const [image, setImage] = useState(null);
  const [authResult, setAuthResult] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const [isWebcamVisible, setIsWebcamVisible] = useState(true);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        setImage(blob);
        setIsWebcamVisible(false);
        handleAuth(blob);
      });
  };

  const handleAuth = async (capturedImage) => {
    if (!capturedImage) {
      setAuthResult('Aucune image capturée');
      return;
    }

    const formData = new FormData();
    formData.append('image', capturedImage, 'capture.jpg');

    try {
      const response = await fetch('http://localhost:8000/utilisateur/authenticate-face/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Échec de l\'authentification');

      const data = await response.json();

      if (data.user_info) {
        setUserInfo(data.user_info);
        setAuthResult(data.message);
        //setTimeout(() => navigate('/dashboard'), 2000);
      } else {
        setAuthResult(data.message);
      }
    } catch (error) {
      setAuthResult('Échec de l\'authentification. Veuillez réessayer.');
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (webcamRef.current && isWebcamVisible) capture();
    }, 5000);
    return () => clearInterval(interval);
  }, [isWebcamVisible]);

  // Styles CSS en plein écran
  const styles = {
    fullscreenContainer: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: '#121212',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      zIndex: 1000
    },
    webcamWrapper: {
      width: '100%',
      maxWidth: '800px',
      height: '60vh',
      position: 'relative',
      overflow: 'hidden',
      borderRadius: '8px',
      boxShadow: '0 0 20px rgba(0, 0, 0, 0.5)'
    },
    title: {
      fontSize: '2rem',
      marginBottom: '2rem',
      textAlign: 'center'
    },
    statusMessage: {
      padding: '1rem',
      margin: '1rem 0',
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
      borderRadius: '4px',
      textAlign: 'center'
    },
    userInfo: {
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
      padding: '1.5rem',
      borderRadius: '8px',
      marginTop: '2rem',
      maxWidth: '800px',
      width: '100%'
    },
    instruction: {
      marginTop: '1rem',
      color: 'rgba(255, 255, 255, 0.7)',
      fontSize: '0.9rem'
    }
  };

  return (
    <div style={styles.fullscreenContainer}>
      <h1 style={styles.title}>Authentification Faciale</h1>
      
      {isWebcamVisible ? (
        <>
          <div style={styles.webcamWrapper}>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width="100%"
              height="100%"
              style={{ objectFit: 'cover' }}
              mirrored
            />
          </div>
          <p style={styles.instruction}>Positionnez votre visage dans le cadre</p>
        </>
      ) : (
        <div style={styles.statusMessage}>
          {authResult || "Analyse en cours..."}
        </div>
      )}

      {userInfo && (
        <div style={styles.userInfo}>
          <h2>Bienvenue, {userInfo.prenom} {userInfo.nom}</h2>
          <p>Pseudo: {userInfo.pseudo}</p>
          <p>Matricule: {userInfo.matricule}</p>
        </div>
      )}
    </div>
  );
};

export default LoginPage;
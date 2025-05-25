import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import jsQR from 'jsqr';
import { useNavigate } from 'react-router-dom';

const QrCodeAuthPage = () => {
  const [authResult, setAuthResult] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  // Styles plein écran
  const styles = {
    container: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      background: '#121212',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontFamily: 'Arial, sans-serif',
      padding: '20px',
      boxSizing: 'border-box'
    },
    title: {
      fontSize: '1.8rem',
      marginBottom: '30px',
      textAlign: 'center'
    },
    webcamContainer: {
      position: 'relative',
      width: '100%',
      maxWidth: '500px',
      height: '300px',
      borderRadius: '12px',
      overflow: 'hidden',
      marginBottom: '20px'
    },
    scanOverlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 2
    },
    scanBox: {
      width: '70%',
      maxWidth: '300px',
      height: '300px',
      border: '4px solid rgba(255, 255, 255, 0.3)',
      borderRadius: '8px',
      position: 'relative'
    },
    scanLine: {
      position: 'absolute',
      width: '100%',
      height: '2px',
      background: 'rgba(255, 0, 0, 0.8)',
      animation: 'scan 2.5s infinite linear'
    },
    status: {
      padding: '15px',
      borderRadius: '8px',
      margin: '20px 0',
      background: 'rgba(255, 255, 255, 0.1)',
      textAlign: 'center',
      maxWidth: '500px',
      width: '100%'
    },
    success: {
      background: 'rgba(46, 213, 115, 0.2)',
      border: '1px solid rgba(46, 213, 115, 0.5)'
    },
    error: {
      background: 'rgba(255, 71, 87, 0.2)',
      border: '1px solid rgba(255, 71, 87, 0.5)'
    }
  };

  const scanQRCode = () => {
    if (isLoading || !webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    const image = new Image();
    image.src = imageSrc;

    image.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = image.width;
      canvas.height = image.height;
      const context = canvas.getContext('2d');
      context.drawImage(image, 0, 0);

      try {
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (code) {
          handleAuth(code.data);
        }
      } catch (error) {
        console.error('Erreur de scan:', error);
        setAuthResult('Erreur lors du scan');
      }
    };
  };

  const handleAuth = async (qrData) => {
    setIsLoading(true);
    setAuthResult('Validation en cours...');

    try {
      const response = await fetch('http://localhost:8000/utilisateur/authenticate-qrcode/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ qr_data: qrData }),
      });

      const data = await response.json();

      if (data?.id) {
        setUserInfo(data);
        setAuthResult('Authentification réussie !');
        setTimeout(() => navigate('/dashboard'), 2000);
      } else {
        setAuthResult(data?.message || 'Échec de l\'authentification');
      }
    } catch (error) {
      setAuthResult('Erreur de connexion au serveur');
      console.error('Erreur:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const timer = setInterval(scanQRCode, 2000);
    return () => clearInterval(timer);
  }, [isLoading]);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Authentification QR Code</h1>
      
      <div style={styles.webcamContainer}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width="100%"
          height="100%"
          style={{ objectFit: 'cover' }}
          videoConstraints={{ facingMode: 'environment' }}
        />
        <div style={styles.scanOverlay}>
          <div style={styles.scanBox}>
            <div style={styles.scanLine}></div>
          </div>
        </div>
      </div>

      <div style={{
        ...styles.status,
        ...(authResult.includes('réussie') ? styles.success : styles.error)
      }}>
        {authResult || 'Positionnez le QR code dans le cadre'}
        {isLoading && <div>Veuillez patienter...</div>}
      </div>

      <style>{`
        @keyframes scan {
          0% { top: 0; }
          100% { top: 100%; }
        }
      `}</style>
    </div>
  );
};

export default QrCodeAuthPage;
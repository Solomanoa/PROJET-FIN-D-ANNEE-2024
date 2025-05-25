import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const WelcomePage = () => {
  const [activeButton, setActiveButton] = useState(null);

  // Styles optimisés
  const styles = {
    fullscreen: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      background: 'radial-gradient(circle at 10% 20%, #2a2a3a 0%, #1e1e2e 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: "'Inter', sans-serif",
      padding: '20px',
      boxSizing: 'border-box',
      color: '#ffffff',
      overflow: 'hidden'
    },
    card: {
      background: 'rgba(255, 255, 255, 0.05)',
      borderRadius: '20px',
      padding: '40px 30px',
      width: '90%',
      maxWidth: '400px',
      textAlign: 'center',
      backdropFilter: 'blur(12px)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      boxShadow: '0 12px 40px rgba(0, 0, 0, 0.25)',
      transform: 'translateY(0)',
      transition: 'transform 0.4s ease, box-shadow 0.4s ease'
    },
    cardHover: {
      transform: 'translateY(-5px)',
      boxShadow: '0 15px 50px rgba(0, 0, 0, 0.35)'
    },
    title: {
      fontSize: '2.4rem',
      margin: '0 0 10px 0',
      fontWeight: 700,
      background: 'linear-gradient(90deg, #ff9a9e, #fad0c4)',
      WebkitBackgroundClip: 'text',
      backgroundClip: 'text',
      color: 'transparent',
      lineHeight: '1.2'
    },
    subtitle: {
      fontSize: '0.95rem',
      color: 'rgba(255, 255, 255, 0.65)',
      marginBottom: '30px',
      lineHeight: '1.6',
      fontWeight: 400
    },
    button: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      padding: '16px',
      margin: '12px 0',
      borderRadius: '12px',
      border: 'none',
      fontSize: '0.95rem',
      fontWeight: 500,
      cursor: 'pointer',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      color: 'white',
      position: 'relative',
      overflow: 'hidden',
      zIndex: 1
    },
    buttonPrimary: {
      background: 'linear-gradient(45deg, #ff6b6b, #ff8e53)'
    },
    buttonSecondary: {
      background: 'linear-gradient(45deg, #48dbfb, #1dd1a1)'
    },
    buttonTertiary: {
      background: 'linear-gradient(45deg, #5f27cd, #9980fa)'
    },
    buttonHover: {
      transform: 'translateY(-3px) scale(1.02)',
      boxShadow: '0 8px 25px rgba(0, 0, 0, 0.25)'
    },
    buttonActive: {
      transform: 'translateY(1px) scale(0.99)'
    },
    buttonIcon: {
      marginRight: '10px',
      fontSize: '1.1rem'
    },
    particles: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      zIndex: 0
    },
    particle: {
      position: 'absolute',
      borderRadius: '50%',
      background: 'rgba(255,255,255,0.1)',
      animation: 'float 15s infinite linear'
    }
  };

  // Générer des particules décoratives
  const particles = Array.from({ length: 8 }).map((_, i) => ({
    size: Math.random() * 60 + 30,
    top: Math.random() * 100,
    left: Math.random() * 100,
    animationDelay: Math.random() * 15,
    opacity: Math.random() * 0.1 + 0.05
  }));

  return (
    <div style={styles.fullscreen}>
      {/* Particules d'arrière-plan */}
      <div style={styles.particles}>
        {particles.map((p, i) => (
          <div key={i} style={{
            ...styles.particle,
            width: `${p.size}px`,
            height: `${p.size}px`,
            top: `${p.top}%`,
            left: `${p.left}%`,
            animationDelay: `${p.animationDelay}s`,
            opacity: p.opacity
          }} />
        ))}
      </div>

      {/* Carte principale */}
      <div 
        style={{
          ...styles.card,
          ...(activeButton && styles.cardHover)
        }}
        onMouseEnter={() => setActiveButton('card')}
        onMouseLeave={() => setActiveButton(null)}
      >
        <h1 style={styles.title}>Bienvenue</h1>
        <p style={styles.subtitle}>Accédez à votre espace en choisissant une méthode sécurisée</p>
        
        <Link to="/loginqrcode" style={{ textDecoration: 'none' }}>
          <button 
            style={{ 
              ...styles.button, 
              ...styles.buttonPrimary,
              ...(activeButton === 'qrcode' && styles.buttonHover)
            }}
            onMouseEnter={() => setActiveButton('qrcode')}
            onMouseLeave={() => activeButton === 'qrcode' && setActiveButton(null)}
            onMouseDown={() => setActiveButton('qrcode-active')}
            onMouseUp={() => setActiveButton('qrcode')}
          >
            <span style={styles.buttonIcon}>📱</span>
            Authentification QR Code
          </button>
        </Link>

        <Link to="/login" style={{ textDecoration: 'none' }}>
          <button 
            style={{ 
              ...styles.button, 
              ...styles.buttonSecondary,
              ...(activeButton === 'face' && styles.buttonHover)
            }}
            onMouseEnter={() => setActiveButton('face')}
            onMouseLeave={() => activeButton === 'face' && setActiveButton(null)}
            onMouseDown={() => setActiveButton('face-active')}
            onMouseUp={() => setActiveButton('face')}
          >
            <span style={styles.buttonIcon}>👤</span>
            Reconnaissance Faciale
          </button>
        </Link>

        <Link to="/register" style={{ textDecoration: 'none' }}>
          <button 
            style={{ 
              ...styles.button, 
              ...styles.buttonTertiary,
              ...(activeButton === 'register' && styles.buttonHover)
            }}
            onMouseEnter={() => setActiveButton('register')}
            onMouseLeave={() => activeButton === 'register' && setActiveButton(null)}
            onMouseDown={() => setActiveButton('register-active')}
            onMouseUp={() => setActiveButton('register')}
          >
            <span style={styles.buttonIcon}>✏️</span>
            Créer un compte
          </button>
        </Link>
      </div>

      {/* Animations CSS */}
      <style>{`
        @keyframes float {
          0% { transform: translateY(0) rotate(0deg); opacity: 0.1; }
          50% { transform: translateY(-20px) rotate(180deg); opacity: 0.15; }
          100% { transform: translateY(0) rotate(360deg); opacity: 0.1; }
        }
      `}</style>
    </div>
  );
};

export default WelcomePage;
import React from 'react';
import { Link } from 'react-router-dom';

const WelcomePage = () => {
  return (
    <div>
      <h1>Bienvenue sur notre application !</h1>
      <Link to="/login">
        <button>S'authentifier</button>
      </Link>
      <Link to="/register">
        <button>S'enregistrer</button>
      </Link>
    </div>
  );
};

export default WelcomePage;

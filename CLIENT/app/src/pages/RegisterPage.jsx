import React, { useState } from 'react';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    nom: '',
    prenom: '',
    pseudo: '',
    tel: '',
    matricule: '',
    photo: null,
    type: '',
    carte_etudiant: null,
    titre: '',
    role: '',
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    const { name } = e.target;
    setFormData({
      ...formData,
      [name]: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMessage('');
    setSuccessMessage('');

    const formDataToSend = new FormData();
    for (const key in formData) {
      if (formData[key] !== null && formData[key] !== '') {
        formDataToSend.append(key, formData[key]);
      }
    }

    try {
      const response = await fetch('http://localhost:8000/utilisateur/utilisateurs/create/', {
        method: 'POST',
        body: formDataToSend,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Échec de l\'enregistrement');
      }

      const data = await response.json();
      setSuccessMessage('Inscription réussie !');
      console.log('User created:', data);
      
      // Réinitialisation du formulaire après succès
      setFormData({
        email: '',
        nom: '',
        prenom: '',
        pseudo: '',
        tel: '',
        matricule: '',
        photo: null,
        type: '',
        carte_etudiant: null,
        titre: '',
        role: '',
      });
    } catch (error) {
      console.error('Erreur:', error);
      setErrorMessage(error.message || 'Une erreur est survenue lors de l\'inscription');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Styles CSS inline
  const styles = {
    container: {
      maxWidth: '600px',
      margin: '0 auto',
      padding: '2rem',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
    },
    title: {
      textAlign: 'center',
      color: '#2c3e50',
      marginBottom: '2rem'
    },
    formGroup: {
      marginBottom: '1.5rem'
    },
    label: {
      display: 'block',
      marginBottom: '0.5rem',
      fontWeight: '600',
      color: '#2c3e50'
    },
    input: {
      width: '100%',
      padding: '0.75rem',
      border: '1px solid #ced4da',
      borderRadius: '4px',
      fontSize: '1rem'
    },
    select: {
      width: '100%',
      padding: '0.75rem',
      border: '1px solid #ced4da',
      borderRadius: '4px',
      fontSize: '1rem',
      backgroundColor: 'white'
    },
    fileInput: {
      width: '100%',
      padding: '0.5rem',
      border: '1px dashed #ced4da',
      borderRadius: '4px'
    },
    button: {
      width: '100%',
      padding: '0.75rem',
      backgroundColor: '#3498db',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      fontSize: '1rem',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'background-color 0.3s'
    },
    buttonHover: {
      backgroundColor: '#2980b9'
    },
    buttonDisabled: {
      backgroundColor: '#95a5a6',
      cursor: 'not-allowed'
    },
    successMessage: {
      color: '#27ae60',
      margin: '1rem 0',
      textAlign: 'center'
    },
    errorMessage: {
      color: '#e74c3c',
      margin: '1rem 0',
      textAlign: 'center'
    },
    conditionalFields: {
      padding: '1rem',
      backgroundColor: '#ecf0f1',
      borderRadius: '4px',
      marginTop: '1rem'
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Créer un compte</h1>
      
      {successMessage && <div style={styles.successMessage}>{successMessage}</div>}
      {errorMessage && <div style={styles.errorMessage}>{errorMessage}</div>}

      <form onSubmit={handleSubmit}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Email *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            style={styles.input}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Nom *</label>
          <input
            type="text"
            name="nom"
            value={formData.nom}
            onChange={handleInputChange}
            style={styles.input}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Prénom *</label>
          <input
            type="text"
            name="prenom"
            value={formData.prenom}
            onChange={handleInputChange}
            style={styles.input}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Pseudo</label>
          <input
            type="text"
            name="pseudo"
            value={formData.pseudo}
            onChange={handleInputChange}
            style={styles.input}
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Téléphone</label>
          <input
            type="tel"
            name="tel"
            value={formData.tel}
            onChange={handleInputChange}
            style={styles.input}
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Matricule</label>
          <input
            type="text"
            name="matricule"
            value={formData.matricule}
            onChange={handleInputChange}
            style={styles.input}
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Photo</label>
          <input
            type="file"
            name="photo"
            onChange={handleFileChange}
            style={styles.fileInput}
            accept="image/*"
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Type d'utilisateur *</label>
          <select 
            name="type" 
            value={formData.type} 
            onChange={handleInputChange}
            style={styles.select}
            required
          >
            <option value="">-- Sélectionnez un type --</option>
            <option value="etudiant">Étudiant</option>
            <option value="enseignant">Enseignant</option>
            <option value="admin">Administrateur</option>
            <option value="responsable">Responsable Pédagogique</option>
          </select>
        </div>

        {formData.type === 'etudiant' && (
          <div style={{...styles.conditionalFields, ...styles.formGroup}}>
            <label style={styles.label}>Carte d'étudiant</label>
            <input
              type="file"
              name="carte_etudiant"
              onChange={handleFileChange}
              style={styles.fileInput}
              accept="image/*,.pdf"
            />
          </div>
        )}

        {formData.type === 'enseignant' && (
          <div style={{...styles.conditionalFields, ...styles.formGroup}}>
            <label style={styles.label}>Titre</label>
            <input
              type="text"
              name="titre"
              value={formData.titre}
              onChange={handleInputChange}
              style={styles.input}
            />
          </div>
        )}

        {formData.type === 'responsable' && (
          <div style={{...styles.conditionalFields, ...styles.formGroup}}>
            <label style={styles.label}>Rôle</label>
            <input
              type="text"
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              style={styles.input}
            />
          </div>
        )}

        <button 
          type="submit" 
          style={{
            ...styles.button,
            ...(isSubmitting ? styles.buttonDisabled : {}),
          }}
          disabled={isSubmitting}
          onMouseEnter={(e) => !isSubmitting && (e.currentTarget.style.backgroundColor = styles.buttonHover.backgroundColor)}
          onMouseLeave={(e) => !isSubmitting && (e.currentTarget.style.backgroundColor = styles.button.backgroundColor)}
        >
          {isSubmitting ? 'Enregistrement en cours...' : 'S\'enregistrer'}
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;
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
    empreinte_digitale: null,
    type: '',
    niveau: '',
    titre: '',
    role: '',
  });

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

    const formDataToSend = new FormData();
    for (const key in formData) {
      formDataToSend.append(key, formData[key]);
    }

    try {
      const response = await fetch('http://localhost:8000/utilisateur/utilisateurs/create/', {
        method: 'POST',
        body: formDataToSend,
      });

      if (!response.ok) {
        throw new Error('Failed to register user');
      }

      const data = await response.json();
      alert('Utilisateur créé avec succès');
      console.log('User created:', data);
    } catch (error) {
      console.error('Erreur lors de la création de l’utilisateur:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="nom"
        placeholder="Nom"
        value={formData.nom}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="prenom"
        placeholder="Prénom"
        value={formData.prenom}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="pseudo"
        placeholder="Pseudo"
        value={formData.pseudo}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="tel"
        placeholder="Téléphone"
        value={formData.tel}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="matricule"
        placeholder="Matricule"
        value={formData.matricule}
        onChange={handleInputChange}
      />
      <input
        type="file"
        name="photo"
        onChange={handleFileChange}
      />
      <select name="type" value={formData.type} onChange={handleInputChange}>
        <option value="">Choisir un type</option>
        <option value="etudiant">Étudiant</option>
        <option value="enseignant">Enseignant</option>
        <option value="admin">Administrateur</option>
        <option value="responsable">Responsable Pédagogique</option>
      </select>

      {/* Champs supplémentaires basés sur le type sélectionné */}
      {formData.type === 'etudiant' && (
        <select name="niveau" value={formData.niveau} onChange={handleInputChange}>
        <option value="">Choisir un niveau</option>
        <option value="L1">L1</option>
        <option value="L2">L2</option>
        <option value="L3">L3</option>
        <option value="M1">M1</option>
        <option value="M2">M2</option>
      </select>
      )}
      {formData.type === 'enseignant' && (
        <input
          type="text"
          name="titre"
          placeholder="Titre"
          value={formData.titre}
          onChange={handleInputChange}
        />
      )}
      {formData.type === 'responsable' && (
        <input
          type="text"
          name="role"
          placeholder="Rôle"
          value={formData.role}
          onChange={handleInputChange}
        />
      )}

      <button type="submit">S'enregistrer</button>
    </form>
  );
};



export default RegisterPage;
// src/components/BarcodeCapture.jsx
import React, { useState } from 'react';
import { QrReader } from 'react-qr-reader'; 

const BarcodeCapture = ({ onBarcode }) => {
  const [error, setError] = useState(null);

  const handleScan = (data) => {
    if (data) {
      onBarcode(data); // Envoie le code-barres au parent
    }
  };

  const handleError = (err) => {
    setError(err);
  };

  return (
    <div>
      <h2>Scan Barcode</h2>
      <QrReader
        delay={300}
        onError={handleError}
        onScan={handleScan}
        style={{ width: '100%' }}
      />
      {error && <p>Error: {error.message}</p>}
    </div>
  );
};

export default BarcodeCapture;

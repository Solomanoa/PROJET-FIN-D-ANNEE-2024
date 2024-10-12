// src/components/FingerprintCapture.jsx
import React from 'react';

const FingerprintCapture = ({ onFingerprint }) => {
  const handleCapture = () => {
    const simulatedFingerprint = new Uint8Array([/* some bytes here */]);
    onFingerprint(simulatedFingerprint);
  };

  return (
    <div>
      <button onClick={handleCapture}>Capture Fingerprint</button>
    </div>
  );
};

export default FingerprintCapture;


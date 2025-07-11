import React, { useState } from 'react';
import { uploadFile } from '../api/minioApi';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    try {
      const res = await uploadFile(file);
      alert("File uploaded successfully!");
      console.log(res.data);
    } catch (err) {
      alert("Upload failed.");
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUpload;

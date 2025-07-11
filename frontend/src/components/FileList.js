import React, { useState, useEffect } from 'react';
import { listFiles, deleteFile, getPresignedUrl, getFileInfo } from '../api/minioApi';

const FileList = () => {
  const [files, setFiles] = useState([]);
  const [hoveredFileInfo, setHoveredFileInfo] = useState(null);

  const fetchFiles = async () => {
    const res = await listFiles();
    setFiles(res.data.files);
  };

  const handleView = async (filename) => {
    const res = await getPresignedUrl(filename);
    window.open(res.data.url, "_blank");
  };

  const handleDelete = async (filename) => {
    await deleteFile(filename);
    fetchFiles();
  };

  const handleHover = async (filename) => {
    try {
      const res = await getFileInfo(filename);
      setHoveredFileInfo(res.data);
    } catch (e) {
      setHoveredFileInfo({ filename, error: "No metadata found" });
    }
  };

  const handleLeave = () => {
    setHoveredFileInfo(null);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div>
      <h3>Uploaded Files</h3>
      <ul>
        {files.map((file) => (
          <li key={file}
              onMouseEnter={() => handleHover(file)}
              onMouseLeave={handleLeave}>
            {file}
            <button onClick={() => handleView(file)}>View</button>
            <button onClick={() => handleDelete(file)}>Delete</button>
          </li>
        ))}
      </ul>

      {hoveredFileInfo && (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "10px" }}>
          <strong>File Info:</strong><br />
          Name: {hoveredFileInfo.filename}<br />
          Size: {hoveredFileInfo.size} bytes<br />
          Type: {hoveredFileInfo.content_type}<br />
          Last Modified: {hoveredFileInfo.metadata['Last-Modified']}<br />
          ETag: {hoveredFileInfo.etag}<br />
        </div>
      )}
    </div>
  );
};

export default FileList;
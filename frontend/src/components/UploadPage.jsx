import { useState, useRef } from 'react';

// ==========================================================================
// UPLOAD PAGE
// Lets the officer upload a document image (required) and optionally a
// live/presented face photo. Supports drag-and-drop and a Browse button.
// Validates file type before allowing "Start Screening".
// ==========================================================================

const ACCEPTED_TYPES = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];

function isValidFile(file) {
  return file && ACCEPTED_TYPES.includes(file.type);
}

function UploadPage({ onStartScreening }) {
  const [docFile, setDocFile] = useState(null);
  const [docPreview, setDocPreview] = useState(null);
  const [faceFile, setFaceFile] = useState(null);
  const [facePreview, setFacePreview] = useState(null);
  const [error, setError] = useState('');
  const [dragOverDoc, setDragOverDoc] = useState(false);

  const docInputRef = useRef(null);
  const faceInputRef = useRef(null);

  function handleDocFile(file) {
    if (!isValidFile(file)) {
      setError('Please upload a valid image file (PNG, JPG, or WEBP).');
      return;
    }
    setError('');
    setDocFile(file);
    setDocPreview(URL.createObjectURL(file));
  }

  function handleFaceFile(file) {
    if (!isValidFile(file)) {
      setError('Please upload a valid image file (PNG, JPG, or WEBP) for the face photo.');
      return;
    }
    setError('');
    setFaceFile(file);
    setFacePreview(URL.createObjectURL(file));
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOverDoc(false);
    const file = e.dataTransfer.files[0];
    handleDocFile(file);
  }

  function handleStart() {
    if (!docFile) {
      setError('Please upload a document before starting screening.');
      return;
    }
    onStartScreening({ docPreview, facePreview });
  }

  return (
    <div className="page-container">
      <div className="page-heading">
        <h1>Document Upload</h1>
        <p className="text-muted">
          Upload the identity document to begin the verification pipeline.
        </p>
      </div>

      <div className="card">
        <h3 className="card__title">1. Identity Document (required)</h3>

        {!docPreview ? (
          <div
            className={`dropzone ${dragOverDoc ? 'dropzone--active' : ''}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOverDoc(true);
            }}
            onDragLeave={() => setDragOverDoc(false)}
            onDrop={handleDrop}
          >
            <p className="dropzone__text">Drag and drop a document image here</p>
            <p className="text-muted dropzone__or">or</p>
            <button
              type="button"
              className="btn btn--secondary"
              onClick={() => docInputRef.current.click()}
            >
              Browse File
            </button>
            <input
              ref={docInputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={(e) => handleDocFile(e.target.files[0])}
            />
          </div>
        ) : (
          <div className="preview-block">
            <img src={docPreview} alt="Document preview" className="preview-image" />
            <div className="preview-actions">
              <span className="text-muted">{docFile.name}</span>
              <button
                className="btn btn--ghost"
                onClick={() => {
                  setDocFile(null);
                  setDocPreview(null);
                }}
              >
                Remove &amp; Replace
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="card__title">2. Live / Presented Face Photo (optional)</h3>
        <p className="text-muted card__subtitle">
          Used to match against the photo printed on the document.
        </p>

        {!facePreview ? (
          <div className="dropzone dropzone--secondary">
            <p className="dropzone__text">No live photo uploaded yet</p>
            <button
              type="button"
              className="btn btn--secondary"
              onClick={() => faceInputRef.current.click()}
            >
              Browse File
            </button>
            <input
              ref={faceInputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={(e) => handleFaceFile(e.target.files[0])}
            />
          </div>
        ) : (
          <div className="preview-block">
            <img src={facePreview} alt="Face preview" className="preview-image preview-image--face" />
            <div className="preview-actions">
              <span className="text-muted">{faceFile.name}</span>
              <button
                className="btn btn--ghost"
                onClick={() => {
                  setFaceFile(null);
                  setFacePreview(null);
                }}
              >
                Remove &amp; Replace
              </button>
            </div>
          </div>
        )}
      </div>

      {error && <div className="alert alert--error">{error}</div>}

      <div className="upload-page__footer">
        <button className="btn btn--primary btn--lg" onClick={handleStart}>
          Start Screening
        </button>
      </div>
    </div>
  );
}

export default UploadPage;
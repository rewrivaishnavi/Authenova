import { useState } from 'react';
import Navbar from './components/Navbar';
import LoginPage from './components/LoginPage';
import UploadPage from './components/UploadPage';
import PipelineProgress from './components/PipelineProgress';
import ResultsPage from './components/ResultsPage';
import { generateMockResult } from './data/mockData';
import './App.css';

// ==========================================================================
// APP
// Controls which screen is currently shown: login -> upload -> pipeline
// -> results. All shared state (previews, results) lives here and is
// passed down as props. No routing library is used to keep this simple.
// ==========================================================================

function App() {
  // 'login' | 'upload' | 'pipeline' | 'results'
  const [page, setPage] = useState('login');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [docPreview, setDocPreview] = useState(null);
  const [facePreview, setFacePreview] = useState(null);
  const [results, setResults] = useState(null);

  function handleLoginSuccess() {
    setIsLoggedIn(true);
    setPage('upload');
  }

  function handleLogout() {
    setIsLoggedIn(false);
    setPage('login');
    setDocPreview(null);
    setFacePreview(null);
    setResults(null);
  }

  function handleStartScreening({ docPreview, facePreview }) {
    setDocPreview(docPreview);
    setFacePreview(facePreview);
    setPage('pipeline');
  }

  function handlePipelineComplete() {
    setResults(generateMockResult());
    setPage('results');
  }

  function handleStartNew() {
    setDocPreview(null);
    setFacePreview(null);
    setResults(null);
    setPage('upload');
  }

  return (
    <div className="app-shell">
      <Navbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />

      <main className="app-main">
        {page === 'login' && <LoginPage onLoginSuccess={handleLoginSuccess} />}

        {page === 'upload' && <UploadPage onStartScreening={handleStartScreening} />}

        {page === 'pipeline' && <PipelineProgress onComplete={handlePipelineComplete} />}

        {page === 'results' && results && (
          <ResultsPage
            results={results}
            docPreview={docPreview}
            facePreview={facePreview}
            onStartNew={handleStartNew}
          />
        )}
      </main>
    </div>
  );
}

export default App;
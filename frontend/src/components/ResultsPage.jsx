import OcrResults from './OcrResults';
import ValidationChecklist from './ValidationChecklist';
import TamperingDetection from './TamperingDetection';
import FaceVerification from './FaceVerification';
import RiskDashboard from './RiskDashboard';
import OfficerDecision from './OfficerDecision';

// ==========================================================================
// RESULTS PAGE
// The unified screening dashboard. Composes every results section using
// the mock result object generated after the pipeline finishes.
// ==========================================================================

function ResultsPage({ results, docPreview, facePreview, onStartNew }) {
  return (
    <div className="page-container">
      <div className="page-heading page-heading--row">
        <div>
          <h1>Screening Results</h1>
          <p className="text-muted">Case reference: AUTHENOVA-{results.risk.score}0921</p>
        </div>
        <button className="btn btn--secondary" onClick={onStartNew}>
          Start New Screening
        </button>
      </div>

      <RiskDashboard risk={results.risk} />

      <OcrResults ocr={results.ocr} />

      <ValidationChecklist validation={results.validation} />

      <TamperingDetection tampering={results.tampering} docPreview={docPreview} />

      <FaceVerification
        faceVerification={results.faceVerification}
        docPreview={docPreview}
        facePreview={facePreview}
      />

      <OfficerDecision />
    </div>
  );
}

export default ResultsPage;
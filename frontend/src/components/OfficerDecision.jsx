import { useState } from 'react';

// ==========================================================================
// OFFICER DECISION PANEL
// Lets the officer approve, flag for review, or reject the applicant, with
// an optional comment. Shows a confirmation once a decision is recorded.
// ==========================================================================

function OfficerDecision() {
  const [comment, setComment] = useState('');
  const [recordedDecision, setRecordedDecision] = useState(null);

  function handleDecision(action) {
    setRecordedDecision({ action, comment });
  }

  return (
    <div className="card">
      <h3 className="card__title">Officer Decision</h3>
      <p className="text-muted card__subtitle">
        Record your final decision based on the evidence above.
      </p>

      <label className="form-label" htmlFor="comment">
        Comment (optional)
      </label>
      <textarea
        id="comment"
        className="form-textarea"
        placeholder="Add any notes for the case file..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={3}
      />

      <div className="decision-actions">
        <button
          className="btn btn--pass"
          onClick={() => handleDecision('Approved')}
        >
          Approve
        </button>
        <button
          className="btn btn--warning"
          onClick={() => handleDecision('Flagged for Review')}
        >
          Flag for Review
        </button>
        <button
          className="btn btn--fail"
          onClick={() => handleDecision('Rejected')}
        >
          Reject
        </button>
      </div>

      {recordedDecision && (
        <div className="alert alert--success">
          Decision recorded: <strong>{recordedDecision.action}</strong>
          {recordedDecision.comment && (
            <span> — "{recordedDecision.comment}"</span>
          )}
        </div>
      )}
    </div>
  );
}

export default OfficerDecision;

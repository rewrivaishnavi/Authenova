const LEVEL_TO_STATUS = {
  LOW: 'pass',
  MEDIUM: 'warning',
  HIGH: 'fail',
};

function RiskDashboard({ risk }) {
  const status = LEVEL_TO_STATUS[risk.level] || 'warning';

  return (
    <div className={`card risk-card risk-card--${status}`}>
      <h3 className="card__title">Overall Risk Assessment</h3>

      <div className="risk-summary">
        <div className={`risk-badge risk-badge--${status}`}>
          {risk.level}
        </div>

        <div className="risk-score-block">
          <span className="risk-score-block__label">Risk Score</span>
          <span className="risk-score-block__value">
            {risk.score} / 100
          </span>
        </div>
      </div>

      <h4 className="risk-reasons__title">
        Why this decision was made
      </h4>

      <ul className="risk-reasons">
        {risk.reasons.map((reason, index) => (
          <li
            key={index}
            className={`risk-reason risk-reason--${reason.tone}`}
          >
            <span
              className={`risk-reason__dot risk-reason__dot--${reason.tone}`}
            />
            {reason.text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RiskDashboard;
import { useEffect, useState } from 'react';
import { PIPELINE_STAGES } from '../data/mockData';

// ==========================================================================
// PIPELINE PROGRESS
// Simulates a multi-stage verification pipeline using setTimeout.
// Once all stages complete, it calls onComplete() to move to the results page.
// ==========================================================================

const STAGE_DURATION_MS = 900;

function PipelineProgress({ onComplete }) {
  const [currentStageIndex, setCurrentStageIndex] = useState(0);

  useEffect(() => {
    if (currentStageIndex >= PIPELINE_STAGES.length) {
      // Small pause on "complete" before moving to results
      const finishTimer = setTimeout(() => {
        onComplete();
      }, 600);
      return () => clearTimeout(finishTimer);
    }

    const timer = setTimeout(() => {
      setCurrentStageIndex((prev) => prev + 1);
    }, STAGE_DURATION_MS);

    return () => clearTimeout(timer);
  }, [currentStageIndex, onComplete]);

  const isAllDone = currentStageIndex >= PIPELINE_STAGES.length;

  return (
    <div className="page-container page-container--narrow">
      <div className="page-heading">
        <h1>Running Verification Pipeline</h1>
        <p className="text-muted">Please wait while the document is analyzed.</p>
      </div>

      <div className="card pipeline-card">
        {PIPELINE_STAGES.map((stage, index) => {
          let status = 'pending';
          if (index < currentStageIndex) status = 'done';
          else if (index === currentStageIndex && !isAllDone) status = 'active';

          return (
            <div key={stage.key} className={`pipeline-step pipeline-step--${status}`}>
              <div className="pipeline-step__indicator">
                {status === 'done' && '✓'}
                {status === 'active' && <span className="spinner" />}
                {status === 'pending' && index + 1}
              </div>
              <div className="pipeline-step__label">{stage.label}</div>
              <div className="pipeline-step__status">
                {status === 'done' && 'Complete'}
                {status === 'active' && 'In progress...'}
                {status === 'pending' && 'Waiting'}
              </div>
            </div>
          );
        })}

        {isAllDone && (
          <div className="pipeline-step pipeline-step--done pipeline-step--final">
            <div className="pipeline-step__indicator">✓</div>
            <div className="pipeline-step__label">All stages complete</div>
            <div className="pipeline-step__status">Preparing results...</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PipelineProgress;
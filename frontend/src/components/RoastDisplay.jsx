import './RoastDisplay.css'

const RoastDisplay = ({ data, onReset }) => {
  const { roast, features, total_processing_time_ms, request_id } = data

  return (
    <div className="roast-display">
      <div className="roast-card">
        <div className="roast-header">
          <h2>Your Roast</h2>
        </div>

        <div className="roast-content">
          <p className="roast-text">{roast}</p>
        </div>

        {features && (
          <div className="features-section">
            <h3>Analysis Details</h3>

            {features.face_analysis && (
              <div className="feature-card">
                <h4>Face Analysis</h4>
                <div className="feature-grid">
                  <div className="feature-item">
                    <span className="feature-label">Faces Detected:</span>
                    <span className="feature-value">{features.face_analysis.face_count || 0}</span>
                  </div>
                  {features.face_analysis.gender && (
                    <div className="feature-item">
                      <span className="feature-label">Gender:</span>
                      <span className="feature-value">{features.face_analysis.gender}</span>
                    </div>
                  )}
                  {features.face_analysis.emotion && (
                    <div className="feature-item">
                      <span className="feature-label">Emotion:</span>
                      <span className="feature-value">{features.face_analysis.emotion}</span>
                    </div>
                  )}
                  {features.face_analysis.attractiveness_score && (
                    <div className="feature-item">
                      <span className="feature-label">Attractiveness:</span>
                      <span className="feature-value">{features.face_analysis.attractiveness_score}/10</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {features.vlm_scene_analysis && (
              <div className="feature-card">
                <h4>Scene Analysis</h4>
                <div className="scene-description">
                  <p>{features.vlm_scene_analysis.scene_description}</p>
                </div>
              </div>
            )}

            <div className="stats">
              <div className="stat-item">
                <span className="stat-label">Processing Time:</span>
                <span className="stat-value">{total_processing_time_ms.toFixed(2)}ms</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Request ID:</span>
                <span className="stat-value stat-id">{request_id}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <button className="btn btn-secondary reset-btn" onClick={onReset}>
        Roast Another Image
      </button>
    </div>
  )
}

export default RoastDisplay


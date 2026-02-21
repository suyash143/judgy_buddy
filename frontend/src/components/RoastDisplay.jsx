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
                  {features.face_analysis.age && (
                    <div className="feature-item">
                      <span className="feature-label">Age:</span>
                      <span className="feature-value">~{features.face_analysis.age}</span>
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

            {features.body_analysis && (
              <div className="feature-card">
                <h4>Body Analysis</h4>
                <div className="feature-grid">
                  {features.body_analysis.pose && (
                    <div className="feature-item">
                      <span className="feature-label">Pose:</span>
                      <span className="feature-value">{features.body_analysis.pose}</span>
                    </div>
                  )}
                  {features.body_analysis.body_type && (
                    <div className="feature-item">
                      <span className="feature-label">Body Type:</span>
                      <span className="feature-value">{features.body_analysis.body_type}</span>
                    </div>
                  )}
                  {features.body_analysis.clothing_style && (
                    <div className="feature-item">
                      <span className="feature-label">Style:</span>
                      <span className="feature-value">{features.body_analysis.clothing_style}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {features.demographics && (
              <div className="feature-card">
                <h4>Demographics</h4>
                <div className="feature-grid">
                  {features.demographics.race && (
                    <div className="feature-item">
                      <span className="feature-label">Race:</span>
                      <span className="feature-value">{features.demographics.race}</span>
                    </div>
                  )}
                  {features.demographics.skin_tone && (
                    <div className="feature-item">
                      <span className="feature-label">Skin Tone:</span>
                      <span className="feature-value">{features.demographics.skin_tone}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {features.object_scene && (
              <div className="feature-card">
                <h4>Scene & Objects</h4>
                <div className="feature-grid">
                  {features.object_scene.scene_type && (
                    <div className="feature-item">
                      <span className="feature-label">Scene:</span>
                      <span className="feature-value">{features.object_scene.scene_type}</span>
                    </div>
                  )}
                  {features.object_scene.background_type && (
                    <div className="feature-item">
                      <span className="feature-label">Background:</span>
                      <span className="feature-value">{features.object_scene.background_type}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {features.quality_aesthetics && (
              <div className="feature-card">
                <h4>Quality & Aesthetics</h4>
                <div className="feature-grid">
                  {features.quality_aesthetics.quality_score && (
                    <div className="feature-item">
                      <span className="feature-label">Quality:</span>
                      <span className="feature-value">{features.quality_aesthetics.quality_score}/10</span>
                    </div>
                  )}
                  {features.quality_aesthetics.aesthetic_score && (
                    <div className="feature-item">
                      <span className="feature-label">Aesthetics:</span>
                      <span className="feature-value">{features.quality_aesthetics.aesthetic_score}/10</span>
                    </div>
                  )}
                  {features.quality_aesthetics.lighting_quality && (
                    <div className="feature-item">
                      <span className="feature-label">Lighting:</span>
                      <span className="feature-value">{features.quality_aesthetics.lighting_quality}</span>
                    </div>
                  )}
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


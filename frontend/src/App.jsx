import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import RoastDisplay from './components/RoastDisplay'
import './App.css'

function App() {
  const [roastData, setRoastData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleRoastReceived = (data) => {
    setRoastData(data)
    setLoading(false)
    setError(null)
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
    if (isLoading) {
      setError(null)
      setRoastData(null)
    }
  }

  const handleError = (errorMessage) => {
    setError(errorMessage)
    setLoading(false)
    setRoastData(null)
  }

  const handleReset = () => {
    setRoastData(null)
    setError(null)
    setLoading(false)
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">I Judge</h1>
          <p className="subtitle">Upload. Analyze. Get Roasted.</p>
        </header>

        <main className="main">
          {!roastData && !loading && (
            <ImageUpload
              onRoastReceived={handleRoastReceived}
              onLoading={handleLoading}
              onError={handleError}
            />
          )}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Analyzing your image and crafting the perfect roast...</p>
            </div>
          )}

          {error && (
            <div className="error">
              <p>{error}</p>
              <button onClick={handleReset} className="btn btn-secondary">
                Try Again
              </button>
            </div>
          )}

          {roastData && (
            <RoastDisplay data={roastData} onReset={handleReset} />
          )}
        </main>

        <footer className="footer">
          <p>Powered by AI. No feelings spared.</p>
        </footer>
      </div>
    </div>
  )
}

export default App


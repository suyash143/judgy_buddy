import { useState, useRef } from 'react'
import axios from 'axios'
import './ImageUpload.css'

const ImageUpload = ({ onRoastReceived, onLoading, onError }) => {
  const [selectedImage, setSelectedImage] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [roastLevel, setRoastLevel] = useState('medium')
  const fileInputRef = useRef(null)

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        onError('Please select a valid image file')
        return
      }
      
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async () => {
    if (!selectedImage) {
      onError('Please select an image first')
      return
    }

    onLoading(true)

    const formData = new FormData()
    formData.append('image', selectedImage)
    formData.append('roast_level', roastLevel)

    try {
      const response = await axios.post('http://localhost:8000/api/v1/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onRoastReceived(response.data)
    } catch (error) {
      console.error('Error:', error)
      onError(error.response?.data?.detail || 'Failed to analyze image. Please try again.')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  return (
    <div className="image-upload">
      <div
        className="upload-area"
        onClick={() => fileInputRef.current.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {previewUrl ? (
          <div className="preview">
            <img src={previewUrl} alt="Preview" />
          </div>
        ) : (
          <div className="upload-placeholder">
            <div className="upload-icon"></div>
            <p className="upload-text">Click to upload or drag & drop</p>
            <p className="upload-hint">JPEG, PNG, WEBP</p>
          </div>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleImageSelect}
          style={{ display: 'none' }}
        />
      </div>

      <div className="roast-level-selector">
        <label>Roast Level</label>
        <div className="level-buttons">
          <button
            className={`level-btn ${roastLevel === 'mild' ? 'active' : ''}`}
            onClick={() => setRoastLevel('mild')}
          >
            Mild
          </button>
          <button
            className={`level-btn ${roastLevel === 'medium' ? 'active' : ''}`}
            onClick={() => setRoastLevel('medium')}
          >
            Medium
          </button>
          <button
            className={`level-btn ${roastLevel === 'savage' ? 'active' : ''}`}
            onClick={() => setRoastLevel('savage')}
          >
            Savage
          </button>
        </div>
      </div>

      <button
        className="btn btn-primary submit-btn"
        onClick={handleSubmit}
        disabled={!selectedImage}
      >
        Generate Roast
      </button>
    </div>
  )
}

export default ImageUpload


'use client'

import { useState } from 'react'
import styles from './page.module.css'

// Get API URL from environment variable (set in Netlify dashboard)
// Must start with NEXT_PUBLIC_ to be available in browser
// Remove trailing slash to avoid double slashes in URLs
const getApiUrl = () => {
  const url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  return url.replace(/\/+$/, '') // Remove trailing slashes
}

const API_URL = getApiUrl()

// Debug: Log API URL in development (removed in production build)
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  console.log('API URL:', API_URL)
}

export default function Home() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)
      
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(selectedFile)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!file) {
      setError('Please select a photo first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('photo', file)

      // Construct API endpoint URL (ensure no double slashes)
      const endpoint = `${API_URL}/personalize`.replace(/([^:]\/)\/+/g, '$1')
      
      // Log API URL for debugging
      console.log('Calling API at:', endpoint)
      console.log('File size:', file.size, 'bytes')

      // Add timeout for long-running requests (60 seconds)
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 60000)

      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      }).finally(() => clearTimeout(timeoutId))

      console.log('Response status:', response.status)
      console.log('Response headers:', Object.fromEntries(response.headers.entries()))

      if (!response.ok) {
        let errorData
        try {
          errorData = await response.json()
        } catch (e) {
          errorData = { detail: `Server error: ${response.status} ${response.statusText}` }
        }
        throw new Error(errorData.detail || 'Failed to process image')
      }

      // Parse response
      let data
      try {
        data = await response.json()
        console.log('Response received, keys:', Object.keys(data))
        console.log('Response status:', data.status)
        if (data.image_base64) {
          console.log('Image data length:', data.image_base64.length, 'characters')
        } else {
          console.warn('No image_base64 in response')
        }
      } catch (parseError) {
        console.error('Failed to parse JSON response:', parseError)
        // Clone response to read as text for debugging
        const clonedResponse = response.clone()
        const text = await clonedResponse.text()
        console.error('Response text (first 500 chars):', text.substring(0, 500))
        throw new Error('Invalid response format from server. Expected JSON but got: ' + text.substring(0, 100))
      }
      
      if (data.status === 'success' && data.image_base64) {
        console.log('Image received, length:', data.image_base64.length)
        setResult(`data:image/${data.format || 'png'};base64,${data.image_base64}`)
      } else {
        console.error('Invalid response data:', data)
        throw new Error('Invalid response from server: missing image data')
      }
    } catch (err) {
      let errorMessage = 'An error occurred while processing your photo'
      
      if (err.name === 'AbortError') {
        errorMessage = 'Request timed out. The image processing is taking longer than expected. Please try again.'
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setError(errorMessage)
      console.error('Error details:', {
        name: err.name,
        message: err.message,
        stack: err.stack
      })
    } finally {
      setLoading(false)
    }
  }

  const downloadImage = () => {
    if (result) {
      const link = document.createElement('a')
      link.href = result
      link.download = 'personalized-book-page.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>PictoBook AI</h1>
        <p className={styles.subtitle}>Transform your photos into personalized children's book illustrations</p>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.uploadSection}>
            <label htmlFor="photo-upload" className={styles.uploadLabel}>
              <input
                id="photo-upload"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className={styles.fileInput}
              />
              <div className={styles.uploadBox}>
                {preview ? (
                  <img src={preview} alt="Preview" className={styles.preview} />
                ) : (
                  <div className={styles.uploadPlaceholder}>
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    <p>Click to upload a photo</p>
                    <p className={styles.uploadHint}>JPG, PNG, or WEBP</p>
                  </div>
                )}
              </div>
            </label>
          </div>

          <button
            type="submit"
            disabled={!file || loading}
            className={styles.submitButton}
          >
            {loading ? 'Processing...' : 'Personalize'}
          </button>
        </form>

        {error && (
          <div className={styles.error}>
            <p>⚠️ {error}</p>
          </div>
        )}

        {loading && (
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>Processing your photo... This may take 10-30 seconds.</p>
          </div>
        )}

        {result && (
          <div className={styles.result}>
            <h2>Your Personalized Book Page</h2>
            <div className={styles.resultImageContainer}>
              <img src={result} alt="Personalized result" className={styles.resultImage} />
            </div>
            <button onClick={downloadImage} className={styles.downloadButton}>
              Download Image
            </button>
          </div>
        )}
      </div>
    </main>
  )
}


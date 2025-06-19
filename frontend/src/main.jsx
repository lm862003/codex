import React from 'react'
import ReactDOM from 'react-dom/client'

function App() {
  return (
    <div className="p-4">
      <h1>SpotMap Prototype</h1>
      <div id="map" style={{ height: '400px' }}></div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)

import { useState } from 'react'
import MapView from './components/MapView'
import './App.css'

function App() {
  // Default center: San Francisco coordinates
  const [mapCenter] = useState([37.7749, -122.4194]);
  const [mapZoom] = useState(10);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Personal Memory Maps</h1>
      </header>
      <main className="map-container">
        <MapView center={mapCenter} zoom={mapZoom} />
      </main>
    </div>
  )
}

export default App

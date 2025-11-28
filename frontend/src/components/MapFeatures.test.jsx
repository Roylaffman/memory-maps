import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { MapContainer, TileLayer } from 'react-leaflet';
import MapFeatures from './MapFeatures';

describe('MapFeatures Component', () => {
  it('renders without crashing with empty features', () => {
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <MapFeatures features={[]} />
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });

  it('renders point features', () => {
    const features = [
      {
        id: 1,
        feature_type: 'point',
        geometry: {
          type: 'Point',
          coordinates: [-122.4194, 37.7749]
        },
        title: 'Test Point',
        description: 'Test description'
      }
    ];
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <MapFeatures features={features} />
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });

  it('renders polygon features', () => {
    const features = [
      {
        id: 2,
        feature_type: 'polygon',
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [-122.42, 37.78],
            [-122.41, 37.78],
            [-122.41, 37.77],
            [-122.42, 37.77],
            [-122.42, 37.78]
          ]]
        },
        title: 'Test Polygon',
        description: 'Test polygon description'
      }
    ];
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <MapFeatures features={features} />
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });
});

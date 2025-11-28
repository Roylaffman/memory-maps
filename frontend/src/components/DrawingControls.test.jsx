import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { MapContainer, TileLayer } from 'react-leaflet';
import DrawingControls from './DrawingControls';

describe('DrawingControls Component', () => {
  it('renders without crashing', () => {
    const mockCallback = vi.fn();
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <DrawingControls onFeatureCreated={mockCallback} />
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });

  it('accepts callback props', () => {
    const onCreated = vi.fn();
    const onEdited = vi.fn();
    const onDeleted = vi.fn();
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <DrawingControls 
          onFeatureCreated={onCreated}
          onFeatureEdited={onEdited}
          onFeatureDeleted={onDeleted}
        />
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });
});

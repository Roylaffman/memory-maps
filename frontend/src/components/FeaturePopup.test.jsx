import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import FeaturePopup from './FeaturePopup';

describe('FeaturePopup Component', () => {
  const mockFeature = {
    id: 1,
    title: 'Test Feature',
    description: 'Test description',
    category: 'Test Category',
    stories: [],
    photos: []
  };

  it('renders without crashing', () => {
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[37.7749, -122.4194]}>
          <FeaturePopup feature={mockFeature} />
        </Marker>
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });

  it('accepts feature prop with all properties', () => {
    const featureWithContent = {
      ...mockFeature,
      stories: [{ title: 'Story 1', content: 'Content 1' }],
      photos: [{ url: 'photo1.jpg', caption: 'Photo 1' }]
    };
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[37.7749, -122.4194]}>
          <FeaturePopup feature={featureWithContent} />
        </Marker>
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });

  it('accepts callback props', () => {
    const onEdit = vi.fn();
    const onDelete = vi.fn();
    
    const { container } = render(
      <MapContainer center={[37.7749, -122.4194]} zoom={10}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[37.7749, -122.4194]}>
          <FeaturePopup 
            feature={mockFeature} 
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </Marker>
      </MapContainer>
    );
    
    expect(container).toBeTruthy();
  });
});

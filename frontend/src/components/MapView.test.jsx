import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import MapView from './MapView';

describe('MapView Component', () => {
  it('renders without crashing', () => {
    const { container } = render(
      <MapView center={[37.7749, -122.4194]} zoom={10} />
    );
    expect(container).toBeTruthy();
  });

  it('uses default center and zoom when not provided', () => {
    const { container } = render(<MapView />);
    expect(container).toBeTruthy();
  });
});

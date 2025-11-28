import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MapGallery from './MapGallery';

describe('MapGallery Component', () => {
  const mockMaps = [
    {
      id: 1,
      title: 'Test Map 1',
      description: 'Description 1',
      is_public: true,
      feature_count: 5,
      created_at: '2024-01-01T00:00:00Z'
    },
    {
      id: 2,
      title: 'Test Map 2',
      description: 'Description 2',
      is_public: false,
      feature_count: 3,
      created_at: '2024-01-02T00:00:00Z'
    }
  ];

  const mockHandlers = {
    onMapSelect: vi.fn(),
    onMapCreate: vi.fn(),
    onMapDelete: vi.fn(),
    onMapShare: vi.fn()
  };

  it('renders gallery header', () => {
    render(<MapGallery maps={[]} {...mockHandlers} />);
    expect(screen.getByText('My Maps')).toBeTruthy();
    expect(screen.getByText('+ Create New Map')).toBeTruthy();
  });

  it('displays empty state when no maps', () => {
    render(<MapGallery maps={[]} {...mockHandlers} />);
    expect(screen.getByText("You haven't created any maps yet")).toBeTruthy();
  });

  it('renders map cards', () => {
    render(<MapGallery maps={mockMaps} {...mockHandlers} />);
    expect(screen.getByText('Test Map 1')).toBeTruthy();
    expect(screen.getByText('Test Map 2')).toBeTruthy();
  });

  it('shows correct visibility badges', () => {
    render(<MapGallery maps={mockMaps} {...mockHandlers} />);
    expect(screen.getByText('🌐 Public')).toBeTruthy();
    expect(screen.getByText('🔒 Private')).toBeTruthy();
  });

  it('filters maps by search query', () => {
    render(<MapGallery maps={mockMaps} {...mockHandlers} />);
    
    const searchInput = screen.getByPlaceholderText('Search maps...');
    fireEvent.change(searchInput, { target: { value: 'Test Map 1' } });
    
    expect(screen.getByText('Test Map 1')).toBeTruthy();
    expect(screen.queryByText('Test Map 2')).toBeNull();
  });

  it('filters maps by visibility', () => {
    render(<MapGallery maps={mockMaps} {...mockHandlers} />);
    
    const publicButton = screen.getByText(/Public \(1\)/);
    fireEvent.click(publicButton);
    
    expect(screen.getByText('Test Map 1')).toBeTruthy();
    expect(screen.queryByText('Test Map 2')).toBeNull();
  });

  it('calls onMapCreate when create button clicked', () => {
    render(<MapGallery maps={[]} {...mockHandlers} />);
    
    const createButton = screen.getByText('Create Your First Map');
    fireEvent.click(createButton);
    
    expect(mockHandlers.onMapCreate).toHaveBeenCalled();
  });
});

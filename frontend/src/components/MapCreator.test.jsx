import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MapCreator from './MapCreator';

describe('MapCreator Component', () => {
  const mockOnSave = vi.fn();
  const mockOnCancel = vi.fn();

  it('renders nothing when not open', () => {
    const { container } = render(
      <MapCreator isOpen={false} onSave={mockOnSave} onCancel={mockOnCancel} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <MapCreator isOpen={true} onSave={mockOnSave} onCancel={mockOnCancel} />
    );
    expect(screen.getByText('Create New Map')).toBeTruthy();
  });

  it('has all required form fields', () => {
    render(
      <MapCreator isOpen={true} onSave={mockOnSave} onCancel={mockOnCancel} />
    );
    
    expect(screen.getByLabelText('Map Title *')).toBeTruthy();
    expect(screen.getByLabelText('Description')).toBeTruthy();
    expect(screen.getByText('Make this map public')).toBeTruthy();
  });

  it('calls onCancel when cancel button clicked', () => {
    render(
      <MapCreator isOpen={true} onSave={mockOnSave} onCancel={mockOnCancel} />
    );
    
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('updates form fields when user types', () => {
    render(
      <MapCreator isOpen={true} onSave={mockOnSave} onCancel={mockOnCancel} />
    );
    
    const titleInput = screen.getByLabelText('Map Title *');
    fireEvent.change(titleInput, { target: { value: 'My New Map' } });
    
    expect(titleInput.value).toBe('My New Map');
  });
});

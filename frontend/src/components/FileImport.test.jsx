import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import FileImport from './FileImport';

describe('FileImport Component', () => {
  const mockOnImport = vi.fn();
  const mockOnCancel = vi.fn();

  it('renders nothing when not open', () => {
    const { container } = render(
      <FileImport isOpen={false} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <FileImport isOpen={true} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    expect(screen.getByText('Import GIS Data')).toBeTruthy();
  });

  it('shows supported file formats', () => {
    render(
      <FileImport isOpen={true} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    expect(screen.getByText('✓ GeoJSON (.geojson, .json)')).toBeTruthy();
    expect(screen.getByText('✓ KML (.kml)')).toBeTruthy();
  });

  it('has file select button', () => {
    render(
      <FileImport isOpen={true} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    expect(screen.getByText('📁 Select File')).toBeTruthy();
  });

  it('calls onCancel when cancel button clicked', () => {
    render(
      <FileImport isOpen={true} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('import button is disabled when no file selected', () => {
    render(
      <FileImport isOpen={true} onImport={mockOnImport} onCancel={mockOnCancel} />
    );
    
    const importButton = screen.getByText('Import Features');
    expect(importButton.disabled).toBe(true);
  });
});

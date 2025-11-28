import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ShareModal from './ShareModal';

describe('ShareModal Component', () => {
  const mockMap = {
    id: 1,
    title: 'Test Map',
    description: 'Test description',
    is_public: true
  };

  const mockOnClose = vi.fn();
  const mockOnVisibilityChange = vi.fn();

  it('renders nothing when not open', () => {
    const { container } = render(
      <ShareModal 
        map={mockMap} 
        isOpen={false} 
        onClose={mockOnClose}
        onVisibilityChange={mockOnVisibilityChange}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <ShareModal 
        map={mockMap} 
        isOpen={true} 
        onClose={mockOnClose}
        onVisibilityChange={mockOnVisibilityChange}
      />
    );
    expect(screen.getByText('Share Map')).toBeTruthy();
  });

  it('displays map title', () => {
    render(
      <ShareModal 
        map={mockMap} 
        isOpen={true} 
        onClose={mockOnClose}
        onVisibilityChange={mockOnVisibilityChange}
      />
    );
    expect(screen.getByText('Test Map')).toBeTruthy();
  });

  it('shows share link for public maps', () => {
    render(
      <ShareModal 
        map={mockMap} 
        isOpen={true} 
        onClose={mockOnClose}
        onVisibilityChange={mockOnVisibilityChange}
      />
    );
    expect(screen.getByText('Share Link')).toBeTruthy();
  });

  it('shows private notice for private maps', () => {
    const privateMap = { ...mockMap, is_public: false };
    render(
      <ShareModal 
        map={privateMap} 
        isOpen={true} 
        onClose={mockOnClose}
        onVisibilityChange={mockOnVisibilityChange}
      />
    );
    expect(screen.getByText('💡 Make this map public to generate a shareable link')).toBeTruthy();
  });
});

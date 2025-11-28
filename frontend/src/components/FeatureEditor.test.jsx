import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import FeatureEditor from './FeatureEditor';

describe('FeatureEditor Component', () => {
  const mockFeature = {
    id: 1,
    title: 'Test Feature',
    description: 'Test description',
    category: 'Test Category',
    stories: [],
    photos: []
  };

  const mockOnSave = vi.fn();
  const mockOnCancel = vi.fn();

  it('renders nothing when not open', () => {
    const { container } = render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={false}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  it('renders modal when open', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    expect(screen.getByText('Edit Feature')).toBeTruthy();
    expect(screen.getByLabelText('Title *')).toBeTruthy();
  });

  it('displays feature data in form fields', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    const titleInput = screen.getByLabelText('Title *');
    const descriptionInput = screen.getByLabelText('Description');
    const categoryInput = screen.getByLabelText('Category');
    
    expect(titleInput.value).toBe('Test Feature');
    expect(descriptionInput.value).toBe('Test description');
    expect(categoryInput.value).toBe('Test Category');
  });

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('calls onCancel when close button is clicked', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    const closeButton = screen.getByText('×');
    fireEvent.click(closeButton);
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('updates form fields when user types', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    const titleInput = screen.getByLabelText('Title *');
    fireEvent.change(titleInput, { target: { value: 'Updated Title' } });
    
    expect(titleInput.value).toBe('Updated Title');
  });

  it('shows add story button', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    expect(screen.getByText('+ Add Story')).toBeTruthy();
  });

  it('shows photo upload button', () => {
    render(
      <FeatureEditor
        feature={mockFeature}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    expect(screen.getByText('📷 Add Photos')).toBeTruthy();
  });

  it('displays existing stories', () => {
    const featureWithStories = {
      ...mockFeature,
      stories: [
        { title: 'Story 1', content: 'Content 1' },
        { title: 'Story 2', content: 'Content 2' }
      ]
    };
    
    render(
      <FeatureEditor
        feature={featureWithStories}
        isOpen={true}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );
    
    expect(screen.getByText('Story 1')).toBeTruthy();
    expect(screen.getByText('Story 2')).toBeTruthy();
  });
});

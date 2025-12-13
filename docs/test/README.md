# Testing Documentation

This directory contains testing-related documentation, troubleshooting guides, and test analysis.

## 📋 Contents

### 🔐 Permission & Security Testing
- **[Photo Upload Permission Issue](./PHOTO_UPLOAD_PERMISSION_ISSUE.md)** - Comprehensive analysis of the photo upload permission system, including:
  - Root cause analysis of permission errors
  - Database ownership verification
  - API security validation
  - Step-by-step troubleshooting guide

### 🔑 Credentials & Authentication
- **[Private Credentials](./PRIVATE_CREDENTIALS.md)** - Private credential information for testing environments

## 🧪 Related Testing Resources

### Main Testing Documentation
- [Testing Guide](../../TESTING_GUIDE.md) - Main testing documentation
- [Integration Verification](../../INTEGRATION_VERIFICATION.md) - Integration testing procedures

### Test Scripts
Located in the project root:
- `test_photo_upload.py` - Photo upload API testing
- `test_feature_integration.py` - Feature integration testing
- `test_file_import.py` - File import testing

### Frontend Tests
Located in `frontend/src/components/`:
- `*.test.jsx` files for component testing

## 🔍 Understanding Permission Issues

The photo upload permission system enforces strict ownership rules:

1. **Map Ownership**: Users can only upload photos to features on maps they own
2. **Permission Validation**: Backend validates ownership before allowing uploads
3. **Error Handling**: Clear error messages guide users to create their own maps

For detailed analysis, see [Photo Upload Permission Issue](./PHOTO_UPLOAD_PERMISSION_ISSUE.md).

## 🚀 Quick Testing Commands

```bash
# Run Django tests
python manage.py test

# Run frontend tests  
cd frontend && npm test

# Test photo upload API
python test_photo_upload.py

# Test feature integration
python test_feature_integration.py
```

## 📝 Adding New Test Documentation

When adding new test documentation:

1. **Use descriptive filenames** that clearly indicate the test purpose
2. **Include step-by-step procedures** for reproducing issues
3. **Document expected vs actual behavior**
4. **Provide clear resolution steps**
5. **Update this README** with links to new documentation
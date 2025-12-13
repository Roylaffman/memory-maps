# Link Test Document

This document tests GitHub-compatible relative links.

## Links to Test

### From docs/test/ to root files:
- [Root README](../../README.md)
- [Quick Start](../../QUICKSTART.md)
- [Testing Guide](../../TESTING_GUIDE.md)

### From docs/test/ to other docs:
- [Docs README](../README.md)
- [Photo Upload Issue](./PHOTO_UPLOAD_PERMISSION_ISSUE.md)
- [Private Credentials](./PRIVATE_CREDENTIALS.md)

### From docs/test/ to frontend:
- [Frontend README](../../frontend/README.md)
- [Backend Integration](../../frontend/BACKEND_INTEGRATION.md)

## GitHub Link Format Rules

✅ **Correct GitHub relative links:**
- `./file.md` (same directory)
- `../file.md` (parent directory)  
- `../../file.md` (two levels up)
- `./folder/file.md` (subdirectory)

❌ **Avoid these formats:**
- `/file.md` (absolute paths don't work on GitHub)
- `file.md` (without ./ can be unreliable)
- Links with spaces or special characters

## Testing Instructions

1. Push to GitHub
2. Navigate to this file on GitHub
3. Click each link to verify they work
4. Delete this file once testing is complete
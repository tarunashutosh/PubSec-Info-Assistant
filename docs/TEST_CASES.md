# Test Case Documentation

This document describes the comprehensive test cases added to the PubSec Info Assistant repository.

## New Test Data Files

The following test data files have been added to improve test coverage:

### `/tests/test_data/`
- `test_example.json` - JSON data format test file
- `test_example.tsv` - Tab-separated values test file  
- `test_example.eml` - Email (EML format) test file
- `test_example.msg` - Microsoft Outlook (MSG format) test file
- `test_example.jpg` - JPEG image test file
- `test_example.png` - PNG image test file

### `/app/backend/test_data/`
- `test_example.json` - JSON data for backend API tests
- `test_example.tsv` - TSV data for backend API tests
- `test_example.eml` - EML data for backend API tests

## Updated Functional Tests

### `tests/run_tests.py`
- Added search queries for new file types (JSON, TSV, EML, MSG)
- Updated image file search queries to match new test content
- Enhanced search query coverage for all supported file types

### `tests/debug_tests.py`
- Updated to include new file extensions in test execution
- Now tests: docx, pdf, html, jpg, png, csv, md, pptx, txt, xlsx, xml, json, tsv, eml, msg

### `scripts/functional-tests.sh`
- Updated functional test script to include new file types
- Ensures CI/CD pipeline tests all supported formats

## New Unit Test Suites

### `app/backend/testsuite.py` (Enhanced)
Added comprehensive edge case tests:
- Unicode filename support (`test_upload_file_with_unicode_name`)
- Special character tags (`test_upload_file_with_special_tags`)
- Empty tags handling (`test_upload_file_empty_tags`)
- Very long file paths (`test_upload_file_very_long_path`)
- Zero-byte files (`test_upload_file_zero_size`)
- Multiple files with same name (`test_upload_multiple_files_same_name`)
- Invalid API parameters (`test_chat_api_invalid_approach`, `test_chat_api_missing_required_fields`)
- Temperature validation (`test_chat_api_invalid_temperature`)
- Empty history handling (`test_chat_api_empty_history`)
- Very long questions (`test_chat_api_very_long_question`)
- Unsupported file types (`test_file_upload_unsupported_extension`)
- Malformed JSON requests (`test_chat_api_malformed_json`)
- New file type uploads (`test_upload_json_file`, `test_upload_tsv_file`, `test_upload_eml_file`)

### `app/backend/test_comprehensive.py` (New)
Comprehensive parameterized test suite with test classes:

#### `TestFileTypes`
- Parameterized tests for all supported file types
- Tests various content types and file extensions
- Folder path variations testing
- Tag variations and edge cases

#### `TestChatAPI`
- All approach values (1-6) testing
- Temperature range testing (0.0-2.0)
- Top-k values testing (1-20)
- Response length limits testing
- User/system persona combinations

#### `TestErrorHandling`
- Missing file upload scenarios
- Missing required parameters
- Invalid JSON requests
- Invalid parameter ranges

#### `TestBoundaryConditions`
- Large file uploads (5MB test)
- Maximum tag counts (100 tags)
- Very long conversation histories (50 turns)

#### `TestInternationalization`
- Multilingual question support (8 languages)
- Unicode filename support (7 languages)
- Character encoding validation

### `tests/test_file_coverage.py` (New)
Validation test suite to ensure:
- All test files exist and are non-empty
- Search queries exist for all file types
- File extensions match search query definitions
- New file types are properly integrated

## Test Coverage Improvements

### File Type Coverage
- **Before**: 11 file types (PDF, DOCX, XLSX, PPTX, TXT, CSV, XML, HTML, MD, JPG, PNG)
- **After**: 15 file types (added JSON, TSV, EML, MSG, updated JPG/PNG)

### Test Scenario Coverage
- **Edge Cases**: 20+ new edge case tests
- **Error Handling**: 10+ error condition tests  
- **Parameterized Tests**: 50+ parameterized test combinations
- **Internationalization**: 15+ multilingual/unicode tests
- **Boundary Conditions**: 5+ stress tests

### API Endpoint Coverage
- All chat API approaches (1-6)
- All parameter combinations
- Error conditions and validation
- File upload scenarios

## Running the Tests

### Functional Tests
```bash
make functional-tests
```

### Unit Tests
```bash
make run-backend-tests
```

### Individual Test Suites
```bash
# Original test suite
cd app/backend && pytest testsuite.py

# Comprehensive test suite  
cd app/backend && pytest test_comprehensive.py

# Coverage validation
cd tests && pytest test_file_coverage.py
```

## Benefits

1. **Comprehensive Coverage**: Tests all supported file types and edge cases
2. **Regression Prevention**: Catches breaking changes in file processing pipeline
3. **Parameter Validation**: Ensures API handles invalid inputs gracefully
4. **Internationalization**: Validates unicode and multilingual support
5. **Performance Testing**: Includes boundary condition testing
6. **Maintainability**: Parameterized tests reduce code duplication
7. **Documentation**: Self-documenting test names and structure

## Future Enhancements

1. Add more media file type tests (video/audio formats)
2. Add performance benchmarking tests
3. Add integration tests with real Azure services
4. Add accessibility testing for frontend components
5. Add security testing for file upload scenarios
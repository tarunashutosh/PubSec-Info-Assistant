# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Test script to validate that all test data files exist and have corresponding search queries
"""
import os
import pytest
from run_tests import search_queries, get_files_by_extension

def test_all_test_files_exist():
    """Verify that all expected test files exist in test_data directory"""
    test_data_dir = "./test_data"
    expected_extensions = list(search_queries.keys())
    
    for extension in expected_extensions:
        expected_file = f"test_example.{extension}"
        file_path = os.path.join(test_data_dir, expected_file)
        assert os.path.exists(file_path), f"Test file {expected_file} does not exist"
        assert os.path.getsize(file_path) > 0, f"Test file {expected_file} is empty"

def test_all_search_queries_have_content():
    """Verify that all search queries have meaningful content"""
    for extension, query in search_queries.items():
        assert query.strip(), f"Search query for {extension} is empty"
        assert len(query) > 10, f"Search query for {extension} is too short: {query}"

def test_search_queries_match_file_extensions():
    """Verify that search queries exist for all supported file extensions"""
    test_data_dir = "./test_data"
    if os.path.exists(test_data_dir):
        test_files = [f for f in os.listdir(test_data_dir) if f.startswith("test_example.")]
        extensions_with_files = {f.split(".")[-1] for f in test_files}
        
        for ext in extensions_with_files:
            assert ext in search_queries, f"No search query defined for extension {ext}"

def test_get_files_by_extension_function():
    """Test the get_files_by_extension utility function"""
    test_data_dir = "./test_data"
    if os.path.exists(test_data_dir):
        # Test with specific extensions
        test_extensions = ["pdf", "docx", "json", "csv"]
        files = get_files_by_extension(test_data_dir, test_extensions)
        
        for file in files:
            assert any(file.endswith(f".{ext}") for ext in test_extensions)
            assert file.startswith("test_example.")

def test_new_file_types_added():
    """Verify that new file types have been added to test suite"""
    new_extensions = ["json", "tsv", "eml", "msg"]
    
    for ext in new_extensions:
        assert ext in search_queries, f"New file type {ext} missing from search queries"
        
        test_file = f"./test_data/test_example.{ext}"
        assert os.path.exists(test_file), f"Test file for new type {ext} does not exist"

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
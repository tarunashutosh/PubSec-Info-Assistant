# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Comprehensive test suite with parameterized tests for file processing and API endpoints
"""
import pytest
import json
import io
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv

dir = current_working_directory = os.getcwd()
# We're running from MAKE file, so we need to change directory to app/backend
if ("/app/backend" not in dir):
    os.chdir(f'{dir}/app/backend')

load_dotenv(dotenv_path=f'../../scripts/environments/infrastructure.debug.env')

from app import app
client = TestClient(app)

class TestFileTypes:
    """Test class for different file type upload scenarios"""
    
    @pytest.mark.parametrize("file_name,content_type,expected_status", [
        ("test.pdf", "application/pdf", 200),
        ("test.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 200),
        ("test.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 200),
        ("test.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation", 200),
        ("test.txt", "text/plain", 200),
        ("test.csv", "text/csv", 200),
        ("test.json", "application/json", 200),
        ("test.xml", "application/xml", 200),
        ("test.html", "text/html", 200),
        ("test.md", "text/markdown", 200),
        ("test.tsv", "text/tab-separated-values", 200),
        ("test.eml", "message/rfc822", 200),
        ("test.msg", "application/vnd.ms-outlook", 200),
        ("test.jpg", "image/jpeg", 200),
        ("test.png", "image/png", 200),
    ])
    def test_file_upload_by_type(self, file_name, content_type, expected_status):
        """Test file upload for different supported file types"""
        # Create dummy file content
        if file_name.endswith(('.jpg', '.png')):
            file_content = b'\x89PNG\r\n\x1a\n' + b'dummy image data'
        elif file_name.endswith('.json'):
            file_content = b'{"test": "data"}'
        elif file_name.endswith('.csv'):
            file_content = b'name,value\ntest,123'
        elif file_name.endswith('.tsv'):
            file_content = b'name\tvalue\ntest\t123'
        else:
            file_content = b'test file content for ' + file_name.encode()
            
        file = io.BytesIO(file_content)
        file.name = file_name
        
        response = client.post(
            "/file",
            files={"file": (file_name, file, content_type)},
            data={"file_path": file_name, "tags": "test,parameterized"}
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize("folder_path", [
        "simple_folder",
        "folder/subfolder",
        "deep/nested/folder/structure",
        "folder-with-dashes",
        "folder_with_underscores",
        "folder.with.dots",
        "123_numeric_folder",
    ])
    def test_file_upload_folder_paths(self, folder_path):
        """Test file uploads to different folder structures"""
        file_content = b'test content'
        file = io.BytesIO(file_content)
        file_name = "test.txt"
        full_path = f"{folder_path}/{file_name}"
        
        response = client.post(
            "/file",
            files={"file": (file_name, file, "text/plain")},
            data={"file_path": full_path, "tags": "test,folder"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": f"File '{file_name}' uploaded successfully"}

    @pytest.mark.parametrize("tags", [
        "single_tag",
        "tag1,tag2,tag3",
        "tag-with-dashes,tag_with_underscores",
        "tag.with.dots,tag@special,tag#hash",
        "very,long,list,of,many,different,tags,for,testing,purposes",
        "",  # Empty tags
        "   spaced_tag   ,  another_spaced_tag  ",  # Tags with spaces
    ])
    def test_file_upload_tag_variations(self, tags):
        """Test file uploads with different tag variations"""
        file_content = b'test content'
        file = io.BytesIO(file_content)
        file_name = "test.txt"
        
        response = client.post(
            "/file",
            files={"file": (file_name, file, "text/plain")},
            data={"file_path": file_name, "tags": tags}
        )
        assert response.status_code == 200

class TestChatAPI:
    """Test class for chat API with different parameter combinations"""
    
    @pytest.mark.parametrize("approach", [1, 2, 3, 4, 5, 6])
    def test_chat_api_approaches(self, approach):
        """Test chat API with different approach values"""
        response = client.post("/chat", json={
            "history":[{"user":"What is artificial intelligence?"}],
            "approach": approach,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

    @pytest.mark.parametrize("temp", [0.0, 0.3, 0.6, 0.9, 1.0, 1.5, 2.0])
    def test_chat_api_temperature_values(self, temp):
        """Test chat API with different temperature values"""
        response = client.post("/chat", json={
            "history":[{"user":"What is machine learning?"}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":temp,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

    @pytest.mark.parametrize("top_k", [1, 3, 5, 10, 20])
    def test_chat_api_top_k_values(self, top_k):
        """Test chat API with different top-k values"""
        response = client.post("/chat", json={
            "history":[{"user":"Explain data science"}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":top_k,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

    @pytest.mark.parametrize("response_length", [512, 1024, 2048, 4096])
    def test_chat_api_response_lengths(self, response_length):
        """Test chat API with different response length limits"""
        response = client.post("/chat", json={
            "history":[{"user":"Tell me about cloud computing"}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":response_length,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

    @pytest.mark.parametrize("user_persona,system_persona", [
        ("analyst", "an Assistant"),
        ("researcher", "a Research Assistant"),
        ("student", "a Tutor"),
        ("manager", "a Business Consultant"),
        ("developer", "a Technical Expert"),
    ])
    def test_chat_api_persona_combinations(self, user_persona, system_persona):
        """Test chat API with different persona combinations"""
        response = client.post("/chat", json={
            "history":[{"user":"What are best practices?"}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":user_persona,
                "system_persona":system_persona,
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

class TestErrorHandling:
    """Test class for error handling scenarios"""
    
    def test_file_upload_no_file(self):
        """Test file upload endpoint without providing a file"""
        response = client.post(
            "/file",
            data={"file_path": "test.txt", "tags": "test"}
        )
        assert response.status_code == 422

    def test_file_upload_no_path(self):
        """Test file upload endpoint without providing file_path"""
        file_content = b'test content'
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/file",
            files={"file": ("test.txt", file, "text/plain")},
            data={"tags": "test"}
        )
        assert response.status_code == 422

    def test_chat_api_no_history(self):
        """Test chat API without history"""
        response = client.post("/chat", json={
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code in [400, 422]

    def test_chat_api_invalid_json(self):
        """Test chat API with invalid JSON"""
        response = client.post("/chat", 
                              data="invalid json",
                              headers={"Content-Type": "application/json"})
        assert response.status_code == 422

    @pytest.mark.parametrize("invalid_temp", [-1.0, 3.0, "invalid", None])
    def test_chat_api_invalid_temperature(self, invalid_temp):
        """Test chat API with invalid temperature values"""
        response = client.post("/chat", json={
            "history":[{"user":"test"}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":invalid_temp,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code in [200, 400, 422]  # May handle gracefully

class TestBoundaryConditions:
    """Test class for boundary conditions and edge cases"""
    
    def test_upload_max_size_file(self):
        """Test uploading maximum allowed file size"""
        # Create a large file (but not too large to avoid timeout)
        file_content = b"a" * (5 * 1024 * 1024)  # 5 MB
        file = io.BytesIO(file_content)
        file.name = "large_file.txt"
        
        response = client.post(
            "/file",
            files={"file": (file.name, file, "text/plain")},
            data={"file_path": "large_file.txt", "tags": "test,large"}
        )
        assert response.status_code in [200, 413]  # Success or payload too large

    def test_upload_file_max_tags(self):
        """Test uploading file with maximum number of tags"""
        tags = ",".join([f"tag{i}" for i in range(100)])  # 100 tags
        file_content = b'test content'
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/file",
            files={"file": ("test.txt", file, "text/plain")},
            data={"file_path": "test.txt", "tags": tags}
        )
        assert response.status_code == 200

    def test_chat_api_max_history_length(self):
        """Test chat API with very long conversation history"""
        long_history = []
        for i in range(50):  # 50 turns of conversation
            long_history.extend([
                {"user": f"Question {i}: What is topic {i}?"},
                {"bot": f"Answer {i}: This is the response about topic {i}."}
            ])
        long_history.append({"user": "Final question"})
        
        response = client.post("/chat", json={
            "history": long_history,
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code in [200, 413, 422]  # Success or payload too large

class TestInternationalization:
    """Test class for internationalization and unicode support"""
    
    @pytest.mark.parametrize("question", [
        "What is artificial intelligence?",  # English
        "¿Qué es la inteligencia artificial?",  # Spanish
        "Qu'est-ce que l'intelligence artificielle?",  # French
        "Was ist künstliche Intelligenz?",  # German
        "人工知能とは何ですか？",  # Japanese
        "什么是人工智能？",  # Chinese
        "Что такое искусственный интеллект?",  # Russian
        "인공지능이 무엇인가요?",  # Korean
    ])
    def test_chat_api_multilingual_questions(self, question):
        """Test chat API with questions in different languages"""
        response = client.post("/chat", json={
            "history":[{"user": question}],
            "approach":1,
            "overrides":{
                "semantic_ranker":True,
                "semantic_captions":False,
                "top":5,
                "suggest_followup_questions":False,
                "user_persona":"analyst",
                "system_persona":"an Assistant",
                "ai_persona":"",
                "response_length":2048,
                "response_temp":0.6,
                "selected_folders":"All",
                "selected_tags":""},
            "citation_lookup":{},
            "thought_chain":{}})
        assert response.status_code == 200

    @pytest.mark.parametrize("filename", [
        "file_测试.txt",  # Chinese
        "archivo_prueba.txt",  # Spanish
        "fichier_test.txt",  # French
        "datei_test.txt",  # German
        "ファイル_テスト.txt",  # Japanese
        "파일_테스트.txt",  # Korean
        "файл_тест.txt",  # Russian
    ])
    def test_file_upload_unicode_names(self, filename):
        """Test file upload with unicode filenames"""
        file_content = b'test content with unicode filename'
        file = io.BytesIO(file_content)
        
        response = client.post(
            "/file",
            files={"file": (filename, file, "text/plain")},
            data={"file_path": filename, "tags": "unicode,test"}
        )
        assert response.status_code == 200
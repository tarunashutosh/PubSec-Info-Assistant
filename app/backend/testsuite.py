import json
import re
import pytest
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import io

dir = current_working_directory = os.getcwd()
# We're running from MAKE file, so we need to change directory to app/backend
if ("/app/backend" not in dir):
    os.chdir(f'{dir}/app/backend')

load_dotenv(dotenv_path=f'../../scripts/environments/infrastructure.debug.env')

azure_credentials = DefaultAzureCredential()

from app import app
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

# Web API Validation for Microsoft CEO
def test_web_chat_api():
    response = client.post("/chat", json={
        "history":[{"user":"Who is the CEO of Microsoft?"}],
        "approach":4,
        "overrides":{
            "semantic_ranker": True,
            "semantic_captions": False,
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
    content = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    assert "Satya" in content
    
# Work API Validation for Microsoft CEO
def test_work_chat_api():
    response = client.post("/chat", json={
        "history":[{"user":"who is the CEO of Microsoft?"}],
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
    content = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    assert "Satya" in content or "I am not sure." in content

# Search work, then compare with web API Validation for Microsoft CEO
def test_web_compare_work_chat_api():
    response = client.post("/chat", json={
        "history":[{"user":"who is the CEO of Microsoft?"}],
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
    content = ""
    work_citation_lookup = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "work_citation_lookup" in eventJson and eventJson["work_citation_lookup"] != None:
            work_citation_lookup = eventJson["work_citation_lookup"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    payload = {"history":[{"user":"who is the CEO of Microsoft?",
                 "bot":content},
                {"user":"who is the CEO of Microsoft?"}],
     "approach":5,
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
     "citation_lookup": work_citation_lookup,
     "thought_chain":{"work_response": content}
     }
    
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    content = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    assert "Satya" in content or "I am not sure." in content


# Search web, then compare with work API Validation for Microsoft CEO
def test_work_compare_web_chat_api():
    response = client.post("/chat", json={
        "history":[{"user":"who is the CEO of Microsoft?"}],
        "approach":4,
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
    content = ""
    web_citation_lookup = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "web_citation_lookup" in eventJson and eventJson["web_citation_lookup"] != None:
            web_citation_lookup = eventJson["web_citation_lookup"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    payload = {"history":[{"user":"who is the CEO of Microsoft?",
                 "bot":content},
                {"user":"who is the CEO of Microsoft?"}],
     "approach":6,
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
     "citation_lookup": web_citation_lookup,
     "thought_chain":{"web_response": content}
     }
    
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    content = ""
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "error" in eventJson and eventJson["error"] != None:
            content += eventJson["error"]
            
    assert "Satya" in content or "I am not sure." in content


def test_get_blob_client():
    response = client.get("/getblobclient")
    assert response.status_code == 200
    assert "blob.core.windows.net" in response.json()["client"].url

def test_get_all_upload_status():
    response = client.post("/getalluploadstatus", json={
        "timeframe":4,
        "state":"ALL",
        "folder":"Root",
        "tag":"All"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_folders():
    response = client.post("/getfolders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tags():
    response = client.post("/gettags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    

def test_get_hint():
    
    response = client.get("/getHint", params={"question": "What is 2+2?"})
    assert response.status_code == 200
    assert "add" in response.json().lower() or "addition" in response.json().lower()


def test_post_td():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post("/posttd", files={"csv": file})
        assert response.status_code == 200

def test_process_td_agent_response():
    response = client.get("/process_td_agent_response", params={"question": "How many rows are there in this file?"})
    assert response.status_code == 200
    assert "200" in response.json()

def test_process_agent_response():
    response = client.get("/process_agent_response", params={"question": "What is 2+2?"})
    assert response.status_code == 200
    assert "4" in response.json()

def test_get_info_data():
    response = client.get("/getInfoData")
    assert response.status_code == 200
    expected_response = {
        "AZURE_OPENAI_CHATGPT_DEPLOYMENT": "deployment_value",
        "AZURE_OPENAI_MODEL_NAME": "model_name_value",
        "AZURE_OPENAI_MODEL_VERSION": "model_version_value",
        "AZURE_OPENAI_SERVICE": "openai_service_value",
        "AZURE_SEARCH_SERVICE": "search_service_value",
        "AZURE_SEARCH_INDEX": "search_index_value",
        "TARGET_LANGUAGE": "en",
        "USE_AZURE_OPENAI_EMBEDDINGS": "true",
        "EMBEDDINGS_DEPLOYMENT": "embedding_deployment_value",
        "EMBEDDINGS_MODEL_NAME": "embedding_model_name_value",
        "EMBEDDINGS_MODEL_VERSION": "embedding_model_version_value",
    }
    assert response.json().keys() == expected_response.keys()
    

def test_get_warning_banner():
    response = client.get("/getWarningBanner")
    assert response.status_code == 200
    assert response.json() == {"WARNING_BANNER_TEXT": os.getenv("CHAT_WARNING_BANNER_TEXT")}

def test_get_max_csv_file_size():
    response = client.get("/getMaxCSVFileSize")
    assert response.status_code == 200
    assert response.json() == {"MAX_CSV_FILE_SIZE": os.getenv("MAX_CSV_FILE_SIZE")}

def test_get_application_title():
    response = client.get("/getApplicationTitle")
    assert response.status_code == 200
    assert response.json() == {"APPLICATION_TITLE": os.getenv("APPLICATION_TITLE")}

def test_get_all_tags():
    response = client.get("/getalltags")
    assert response.status_code == 200
    assert isinstance(response.json(), str)

def test_get_feature_flags():
    response = client.get("/getFeatureFlags")
    assert response.status_code == 200
    
    expected_response = {
        "ENABLE_WEB_CHAT": os.getenv("ENABLE_WEB_CHAT") == "true",
        "ENABLE_UNGROUNDED_CHAT": os.getenv("ENABLE_UNGROUNDED_CHAT") == "true",
        "ENABLE_MATH_ASSISTANT": os.getenv("ENABLE_MATH_ASSISTANT") == "true",
        "ENABLE_TABULAR_DATA_ASSISTANT": os.getenv("ENABLE_TABULAR_DATA_ASSISTANT") == "true",
    }

    assert response.json() == expected_response

def test_upload_blob():
    storage_account_url=os.getenv("BLOB_STORAGE_ACCOUNT_ENDPOINT")
    container_name = os.getenv("AZURE_BLOB_STORAGE_UPLOAD_CONTAINER")
    blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=azure_credentials)

    # Create a container client
    container_client = blob_service_client.get_container_client(container_name)

    # Path to the local file you want to upload
    local_file_path = "test_data/parts_inventory.csv"
    blob_name = "parts_inventory.csv"

    # Create a BlobClient
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the file
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        
    return blob_name 

def test_log_status():
    response = client.post("/logstatus", json={
        "path": "upload/parts_inventory.csv",
        "status": "File uploaded from test suite to Azure Blob Storage",
        "status_classification": "Info",
        "state": "Uploaded"
    })
    assert response.status_code == 200
    
def test_resubmit_item():
    response = client.post("/resubmitItems", json={"path": "/parts_inventory.csv"})
    assert response.status_code == 200
    assert response.json() == True

def test_delete_item():
    response = client.post("/deleteItems", json={"path": "/parts_inventory.csv"})
    assert response.status_code == 200
    assert response.json() == True  
  
def test_get_file():  
    blob_name = test_upload_blob()
      
    try:  
        file_path = blob_name  
        response = client.post("/get-file", json={"path": file_path})  
          
        assert response.status_code == 200  
        assert response.headers["Content-Disposition"] == f"inline; filename=parts_inventory.csv"  
        assert "text/csv" in response.headers["Content-Type"]  
    finally:  
        test_delete_item() 
    assert response.json() == True

def test_upload_file_one_tag():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": "test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}


def test_uploadfilenotagsnofolder():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": ""}
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_uploadfiletags():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": "test,inventory"}
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}
def test_uploadfilespecificfolder():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "Finance/parts_inventory.csv", "tags": "test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}
def test_uploadfilespecificfoldernested():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "Finance/new/parts_inventory.csv", "tags": "test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_upload_file_no_file():
    response = client.post(
        "/file",
        data={"file_path": "parts_inventory.csv", "tags": "test"}
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_upload_file_large_file():
    file_content = b"a" * (10 * 1024 * 1024)  # 10 MB file
    file = io.BytesIO(file_content)
    file.name = "large_parts_inventory.csv"
    
    response = client.post(
        "/file",
        files={"file": (file.name, file, "text/csv")},
        data={"file_path": "large_parts_inventory.csv", "tags": "test"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "File 'large_parts_inventory.csv' uploaded successfully"}

def test_upload_file_missing_file_path():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"tags": "test"}
        )
        assert response.status_code == 422  # Unprocessable Entity
def test_upload_file_special_characters_in_file_path():
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "Finance/@new/parts_inventory.csv", "tags": "test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_upload_file_long_tags():
    with open("test_data/parts_inventory.csv", "rb") as file:
        long_tags = ",".join(["tag"] * 1000)  # Very long tags string
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": long_tags}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}
# This test requires some amount of data to be present and processed in IA
# It is commented out because processing the data takes time and the test will fail if the data is not processed
# Change the question to a valid question that will produce citations if you want to run this test
"""
def test_get_citation_obj():
    question = "Who is the CEO of Microsoft?"
    response = client.post("/chat", json={
        "history":[{"user": question}],
        "approach":1,
        "overrides":{
            "semantic_ranker": True,
            "semantic_captions": False,
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
    content = ""
    work_citation_lookup = {}
    for line in response.iter_lines():
        eventJson = json.loads(line)
        if "content" in eventJson and eventJson["content"] != None:
            content += eventJson["content"]
        elif "work_citation_lookup" in eventJson and eventJson["work_citation_lookup"] != None:
            work_citation_lookup = eventJson["work_citation_lookup"]
            
    # Define the regex pattern
    pattern = r'\\[(File[0-9])\\]'
    
    # Search for the first match
    match = re.search(pattern, content)
    
    # If a match is found, make a call to get citation object
    if match:
        response = client.post("/getcitation", json={"citation": work_citation_lookup[match.group(1)]})
        assert response.status_code == 200
    else:
        pytest.fail("No citation was found in work response. Unable to make a call to get citation object.")
"""

# Additional comprehensive test cases for file uploads and edge cases

def test_upload_json_file():
    """Test uploading JSON file"""
    with open("test_data/test_example.json", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("test_example.json", file, "application/json")},
            data={"file_path": "test_example.json", "tags": "json,test,data"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'test_example.json' uploaded successfully"}

def test_upload_tsv_file():
    """Test uploading TSV file"""
    with open("test_data/test_example.tsv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("test_example.tsv", file, "text/tab-separated-values")},
            data={"file_path": "test_example.tsv", "tags": "tsv,test,data"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'test_example.tsv' uploaded successfully"}

def test_upload_eml_file():
    """Test uploading EML email file"""
    with open("test_data/test_example.eml", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("test_example.eml", file, "message/rfc822")},
            data={"file_path": "test_example.eml", "tags": "eml,email,test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'test_example.eml' uploaded successfully"}

def test_upload_file_with_unicode_name():
    """Test uploading file with unicode characters in name"""
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("测试文件_parts_inventory.csv", file, "text/csv")},
            data={"file_path": "测试文件_parts_inventory.csv", "tags": "unicode,test"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File '测试文件_parts_inventory.csv' uploaded successfully"}

def test_upload_file_with_special_tags():
    """Test uploading file with special characters in tags"""
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": "test-tag,tag_with_underscore,tag.with.dots,tag@special"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_upload_file_empty_tags():
    """Test uploading file with empty tags string"""
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": "parts_inventory.csv", "tags": ""}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_upload_file_very_long_path():
    """Test uploading file with very long folder path"""
    long_path = "a" * 50 + "/" + "b" * 50 + "/" + "c" * 50 + "/parts_inventory.csv"
    with open("test_data/parts_inventory.csv", "rb") as file:
        response = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file, "text/csv")},
            data={"file_path": long_path, "tags": "test,long_path"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "File 'parts_inventory.csv' uploaded successfully"}

def test_upload_file_zero_size():
    """Test uploading zero-byte file"""
    file_content = b""
    file = io.BytesIO(file_content)
    file.name = "empty.txt"
    
    response = client.post(
        "/file",
        files={"file": (file.name, file, "text/plain")},
        data={"file_path": "empty.txt", "tags": "test,empty"}
    )
    # Should handle empty files gracefully
    assert response.status_code == 200
    assert response.json() == {"message": "File 'empty.txt' uploaded successfully"}

def test_upload_multiple_files_same_name():
    """Test uploading multiple files with same name to different folders"""
    with open("test_data/parts_inventory.csv", "rb") as file1:
        response1 = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file1, "text/csv")},
            data={"file_path": "folder1/parts_inventory.csv", "tags": "test,folder1"}
        )
        assert response1.status_code == 200

    with open("test_data/parts_inventory.csv", "rb") as file2:
        response2 = client.post(
            "/file",
            files={"file": ("parts_inventory.csv", file2, "text/csv")},
            data={"file_path": "folder2/parts_inventory.csv", "tags": "test,folder2"}
        )
        assert response2.status_code == 200

def test_chat_api_invalid_approach():
    """Test chat API with invalid approach number"""
    response = client.post("/chat", json={
        "history":[{"user":"test question"}],
        "approach":999,  # Invalid approach
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
    # Should handle invalid approach gracefully
    assert response.status_code in [200, 400, 422]

def test_chat_api_missing_required_fields():
    """Test chat API with missing required fields"""
    response = client.post("/chat", json={
        "history":[{"user":"test question"}]
        # Missing approach, overrides, etc.
    })
    assert response.status_code in [400, 422]

def test_chat_api_invalid_temperature():
    """Test chat API with invalid temperature values"""
    response = client.post("/chat", json={
        "history":[{"user":"test question"}],
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
            "response_temp":2.5,  # Invalid temperature > 2.0
            "selected_folders":"All",
            "selected_tags":""},
        "citation_lookup":{},
        "thought_chain":{}})
    assert response.status_code in [200, 400, 422]

def test_chat_api_empty_history():
    """Test chat API with empty history"""
    response = client.post("/chat", json={
        "history":[],  # Empty history
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
    assert response.status_code in [200, 400, 422]

def test_chat_api_very_long_question():
    """Test chat API with extremely long question"""
    long_question = "A" * 10000  # Very long question
    response = client.post("/chat", json={
        "history":[{"user": long_question}],
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
    # Should handle very long questions
    assert response.status_code in [200, 400, 413, 422]

def test_file_upload_unsupported_extension():
    """Test uploading file with unsupported extension"""
    file_content = b"test content"
    file = io.BytesIO(file_content)
    file.name = "test.unknown_extension"
    
    response = client.post(
        "/file",
        files={"file": (file.name, file, "application/octet-stream")},
        data={"file_path": "test.unknown_extension", "tags": "test"}
    )
    # Should either accept or reject gracefully
    assert response.status_code in [200, 400, 415, 422]

def test_chat_api_malformed_json():
    """Test chat API with malformed JSON in citation_lookup"""
    response = client.post("/chat", json={
        "history":[{"user":"test question"}],
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
        "citation_lookup":"invalid_json_string",  # Should be dict
        "thought_chain":{}})
    assert response.status_code in [200, 400, 422]
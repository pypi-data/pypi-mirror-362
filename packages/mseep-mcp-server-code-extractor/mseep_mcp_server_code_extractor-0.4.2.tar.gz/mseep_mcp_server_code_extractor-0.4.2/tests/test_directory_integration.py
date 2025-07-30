"""
Integration tests for directory search functionality.

Tests real directory structures, cross-file pattern detection,
and end-to-end directory search workflows.
"""

import pytest
import tempfile
import os
from pathlib import Path
from typing import List, Dict

from code_extractor.search_engine import SearchEngine
from code_extractor.models import SearchParameters, SearchResult


class TestDirectoryIntegration:
    """Integration tests with real directory structures."""
    
    def setup_method(self):
        """Set up test environment."""
        self.engine = SearchEngine()
    
    @pytest.fixture
    def python_project_structure(self, tmp_path):
        """Create a realistic Python project structure."""
        # Main source files
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        (src_dir / "__init__.py").write_text("")
        
        (src_dir / "main.py").write_text("""
#!/usr/bin/env python3
import sys
from utils import get_file_content, process_data
from models import User, Database

def main():
    config = get_file_content("config.json")
    db = Database(config)
    user = User.create_from_dict(config["user"])
    
    result = process_data(user.data)
    print(f"Processed: {result}")
    return result

if __name__ == "__main__":
    main()
""")
        
        (src_dir / "utils.py").write_text("""
import json
import os
from typing import Dict, Any

def get_file_content(filename: str) -> str:
    '''Read file content safely.'''
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return ""

def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    '''Process user data.'''
    processed = {}
    for key, value in data.items():
        if isinstance(value, str):
            processed[key] = value.upper()
        else:
            processed[key] = value
    return processed

def save_to_file(data: Dict[str, Any], filename: str) -> bool:
    '''Save data to file.'''
    try:
        content = json.dumps(data, indent=2)
        with open(filename, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False
""")
        
        (src_dir / "models.py").write_text("""
from typing import Dict, Any, Optional
from utils import get_file_content

class Database:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
    
    def connect(self) -> bool:
        '''Establish database connection.'''
        return True
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        '''Execute SQL query.'''
        return []

class User:
    def __init__(self, name: str, email: str, data: Dict[str, Any]):
        self.name = name
        self.email = email
        self.data = data
    
    @classmethod
    def create_from_dict(cls, user_dict: Dict[str, Any]) -> 'User':
        '''Create user from dictionary.'''
        return cls(
            name=user_dict.get('name', ''),
            email=user_dict.get('email', ''),
            data=user_dict.get('data', {})
        )
    
    @classmethod
    def load_from_file(cls, filename: str) -> Optional['User']:
        '''Load user from JSON file.'''
        content = get_file_content(filename)
        if content:
            import json
            user_dict = json.loads(content)
            return cls.create_from_dict(user_dict)
        return None
    
    def save_to_file(self, filename: str) -> bool:
        '''Save user to JSON file.'''
        from utils import save_to_file
        user_dict = {
            'name': self.name,
            'email': self.email,
            'data': self.data
        }
        return save_to_file(user_dict, filename)
""")
        
        # Test files
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        (tests_dir / "__init__.py").write_text("")
        
        (tests_dir / "test_utils.py").write_text("""
import pytest
from src.utils import get_file_content, process_data, save_to_file

def test_get_file_content():
    '''Test file content reading.'''
    content = get_file_content("nonexistent.txt")
    assert content == ""

def test_process_data():
    '''Test data processing.'''
    data = {"name": "john", "age": 30}
    result = process_data(data)
    assert result["name"] == "JOHN"
    assert result["age"] == 30

def test_save_to_file(tmp_path):
    '''Test file saving.'''
    data = {"test": "data"}
    filename = tmp_path / "test.json"
    result = save_to_file(data, str(filename))
    assert result == True
""")
        
        (tests_dir / "test_models.py").write_text("""
import pytest
from src.models import User, Database

def test_user_creation():
    '''Test user creation.'''
    user_dict = {"name": "Alice", "email": "alice@test.com", "data": {}}
    user = User.create_from_dict(user_dict)
    assert user.name == "Alice"
    assert user.email == "alice@test.com"

def test_user_file_operations(tmp_path):
    '''Test user file save/load.'''
    user = User("Bob", "bob@test.com", {"role": "admin"})
    filename = tmp_path / "user.json"
    
    # Test save
    result = user.save_to_file(str(filename))
    assert result == True
    
    # Test load
    loaded_user = User.load_from_file(str(filename))
    assert loaded_user is not None
    assert loaded_user.name == "Bob"
""")
        
        # Config and docs
        (tmp_path / "config.json").write_text('{"user": {"name": "test"}, "database": {"url": "sqlite:///test.db"}}')
        (tmp_path / "README.md").write_text("# Test Project\n\nA sample Python project for testing.")
        (tmp_path / "requirements.txt").write_text("pytest>=6.0.0\ntyping-extensions>=3.7.0")
        
        return tmp_path
    
    @pytest.fixture
    def mixed_language_structure(self, tmp_path):
        """Create a mixed-language project structure."""
        # Python backend
        api_dir = tmp_path / "api"
        api_dir.mkdir()
        
        (api_dir / "app.py").write_text("""
from flask import Flask, request, jsonify
from utils import get_file_content, validate_data

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    config = get_file_content('config.json')
    return jsonify({"status": "ok", "config": config})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if validate_data(request.json):
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400
""")
        
        # JavaScript frontend
        frontend_dir = tmp_path / "frontend"
        frontend_dir.mkdir()
        
        (frontend_dir / "app.js").write_text("""
import { fetchData, validateData } from './utils.js';

class App {
    constructor() {
        this.data = null;
    }
    
    async loadData() {
        try {
            const response = await fetchData('/api/data');
            this.data = response.data;
            return this.data;
        } catch (error) {
            console.error('Error loading data:', error);
            return null;
        }
    }
    
    validateInput(input) {
        return validateData(input);
    }
}

export default App;
""")
        
        (frontend_dir / "utils.js").write_text("""
export async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

export function validateData(data) {
    if (!data || typeof data !== 'object') {
        return false;
    }
    return Object.keys(data).length > 0;
}

export function processResponse(response) {
    if (validateData(response)) {
        return response;
    }
    throw new Error('Invalid response data');
}
""")
        
        # TypeScript components
        components_dir = frontend_dir / "components"
        components_dir.mkdir()
        
        (components_dir / "DataComponent.ts").write_text("""
import { fetchData, validateData } from '../utils.js';

interface DataItem {
    id: number;
    name: string;
    value: any;
}

export class DataComponent {
    private items: DataItem[] = [];
    
    async loadItems(): Promise<DataItem[]> {
        try {
            const data = await fetchData('/api/items');
            if (validateData(data)) {
                this.items = data.items;
                return this.items;
            }
            throw new Error('Invalid data received');
        } catch (error) {
            console.error('Failed to load items:', error);
            return [];
        }
    }
    
    validateItem(item: DataItem): boolean {
        return validateData(item) && 
               typeof item.id === 'number' && 
               typeof item.name === 'string';
    }
}
""")
        
        return tmp_path
    
    def test_python_project_get_file_content_search(self, python_project_structure):
        """Test searching for get_file_content calls across Python project."""
        params = SearchParameters(
            search_type="function-calls",
            target="get_file_content",
            scope=str(python_project_structure),
            file_patterns=["*.py"]
        )
        
        results = self.engine.search_directory(str(python_project_structure), params)
        
        # Should find calls in main.py, models.py, and test files
        assert len(results) >= 3
        
        # Check that we found calls in expected files
        file_names = {os.path.basename(r.file_path) for r in results}
        assert "main.py" in file_names
        assert "models.py" in file_names
        assert "test_utils.py" in file_names
        
        # Verify match content
        for result in results:
            assert "get_file_content" in result.match_text
            assert result.language == "python"
    
    def test_python_project_class_method_search(self, python_project_structure):
        """Test searching for class method calls."""
        params = SearchParameters(
            search_type="function-calls",
            target="create_from_dict",
            scope=str(python_project_structure),
            file_patterns=["*.py"]
        )
        
        results = self.engine.search_directory(str(python_project_structure), params)
        
        # Should find calls in main.py and test_models.py
        assert len(results) >= 2
        
        file_names = {os.path.basename(r.file_path) for r in results}
        assert "main.py" in file_names
        assert "test_models.py" in file_names
    
    def test_mixed_language_validate_data_search(self, mixed_language_structure):
        """Test searching across multiple languages for validation function calls."""
        # Search for validate_data (Python snake_case) 
        params = SearchParameters(
            search_type="function-calls",
            target="validate_data",
            scope=str(mixed_language_structure),
            file_patterns=["*.py"]
        )
        
        python_results = self.engine.search_directory(str(mixed_language_structure), params)
        
        # Search for validateData (JavaScript/TypeScript camelCase)
        params.target = "validateData"
        params.file_patterns = ["*.js", "*.ts"]
        
        js_ts_results = self.engine.search_directory(str(mixed_language_structure), params)
        
        # Should find calls in both Python and JavaScript/TypeScript files
        assert len(python_results) >= 1, f"Expected Python results, got {len(python_results)}"
        assert len(js_ts_results) >= 2, f"Expected JS/TS results, got {len(js_ts_results)}"
        
        # Check languages detected
        python_languages = {r.language for r in python_results}
        js_ts_languages = {r.language for r in js_ts_results}
        
        assert "python" in python_languages
        assert {"javascript", "typescript"}.intersection(js_ts_languages), f"Expected JS/TS, got {js_ts_languages}"
    
    def test_mixed_language_fetch_data_search(self, mixed_language_structure):
        """Test searching for fetchData calls in frontend code."""
        params = SearchParameters(
            search_type="function-calls",
            target="fetchData",
            scope=str(mixed_language_structure),
            file_patterns=["*.js", "*.ts"]
        )
        
        results = self.engine.search_directory(str(mixed_language_structure), params)
        
        # Should find calls in JavaScript and TypeScript files
        assert len(results) >= 2
        
        file_names = {os.path.basename(r.file_path) for r in results}
        assert "app.js" in file_names
        assert "DataComponent.ts" in file_names
    
    def test_nested_directory_search(self, mixed_language_structure):
        """Test search in nested directory structures."""
        params = SearchParameters(
            search_type="function-calls",
            target="validateData",
            scope=str(mixed_language_structure / "frontend"),
            file_patterns=["*.js", "*.ts"]
        )
        
        results = self.engine.search_directory(str(mixed_language_structure / "frontend"), params)
        
        # Should find calls in nested components directory
        assert len(results) >= 3
        
        # Check that nested files are found
        relative_paths = {
            str(Path(r.file_path).relative_to(mixed_language_structure / "frontend"))
            for r in results
        }
        assert any("components" in path for path in relative_paths)
    
    def test_file_exclusion_patterns(self, python_project_structure):
        """Test excluding test files from search."""
        params = SearchParameters(
            search_type="function-calls",
            target="get_file_content",
            scope=str(python_project_structure),
            file_patterns=["*.py"],
            exclude_patterns=["test_*", "tests/*"]
        )
        
        results = self.engine.search_directory(str(python_project_structure), params)
        
        # Should exclude test files
        file_paths = {r.file_path for r in results}
        # Check only the filename, not the full path (to avoid false positives from temp directory names)
        file_names = {os.path.basename(r.file_path) for r in results}
        relative_paths = {str(Path(r.file_path).relative_to(python_project_structure)) for r in results}
        
        assert not any(name.startswith("test_") for name in file_names), f"Found test files: {[n for n in file_names if n.startswith('test_')]}"
        assert not any("tests/" in path for path in relative_paths), f"Found files in tests/: {[p for p in relative_paths if 'tests/' in p]}"
        
        # But should still find calls in main source files
        file_names = {os.path.basename(r.file_path) for r in results}
        assert "main.py" in file_names
        assert "models.py" in file_names
    
    def test_large_directory_performance(self, tmp_path):
        """Test performance with larger directory structures."""
        # Create many files with function calls
        for i in range(50):
            (tmp_path / f"file_{i:03d}.py").write_text(f"""
def function_{i}():
    get_file_content("data_{i}.json")
    process_data({{"{i}": "value"}})
    return True

class Class_{i}:
    def method_{i}(self):
        get_file_content("config_{i}.json")
        return self
""")
        
        params = SearchParameters(
            search_type="function-calls",
            target="get_file_content",
            scope=str(tmp_path),
            max_files=100,
            max_results=200
        )
        
        import time
        start_time = time.time()
        results = self.engine.search_directory(str(tmp_path), params)
        end_time = time.time()
        
        # Should find 100 calls (2 per file × 50 files)
        assert len(results) == 100
        
        # Should complete reasonably quickly (under 5 seconds for 50 files)
        assert (end_time - start_time) < 5.0
        
        # Check that results are properly formatted
        for result in results:
            assert "get_file_content" in result.match_text
            assert result.start_line > 0
            assert result.file_path.endswith(".py")
    
    def test_cross_file_pattern_analysis(self, python_project_structure):
        """Test analyzing function call patterns across multiple files."""
        # Search for common function calls that appear across files
        params = SearchParameters(
            search_type="function-calls",
            target="print",  # print() calls appear in multiple files
            scope=str(python_project_structure),
            file_patterns=["*.py"],
            exclude_patterns=["__pycache__/*"]
        )
        
        results = self.engine.search_directory(str(python_project_structure), params)
        
        # Should find print calls across multiple files
        file_names = {os.path.basename(r.file_path) for r in results}
        assert len(file_names) >= 1  # At least one file should have print calls
        
        # Group results by file to analyze patterns
        by_file = {}
        for result in results:
            filename = os.path.basename(result.file_path)
            if filename not in by_file:
                by_file[filename] = []
            by_file[filename].append(result)
        
        # Each file should have multiple function definitions
        for filename, file_results in by_file.items():
            if filename.endswith('.py') and not filename.startswith('__'):
                assert len(file_results) >= 1


class TestDirectorySearchEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test environment."""
        self.engine = SearchEngine()
    
    def test_deeply_nested_directories(self, tmp_path):
        """Test handling of deeply nested directory structures."""
        # Create deeply nested structure
        current_dir = tmp_path
        for i in range(10):
            current_dir = current_dir / f"level_{i}"
            current_dir.mkdir()
            (current_dir / f"file_{i}.py").write_text(f"print('level {i}')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path)
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        
        # Should find all files in nested structure
        assert len(results) == 10
        
        # Check that deep nesting is handled correctly
        deepest_result = max(results, key=lambda r: r.file_path.count(os.sep))
        assert "level_9" in deepest_result.file_path
    
    def test_mixed_file_encodings(self, tmp_path):
        """Test handling of files with different encodings."""
        # UTF-8 file
        utf8_file = tmp_path / "utf8.py"
        utf8_file.write_text("print('Hello 世界')", encoding='utf-8')
        
        # ASCII file
        ascii_file = tmp_path / "ascii.py" 
        ascii_file.write_text("print('Hello World')", encoding='ascii')
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path)
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        
        # Should handle both files
        assert len(results) == 2
        file_names = {os.path.basename(r.file_path) for r in results}
        assert "utf8.py" in file_names
        assert "ascii.py" in file_names
    
    def test_very_large_files(self, tmp_path):
        """Test handling of very large files."""
        # Create a large file with many function calls
        lines = []
        for i in range(1000):
            lines.append(f"    get_data('item_{i}')")
        
        large_file = tmp_path / "large.py"
        large_file.write_text("def process_all():\n" + "\n".join(lines))
        
        params = SearchParameters(
            search_type="function-calls",
            target="get_data",
            scope=str(tmp_path),
            max_results=500  # Limit results
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        
        # Should respect max_results limit
        assert len(results) <= 500
        
        # All results should be from the large file
        for result in results:
            assert "large.py" in result.file_path
            assert "get_data" in result.match_text
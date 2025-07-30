#!/usr/bin/env python3
"""
Test the new project creation system based on user prompts
"""
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from memory_manager import MemoryManager

def test_project_creation_from_prompts():
    print("=== Testing New Project Creation System ===")
    
    # Initialize components
    db_manager = DatabaseManager("data/mcp_memory.db")
    memory_manager = MemoryManager(db_manager)
    
    # Test prompts that should create new projects
    test_prompts = [
        "Build a modern Python web framework called 'Fusion' with Flask-like simplicity and Express.js middleware power",
        "Create an e-commerce API with user authentication, product catalog, and payment processing",
        "Develop a task management application with real-time collaboration features",
        "Design a machine learning pipeline for image classification using TensorFlow"
    ]
    
    print(f"\n1. Testing project name extraction from prompts:")
    for i, prompt in enumerate(test_prompts, 1):
        project_name = memory_manager.extract_project_name_from_prompt(prompt)
        is_new_project = memory_manager.is_new_project_request(prompt)
        print(f"   {i}. Prompt: {prompt[:60]}...")
        print(f"      -> Project Name: '{project_name}'")
        print(f"      -> Is New Project: {is_new_project}")
        print()
    
    # Test creating a project from a prompt
    print("2. Testing project creation from prompt:")
    test_prompt = "Build a modern Python web framework called 'Fusion' with Flask-like simplicity"
    
    # Clear current project to test creation
    memory_manager.current_project_id = None
    
    print(f"   Prompt: {test_prompt}")
    project_id = memory_manager.create_project_from_prompt(test_prompt)
    print(f"   Created Project ID: {project_id}")
    
    # Get project details
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    
    if project:
        print(f"   Project Details:")
        print(f"     - Name: {project['name']}")
        print(f"     - Description: {project['description'][:100]}...")
        print(f"     - Path: {project['path']}")
    
    # Test auto task creation with the new project
    print("\n3. Testing task creation in new project:")
    task_id = memory_manager.auto_create_task_from_context(test_prompt)
    if task_id:
        print(f"   Created Task ID: {task_id}")
        
        # Get task details
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task:
            print(f"   Task Details:")
            print(f"     - Title: {task['title']}")
            print(f"     - Category: {task['category']}")
            print(f"     - Priority: {task['priority']}")
            print(f"     - Project ID: {task['project_id']}")
            print(f"     - Matches Current Project: {task['project_id'] == memory_manager.current_project_id}")
    else:
        print("   No task created")
    
    # Show all projects now
    print("\n4. All projects in database:")
    cursor.execute("""
    SELECT p.name, p.id, COUNT(t.id) as task_count
    FROM projects p
    LEFT JOIN tasks t ON p.id = t.project_id
    GROUP BY p.id, p.name
    ORDER BY p.created_at DESC
    """)
    
    for project in cursor.fetchall():
        is_current = "[CURRENT]" if project[1] == memory_manager.current_project_id else ""
        print(f"   - {project[0]} ({project[1][:8]}...) - Tasks: {project[2]} {is_current}")
    
    db_manager.close()

if __name__ == "__main__":
    test_project_creation_from_prompts()
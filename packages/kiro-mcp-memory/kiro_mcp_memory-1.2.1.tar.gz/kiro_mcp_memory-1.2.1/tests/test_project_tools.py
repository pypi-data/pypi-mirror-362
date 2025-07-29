#!/usr/bin/env python3
"""
Test script to verify project management tools work correctly
"""
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from memory_manager import MemoryManager

def test_project_management():
    print("=== Testing Project Management ===")
    
    # Initialize components
    db_manager = DatabaseManager("data/mcp_memory.db")
    memory_manager = MemoryManager(db_manager)
    
    print("\n1. Current working directory:", os.getcwd())
    print("2. Detected project name:", memory_manager.detect_project_name())
    
    # Start session
    session_id = memory_manager.start_session()
    print(f"3. Started session: {session_id}")
    print(f"4. Current project ID: {memory_manager.current_project_id}")
    
    # Check all projects in database
    cursor = db_manager.connection.cursor()
    cursor.execute("""
    SELECT p.name, p.id, p.path, 
           COUNT(DISTINCT t.id) as task_count,
           COUNT(DISTINCT m.id) as memory_count
    FROM projects p
    LEFT JOIN tasks t ON p.id = t.project_id
    LEFT JOIN memories m ON p.id = m.project_id
    GROUP BY p.id, p.name, p.path
    ORDER BY p.created_at DESC
    """)
    
    projects = cursor.fetchall()
    print(f"\n5. All projects in database:")
    for project in projects:
        is_current = "[CURRENT]" if project[1] == memory_manager.current_project_id else ""
        print(f"   - {project[0]} ({project[1][:8]}...) - Tasks: {project[3]}, Memories: {project[4]} {is_current}")
        print(f"     Path: {project[2]}")
    
    # Test task retrieval for current project
    tasks = db_manager.get_tasks(memory_manager.current_project_id)
    print(f"\n6. Tasks in current project ({memory_manager.current_project_id[:8]}...):")
    for task in tasks:
        print(f"   - {task['title'][:60]}... [{task['status']}/{task['priority']}]")
    
    # Test switching to another project if available
    if len(projects) > 1:
        other_project = None
        for project in projects:
            if project[1] != memory_manager.current_project_id:
                other_project = project
                break
        
        if other_project:
            print(f"\n7. Switching to project: {other_project[0]} ({other_project[1][:8]}...)")
            memory_manager.current_project_id = other_project[1]
            memory_manager.load_relevant_memories()
            
            # Get tasks for the other project
            other_tasks = db_manager.get_tasks(memory_manager.current_project_id)
            print(f"8. Tasks in switched project:")
            for task in other_tasks:
                print(f"   - {task['title'][:60]}... [{task['status']}/{task['priority']}]")
    
    db_manager.close()

if __name__ == "__main__":
    test_project_management()
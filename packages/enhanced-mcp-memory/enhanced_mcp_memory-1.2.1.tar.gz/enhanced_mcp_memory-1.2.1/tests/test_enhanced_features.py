#!/usr/bin/env python3
"""
Test script for enhanced MCP server features
"""
import sys
import os
import json
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from memory_manager import MemoryManager

def test_enhanced_features():
    print("=== Testing Enhanced MCP Server Features ===")
    
    # Initialize components
    db_manager = DatabaseManager("data/mcp_memory.db")
    memory_manager = MemoryManager(db_manager)
    
    print("\n1. Testing Database Stats...")
    stats = db_manager.get_database_stats()
    print(f"   Database size: {stats.get('database_size_bytes', 0) / (1024*1024):.2f} MB")
    print(f"   Total projects: {stats.get('projects_count', 0)}")
    print(f"   Total memories: {stats.get('memories_count', 0)}")
    print(f"   Total tasks: {stats.get('tasks_count', 0)}")
    
    print("\n2. Testing Retry Mechanism...")
    try:
        # This should work with retry decorator
        project_id = db_manager.get_or_create_project("Test Enhanced Project", os.getcwd())
        print(f"   [OK] Project created/retrieved: {project_id[:8]}...")
        
        # Add some test data
        memory_id = db_manager.add_memory(
            project_id=project_id,
            memory_type="test",
            title="Test Memory",
            content="This is a test memory for enhanced features",
            importance_score=0.8
        )
        print(f"   [OK] Memory added: {memory_id[:8]}...")
        
        task_id = db_manager.add_task(
            project_id=project_id,
            title="Test Enhanced Task",
            description="Testing enhanced features",
            priority="high",
            category="test"
        )
        print(f"   [OK] Task added: {task_id[:8]}...")
        
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    print("\n3. Testing Cleanup Features...")
    try:
        # Add some old test data first
        old_memory_id = db_manager.add_memory(
            project_id=project_id,
            memory_type="test",
            title="Old Memory",
            content="This is old test data",
            importance_score=0.1  # Low importance for cleanup
        )
        
        # Manually set old date for testing
        cursor = db_manager.connection.cursor()
        cursor.execute("""
            UPDATE memories 
            SET created_at = datetime('now', '-40 days')
            WHERE id = ?
        """, (old_memory_id,))
        db_manager.connection.commit()
        
        # Test cleanup
        cleanup_results = db_manager.cleanup_old_data(days_old=30)
        print(f"   [OK] Cleanup results: {cleanup_results}")
        
    except Exception as e:
        print(f"   [ERROR] Cleanup error: {e}")
    
    print("\n4. Testing Memory Optimization...")
    try:
        # Add duplicate memories for testing
        dup_id1 = db_manager.add_memory(
            project_id=project_id,
            memory_type="test",
            title="Duplicate Memory",
            content="This is duplicate content",
            importance_score=0.5
        )
        
        dup_id2 = db_manager.add_memory(
            project_id=project_id,
            memory_type="test", 
            title="Duplicate Memory 2",
            content="This is duplicate content",  # Same content
            importance_score=0.5
        )
        
        print(f"   Added duplicate memories: {dup_id1[:8]}... and {dup_id2[:8]}...")
        
        # Test optimization
        optimization_results = db_manager.optimize_memories()
        print(f"   [OK] Optimization results: {optimization_results}")
        
    except Exception as e:
        print(f"   [ERROR] Optimization error: {e}")
    
    print("\n5. Testing Notifications...")
    try:
        # Add test notifications
        notif_id = db_manager.add_notification(
            project_id=project_id,
            notification_type="test",
            title="Test Notification",
            message="This is a test notification for enhanced features"
        )
        print(f"   [OK] Notification created: {notif_id[:8]}...")
        
        # Get notifications
        notifications = db_manager.get_notifications(project_id=project_id)
        print(f"   [INFO] Found {len(notifications)} notifications")
        
        # Mark as read
        success = db_manager.mark_notification_read(notif_id)
        print(f"   [OK] Marked as read: {success}")
        
    except Exception as e:
        print(f"   [ERROR] Notification error: {e}")
    
    print("\n6. Testing Performance Tracking...")
    try:
        from mcp_server_enhanced import PerformanceTracker
        
        tracker = PerformanceTracker()
        
        # Simulate some calls
        tracker.track_call("test_function", 0.1, True)
        tracker.track_call("test_function", 0.2, True)
        tracker.track_call("test_function", 0.15, False)  # One failure
        
        stats = tracker.get_stats()
        print(f"   [OK] Performance stats: {json.dumps(stats, indent=2)}")
        
    except Exception as e:
        print(f"   [ERROR] Performance tracking error: {e}")
    
    print("\n7. Final Database Stats...")
    final_stats = db_manager.get_database_stats()
    print(f"   Final database size: {final_stats.get('database_size_bytes', 0) / (1024*1024):.2f} MB")
    print(f"   Total projects: {final_stats.get('projects_count', 0)}")
    print(f"   Total memories: {final_stats.get('memories_count', 0)}")
    print(f"   Total tasks: {final_stats.get('tasks_count', 0)}")
    print(f"   Total notifications: {final_stats.get('notifications_count', 0)}")
    
    db_manager.close()
    print("\n[SUCCESS] Enhanced features testing completed!")

if __name__ == "__main__":
    test_enhanced_features()
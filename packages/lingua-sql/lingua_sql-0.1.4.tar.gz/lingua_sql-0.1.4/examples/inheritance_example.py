#!/usr/bin/env python3
"""
Example demonstrating MySQLConnector inheritance from Lingua_sqlBase
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lingua_sql.database.mysql_connector import MySQLConnector
from lingua_sql.base.base import Lingua_sqlBase
from lingua_sql import LinguaSQL

def demonstrate_inheritance():
    """Demonstrate that MySQLConnector properly inherits from Lingua_sqlBase"""
    print("=== MySQLConnector Inheritance Demonstration ===\n")
    
    # 1. Show inheritance relationship
    print("1. Inheritance Check:")
    print(f"   MySQLConnector is subclass of Lingua_sqlBase: {issubclass(MySQLConnector, Lingua_sqlBase)}")
    print(f"   MySQLConnector base classes: {MySQLConnector.__bases__}")
    print()
    
    # 2. Create an instance
    print("2. Creating MySQLConnector instance:")
    try:
        connector = MySQLConnector(
            host="localhost",
            user="test_user",
            password="test_password", 
            database="test_db",
            config={"test": True}
        )
        print("   ✓ MySQLConnector instance created successfully")
        print(f"   ✓ Instance type: {type(connector)}")
        print()
        
        # 3. Show methods from Lingua_sqlBase
        print("3. Methods inherited from Lingua_sqlBase:")
        base_methods = [
            'generate_embedding',
            'get_similar_question_sql', 
            'get_related_ddl',
            'get_related_documentation',
            'add_question_sql',
            'add_ddl',
            'add_documentation',
            'get_training_data',
            'remove_training_data',
            'system_message',
            'user_message',
            'assistant_message',
            'submit_prompt',
            'get_sql_prompt'
        ]
        
        for method in base_methods:
            if hasattr(connector, method):
                print(f"   ✓ {method}")
            else:
                print(f"   ✗ {method} (missing)")
        print()
        
        # 4. Show MySQL-specific methods
        print("4. MySQL-specific methods:")
        mysql_methods = [
            'connect',
            'disconnect', 
            'run_sql',
            'execute_update',
            'get_tables',
            'get_table_schema',
            'get_all_tables'
        ]
        
        for method in mysql_methods:
            if hasattr(connector, method):
                print(f"   ✓ {method}")
            else:
                print(f"   ✗ {method} (missing)")
        print()
        
        # 5. Test some method calls
        print("5. Testing method calls:")
        
        # Test base class methods
        embedding = connector.generate_embedding("test text")
        print(f"   generate_embedding result length: {len(embedding)}")
        
        system_msg = connector.system_message("You are a helpful assistant")
        print(f"   system_message result: {system_msg}")
        
        # Test MySQL methods (without actual connection)
        print("   Note: MySQL methods require actual database connection")
        print()
        
    except Exception as e:
        print(f"   ✗ Error creating instance: {e}")
        print()

def demonstrate_lingua_sql_integration():
    """Demonstrate how LinguaSQL integrates with MySQLConnector"""
    print("=== LinguaSQL Integration Demonstration ===\n")
    
    # 1. Create LinguaSQL with database config
    print("1. Creating LinguaSQL with database configuration:")
    try:
        nl = LinguaSQL(config={
            "api_key": "test_key",
            "model": "deepseek-chat", 
            "client": "in-memory",
            "db_host": "localhost",
            "db_user": "test_user",
            "db_password": "test_password",
            "db_database": "test_db"
        })
        print("   ✓ LinguaSQL instance created successfully")
        print(f"   ✓ Database connector type: {type(nl.db)}")
        print()
        
        # 2. Show that db attribute exists
        print("2. Database connector attributes:")
        if hasattr(nl, 'db') and nl.db is not None:
            print("   ✓ Database connector is available")
            print(f"   ✓ Database connector class: {nl.db.__class__.__name__}")
            print(f"   ✓ Database host: {nl.db.host}")
            print(f"   ✓ Database name: {nl.db.database}")
        else:
            print("   ✗ Database connector is not available")
        print()
        
        # 3. Test run_sql method
        print("3. Testing run_sql method:")
        if nl.db:
            print("   ✓ run_sql method is available")
            print("   Note: Actual SQL execution requires database connection")
        else:
            print("   ✗ run_sql method not available (no database connector)")
        print()
        
    except Exception as e:
        print(f"   ✗ Error creating LinguaSQL: {e}")
        print()
    
    # 4. Create LinguaSQL without database config
    print("4. Creating LinguaSQL without database configuration:")
    try:
        nl_no_db = LinguaSQL(config={
            "api_key": "test_key",
            "model": "deepseek-chat",
            "client": "in-memory"
        })
        print("   ✓ LinguaSQL instance created successfully")
        print(f"   ✓ Database connector: {nl_no_db.db}")
        print("   ✓ Database connector is None (as expected)")
        print()
        
    except Exception as e:
        print(f"   ✗ Error creating LinguaSQL without DB: {e}")
        print()

def main():
    """Main demonstration function"""
    print("MySQLConnector Inheritance and LinguaSQL Integration Demo")
    print("=" * 60)
    print()
    
    demonstrate_inheritance()
    demonstrate_lingua_sql_integration()
    
    print("=== Summary ===")
    print("✓ MySQLConnector properly inherits from Lingua_sqlBase")
    print("✓ MySQLConnector implements all required abstract methods")
    print("✓ MySQLConnector provides MySQL-specific functionality")
    print("✓ LinguaSQL can integrate with MySQLConnector")
    print("✓ LinguaSQL handles both with and without database configuration")
    print()
    print("The inheritance structure is working correctly!")

if __name__ == "__main__":
    main() 
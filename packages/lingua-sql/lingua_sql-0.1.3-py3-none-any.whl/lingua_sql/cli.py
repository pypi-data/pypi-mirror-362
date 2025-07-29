#!/usr/bin/env python3
"""
Lingua SQL Command Line Interface
"""

import argparse
import json
import os
import sys
from typing import Optional

from . import LinguaSQL


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Lingua SQL - Text-to-SQL pipeline using DeepSeek and ChromaDB"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question in natural language")
    ask_parser.add_argument("question", help="Natural language question")
    ask_parser.add_argument("--config", "-c", help="Path to config file")
    ask_parser.add_argument("--output", "-o", help="Output file for results")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train with custom data")
    train_parser.add_argument("--question", help="Training question")
    train_parser.add_argument("--sql", help="Training SQL")
    train_parser.add_argument("--ddl", help="Training DDL")
    train_parser.add_argument("--documentation", help="Training documentation")
    train_parser.add_argument("--config", "-c", help="Path to config file")
    
    # Import schema command
    schema_parser = subparsers.add_parser("import-schema", help="Import database schema")
    schema_parser.add_argument("--config", "-c", help="Path to config file")
    
    # Server command
    server_parser = subparsers.add_parser("serve", help="Start web server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    server_parser.add_argument("--config", "-c", help="Path to config file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Load configuration
    config = load_config(args.config)
    
    try:
        if args.command == "ask":
            handle_ask(args, config)
        elif args.command == "train":
            handle_train(args, config)
        elif args.command == "import-schema":
            handle_import_schema(config)
        elif args.command == "serve":
            handle_serve(args, config)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def load_config(config_path: Optional[str]) -> dict:
    """Load configuration from file or environment variables"""
    config = {}
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    
    # Override with environment variables
    env_mapping = {
        "db_host": "DB_HOST",
        "db_user": "DB_USER", 
        "db_password": "DB_PASSWORD",
        "db_database": "DB_DATABASE",
        "deepseek_api_key": "DEEPSEEK_API_KEY",
        "deepseek_base_url": "DEEPSEEK_BASE_URL",
        "chroma_persist_directory": "CHROMA_PERSIST_DIRECTORY"
    }
    
    for config_key, env_key in env_mapping.items():
        if env_key in os.environ:
            config[config_key] = os.environ[env_key]
    
    return config


def handle_ask(args, config: dict):
    """Handle ask command"""
    lingua_sql = LinguaSQL(config)
    
    print(f"Question: {args.question}")
    print("Generating SQL and executing query...")
    
    results = lingua_sql.ask(args.question)
    
    if results is not None:
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results saved to {args.output}")
        else:
            print("\nResults:")
            print(results)
    else:
        print("No results returned")


def handle_train(args, config: dict):
    """Handle train command"""
    lingua_sql = LinguaSQL(config)
    
    if not any([args.question, args.sql, args.ddl, args.documentation]):
        print("Error: At least one training parameter must be provided")
        return
    
    print("Training with provided data...")
    
    lingua_sql.train(
        question=args.question,
        sql=args.sql,
        ddl=args.ddl,
        documentation=args.documentation
    )
    
    print("Training completed successfully")


def handle_import_schema(config: dict):
    """Handle import-schema command"""
    lingua_sql = LinguaSQL(config)
    
    print("Importing database schema...")
    
    success = lingua_sql.import_database_schema()
    
    if success:
        print("Database schema imported successfully")
    else:
        print("Failed to import database schema")


def handle_serve(args, config: dict):
    """Handle serve command"""
    try:
        from .api.app import app
        import uvicorn
        
        print(f"Starting server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    except ImportError:
        print("Error: FastAPI dependencies not installed. Install with: pip install lingua-sql[web]")


if __name__ == "__main__":
    main() 
import os

def create_project_structure():
    file_structure = [
        "mcp-server/app/__init__.py",
        "mcp-server/app/main.py",
        "mcp-server/app/routes/chat.py",
        "mcp-server/app/core/context.py",
        "mcp-server/app/core/llm.py",
        "mcp-server/app/core/prompt.py",
        "mcp-server/app/core/tools.py",
        "mcp-server/app/services/dispatcher.py",
        "mcp-server/app/config.py",
        "mcp-server/tests/test_chat.py",
        "mcp-server/requirements.txt",
        "mcp-server/Dockerfile",
        "mcp-server/README.md",
    ]

    for file_path in file_structure:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("")

    print("✅ MCP server project structure created successfully.")

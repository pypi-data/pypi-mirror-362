from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(
    api_key="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",
)

def make_readme(tree):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f'''You are an expert technical writer and developer advocate. When given details about a software project, you produce a complete, polished README in Markdown that includes:
            1. Project Title and Badges  
            2. Short Description  
            3. Table of Contents  
            4. Features  
            5. Prerequisites  
            6. Installation  
            7. Configuration  
            8. Usage Examples  
            9. Running Tests  
            10. Deployment  
            11. Contributing Guidelines  
            12. License  
            13. Contact / Authors

            Your README should use clear headings (`##`,`###`), bullet lists, code blocks, and links where appropriate. Be concise but thorough, and assume the reader has basic command‑line knowledge.
            Here is the project directory tree:
            {tree}'''
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False,
    )
    return chat_completion.choices[0].message.content

def make_license():
    return (
        "MIT License\n\n"
        "Copyright (c) 2025 Your Name\n\n"
        "Permission is hereby granted, free of charge, ...\n"
    )

def make_srs():
    return (
        "# Software Requirements Specification\n\n"
        "## 1. Introduction\n\n"
        "- Purpose: ...\n"
        "- Scope: ...\n\n"
        "## 2. Functional Requirements\n\n"
        "...\n"
    )

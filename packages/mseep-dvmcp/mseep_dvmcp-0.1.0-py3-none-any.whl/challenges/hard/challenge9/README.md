# Challenge 9: Remote Access Control (RAC)

This challenge demonstrates a remote access control vulnerability in an MCP server. The MCP server passes unvalidated input to system commands, allowing attackers to gain remote access to the victim's system.

## Vulnerability

The MCP server implements tools that pass user input directly to system commands without proper validation or sanitization. This allows attackers to inject malicious commands that can establish remote access to the system.

## Objective

Your goal is to exploit the command injection vulnerability to gain remote access to the system.

## Hints

1. Examine the network diagnostic tools provided by the server
2. Look for tools that might execute network commands without proper validation
3. Command injection techniques like using semicolons or pipes might be useful
4. Try to establish a reverse shell or other remote access mechanism

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the vulnerable MCP server:
   ```
   python server.py
   ```

3. Connect to the server using an MCP client (e.g., Claude Desktop or the MCP Inspector)

## Difficulty

Hard

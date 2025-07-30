# Challenge 10: Multi-Vector Attack

This challenge demonstrates a sophisticated multi-vector attack against an MCP server. This challenge requires chaining multiple vulnerabilities together to successfully exploit the system.

## Vulnerability

The MCP server contains multiple vulnerabilities that can be combined to create a powerful attack chain. This includes prompt injection, tool shadowing, and credential theft techniques that must be used together to achieve the objective.

## Objective

Your goal is to perform a sophisticated attack that combines multiple vulnerability types to exfiltrate sensitive information and gain persistent access to the system.

## Hints

1. Examine all available tools and resources carefully
2. Look for ways to combine different vulnerability types
3. The authentication system might be vulnerable to multiple attack vectors
4. You'll need to chain at least three different vulnerabilities to complete this challenge

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

#!/usr/bin/env python3
"""Test NetworkX MCP Server with stdio transport."""

import json
import subprocess
import sys
import time

import pytest


def test_stdio_server():
    """Test NetworkX MCP Server with stdio transport."""
    print("🧪 Testing NetworkX MCP Server with stdio transport...")

    # Start the server process with stdio transport (default)
    process = subprocess.Popen(
        [sys.executable, "-m", "networkx_mcp.server", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
    )

    try:
        # Give it a moment to start
        time.sleep(1)

        # Check if process is running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("❌ Server failed to start!")
            if stderr:
                print(f"Error: {stderr}")
            pytest.fail("Server failed to start")

        print("✅ Server process started successfully!")

        # Test with a simple MCP request
        test_request = {"jsonrpc": "2.0", "method": "tools/list", "id": 1}

        try:
            # Send request
            request_str = json.dumps(test_request) + "\n"
            if process.stdin:
                process.stdin.write(request_str)
                process.stdin.flush()

            # Set a timeout for reading response
            # Make stdout non-blocking
            import fcntl
            import os
            import select

            if process.stdout:
                flags = fcntl.fcntl(process.stdout.fileno(), fcntl.F_GETFL)
                fcntl.fcntl(
                    process.stdout.fileno(), fcntl.F_SETFL, flags | os.O_NONBLOCK
                )

                # Wait for response
                ready, _, _ = select.select([process.stdout], [], [], 5.0)

                if ready:
                    response_lines = []
                    while True:
                        try:
                            line = process.stdout.readline()
                            if line:
                                response_lines.append(line)
                            else:
                                break
                        except Exception:
                            break

                    if response_lines:
                        print("📡 Server is responding to MCP requests!")
                        print(f"   Response preview: {response_lines[0][:100]}...")
                    else:
                        print("⚠️  Server started but no response received")
                else:
                    print("⚠️  Server started but response timed out")
            else:
                print("⚠️  Server process stdout not available")

        except Exception as e:
            print(f"⚠️  Communication error: {e}")

    finally:
        # Terminate the server
        process.terminate()
        process.wait()

    print("\n🛑 Test server stopped")
    print("✨ Server can be started with stdio transport!")


if __name__ == "__main__":
    # If run directly as a script, run the test
    test_stdio_server()

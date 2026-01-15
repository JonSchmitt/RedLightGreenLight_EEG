import base64
import sys

def generate_mermaid_link(mermaid_code):
    graphbytes = mermaid_code.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return f"https://mermaid.ink/svg/{base64_string}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read from arguments if provided (might be tricky with newlines)
        print("Please provide mermaid code via stdin for better handling of newlines.")
    
    # Read from stdin
    lines = sys.stdin.readlines()
    if lines:
        mermaid_code = "".join(lines)
        print(generate_mermaid_link(mermaid_code))

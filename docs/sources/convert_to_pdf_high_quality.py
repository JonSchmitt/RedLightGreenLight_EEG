import markdown
import asyncio
from playwright.async_api import async_playwright
import os
import tempfile
import re

async def convert_md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Pre-process md_content to handle local image paths correctly
    # We will use the absolute path in the HTML and load it via file://
    def fix_path(match):
        prefix = match.group(1)
        path = match.group(2)
        suffix = match.group(3)
        if not path.startswith('http') and not path.startswith('data:'):
            abs_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(md_file)), path))
            file_url = "file:///" + abs_path.replace("\\", "/")
            return f'{prefix}{file_url}{suffix}'
        return match.group(0)

    # Match ![alt](path)
    md_content = re.sub(r'(!\[.*?\]\()(.+?)(\))', fix_path, md_content)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'toc', 'tables'])
    
    # High-quality CSS for the PDF
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                line-height: 1.6;
                font-size: 11pt;
                color: #24292e;
                max-width: 900px;
                margin: 0 auto;
                padding: 2cm;
            }}
            h1, h2, h3, h4 {{
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
            }}
            pre {{
                background-color: #f6f8fa;
                padding: 16px;
                border-radius: 6px;
                overflow: auto;
                font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
                font-size: 85%;
            }}
            code {{
                background-color: rgba(27,31,35,0.05);
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: inherit;
                font-size: 85%;
            }}
            img {{
                max-width: 100%;
                display: block;
                margin: 20px auto;
                border: 1px solid #eee;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
            }}
            table {{
                border-spacing: 0;
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 16px;
            }}
            table th, table td {{
                padding: 6px 13px;
                border: 1px solid #dfe2e5;
            }}
            table tr {{
                background-color: #fff;
                border-top: 1px solid #c6cbd1;
            }}
            table tr:nth-child(2n) {{
                background-color: #f6f8fa;
            }}
            blockquote {{
                padding: 0 1em;
                color: #6a737d;
                border-left: 0.25em solid #dfe2e5;
                margin: 0 0 16px 0;
            }}
            ul, ol {{
                padding-left: 2em;
                margin-bottom: 16px;
                display: block;
            }}
            li {{
                margin-bottom: 4px;
                display: list-item;
            }}
            li p {{
                margin-top: 0;
                margin-bottom: 4px;
                display: block;
            }}
            li > ul, li > ol {{
                margin-bottom: 0;
                margin-top: 4px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Create a temporary HTML file to load via file:// URI
    # This is more reliable for local resource loading than set_content
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as tf:
        tf.write(styled_html)
        temp_html_path = tf.name

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Load the temporary file
            url = "file:///" + temp_html_path.replace("\\", "/")
            await page.goto(url, wait_until="networkidle")
            
            # Wait additional time for images to render (especially SVGs)
            await asyncio.sleep(3)
            
            await page.pdf(path=pdf_file, format="A4", print_background=True, margin={
                "top": "0cm", "bottom": "0cm", "left": "0cm", "right": "0cm"
            })
            await browser.close()
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

async def main():
    files = ["README.md", "ProjectStructure.md", "GameDetails.md"]
    for file in files:
        if not os.path.exists(file):
            continue
            
        pdf_name = file.replace(".md", ".pdf")
        print(f"Converting {file} to {pdf_name}...")
        try:
            await convert_md_to_pdf(file, pdf_name)
            print(f"Successfully created {pdf_name}")
        except Exception as e:
            print(f"Failed to create {pdf_name}: {e}")

if __name__ == "__main__":
    asyncio.run(main())

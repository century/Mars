import os
import markdown
from datetime import datetime
from jinja2 import Template

# Paths
input_dir = 'md'
output_dir = 'build'

# HTML templates
article_template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles.css">
    <title>{{ title }}</title>
</head>
<body>
    <header>
        <a href="index.html">Back to index</a>
        <h1>{{ title }}</h1>
        <p><strong>Date:</strong> {{ date }}</p>
    </header>
    <article>
        {{ content | safe }}
    </article>
</body>
<footer>
        <a href="index.html">Back to index</a>
</footer>
</html>"""

index_template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles.css">
    <title>Article Index</title>
    <style>
        ul {
            padding: 0;
            margin: 0;
        }
        .article-item {
            display: flex;
            justify-content: space-between;
            padding: 0;
        }
        .article-title {
            flex-grow: 1;
            margin: 0;
            padding: 0;
        }
        .article-date {
            text-align: right;
            white-space: nowrap;
            color: #888;
        }
        hr {
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <h1>Julian Maroux is a (type) designer with a focus on the web and life.</h1>
    <a href="https://wiki.78bpm.com">Wiki</a>
    <hr>
    <ul>
    {% for article in articles %}
        <li class="article-item">
            <span class="article-title"><a href="{{ article.filename }}">{{ article.title }}</a></span>
            <span class="article-date">{{ article.date }}</span>
        </li>
    {% endfor %}
    </ul>
</body>
</html>"""

article_template = Template(article_template_str)
index_template = Template(index_template_str)

# Helper function to extract metadata from markdown
def parse_metadata(md_content):
    lines = md_content.splitlines()
    metadata = {}
    if lines[0] == "---":
        for i in range(1, len(lines)):
            if lines[i] == "---":
                content = "\n".join(lines[i+1:])
                break
            key, value = lines[i].split(": ", 1)
            metadata[key.lower()] = value
    return metadata, content

# Prepare output directory
os.makedirs(output_dir, exist_ok=True)

# Get the list of existing HTML files in the /build directory
existing_html_files = {f for f in os.listdir(output_dir) if f.endswith('.html') and f != 'index.html'}

# Process each markdown file
articles = []
for filename in os.listdir(input_dir):
    if filename.endswith('.md'):
        with open(os.path.join(input_dir, filename), 'r') as f:
            md_content = f.read()
        
        # Extract metadata and content
        metadata, content_md = parse_metadata(md_content)
        content_html = markdown.markdown(content_md)

        # Use metadata to generate HTML
        output_filename = filename.replace('.md', '.html')
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w') as f:
            f.write(article_template.render(
                title=metadata.get('title', 'Untitled'),
                author=metadata.get('author', 'Unknown'),
                date=metadata.get('date', 'Unknown'),
                content=content_html
            ))

        # Collect articles for index
        articles.append({
            'title': metadata.get('title', 'Untitled'),
            'date': metadata.get('date', 'Unknown'),
            'filename': output_filename,
            'datetime': datetime.strptime(metadata['date'], '%Y-%m-%d')
        })

        # Keep track of the generated HTML files
        if output_filename in existing_html_files:
            existing_html_files.remove(output_filename)

# Remove orphaned HTML files that no longer have corresponding Markdown files
for orphan_html in existing_html_files:
    os.remove(os.path.join(output_dir, orphan_html))

# Sort articles by date, most recent first
articles = sorted(articles, key=lambda x: x['datetime'], reverse=True)

# Generate index.html
with open(os.path.join(output_dir, 'index.html'), 'w') as f:
    f.write(index_template.render(articles=articles))

print("Markdown to HTML build complete, and orphaned files deleted.")

import os 
import shutil
from textnode import *
from textparser import *

def main():
    # Define directories
    public_dir = 'public'
    static_dir = 'static'
    content_dir = 'content'
    template_html = 'template.html'
    
    # Clearing the public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Create public directory again
    os.makedirs(public_dir, exist_ok=True)

    # Copy all static files to public
    if os.path.exists(static_dir):
        for item in os.listdir(static_dir):
            full_item_path = os.path.join(static_dir, item)
            dest_item_path = os.path.join(public_dir, item)

            if os.path.isfile(full_item_path):
                shutil.copy(full_item_path, dest_item_path)
            elif os.path.isdir(full_item_path):
                # Ensure the target directory exists or overwrite it
                shutil.copytree(full_item_path, dest_item_path, dirs_exist_ok=True)

    # Generate pages recursively
    generate_pages_recursive(content_dir, template_html, public_dir)
    


def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
   
    os.mkdir(destination)
    source_content = os.listdir(source)

    for file in source_content:
        source_path = os.path.join(source, file)
        dest_path = os.path.join(destination, file)
        if os.path.isfile(source_path):
            shutil.copyfile(source_path, dest_path)
        else:
            copy_directory(source_path, dest_path)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if os.path.splitext(file)[1] == ".md":
                rel_path = os.path.relpath(root, dir_path_content)
                from_path = os.path.join(root, file)

                # Create destination path with .html extension
                html_file_name = os.path.splitext(file)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, rel_path, html_file_name)

                generate_page(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as markdown:
        markdown_file = markdown.read()
    
    with open(template_path, 'r') as template:
        template_file = template.read()

    markdown_node = markdown_to_html_node(markdown_file)
    html_node = markdown_node.to_html()
    page_title = extract_title(markdown_file)
    final_output = template_file.replace("{{ Title }}", page_title)
    final_output = final_output.replace("{{ Content }}", html_node)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file: 
        dest_file.write(final_output)
    
    

main()

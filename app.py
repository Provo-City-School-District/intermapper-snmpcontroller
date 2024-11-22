from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_scripts_from_subfolders():
    script_files = {}
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'scripts')):
        for file in files:
            if file.endswith('.py'):
                # Get relative path from BASE_DIR, excluding 'scripts/' from the path
                relative_path = os.path.relpath(os.path.join(root, file), BASE_DIR)
                folder = os.path.dirname(relative_path)  # Get folder name
                script_files.setdefault(folder, []).append(file)  # Add to dictionary
    return script_files

# Define routes
@app.route('/')
def index():
    script_files = get_scripts_from_subfolders()  # Get scripts from subfolders
    print(f"Detected scripts: {script_files}")
    # Sort the folders alphabetically
    sorted_script_files = {folder: scripts for folder, scripts in sorted(script_files.items())}
    
    return render_template('index.html', scripts=sorted_script_files)

@app.route('/run/<path:script_path>')
def run_script(script_path):
    # Add '.py' extension if it's missing
    if not script_path.endswith('.py'):
        script_path += '.py'

    # Ensure the full script path is constructed correctly
    script_full_path = os.path.join(BASE_DIR, '', script_path)  # Directly construct path
    print(f"Running script: {script_full_path}")
    
    try:
        # Run the script with Python3
        output = subprocess.run(
            ['python3', script_full_path],
            capture_output=True, text=True, check=True
        )
        return f"Output:<br><pre>{output.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error:<br><pre>{e.stderr}</pre>"
    except FileNotFoundError:
        return f"Error: Script '{script_full_path}' not found!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

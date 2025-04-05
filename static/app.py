import os
from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

# Set up the folder to store the uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure that the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to call your LLM model (main.py) after uploading the file
def process_document(file_path):
    # Replace this with the actual command you use to run your script
    command = f"python src/main.py {file_path} --llm lmstudio"
    
    # Run the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Return the output of the script
    return result.stdout

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # Save the uploaded file to the server's disk
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Call your processing function (main.py) to handle the file
    output = process_document(file_path)
    
    # Return the processed output to the user
    return render_template('result.html', output=output)

if __name__ == "__main__":
    app.run(debug=True)

import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='static/templates')

# Set up the folders
UPLOAD_FOLDER = os.path.abspath('uploads')
OUTPUT_FOLDER = os.path.abspath('outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure that the required folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to call the document processing script
def process_document(file_path):
    # Construct the output path
    base_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{name_without_ext}.xlsx")
    
    # Properly quote paths for command-line use
    quoted_file_path = f'"{file_path}"'
    quoted_output_path = f'"{output_path}"'
    
    # Use a list for subprocess.run to avoid shell-based path issues
    command = [
        "python", 
        "main.py", 
        file_path,
        "--excel_path", 
        output_path,
        "--llm_type", 
        "lmstudio"
    ]
    
    logging.info(f"Running command: {' '.join(command)}")
    
    # Run the command and capture the output
    result = subprocess.run(command, shell=False, capture_output=True, text=True)
    
    if result.returncode != 0:
        logging.error(f"Error processing document: {result.stderr}")
        return None, result.stderr
    
    logging.info(f"Processing complete: {result.stdout}")
    
    # Check if the output file was created
    if os.path.exists(output_path):
        return output_path, result.stdout
    else:
        return None, f"Output file not created. Process output: {result.stdout}"

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
    
    # Only allow docx files
    if not file.filename.endswith('.docx'):
        return render_template('error.html', message="Only .docx files are supported")
    
    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Process the document
    output_path, processing_output = process_document(file_path)
    
    if output_path:
        relative_path = os.path.relpath(output_path, start=os.path.dirname(__file__))
        filename = os.path.basename(output_path)
        return render_template('result.html', 
                              output=processing_output, 
                              excel_path=filename)
    else:
        return render_template('error.html', message=processing_output)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename),
                     as_attachment=True)

def main():
    import argparse
    from main import WordToExcelConverter  # Assuming this exists in your project

    parser = argparse.ArgumentParser(description="Convert Word to Excel with structured data.")
    parser.add_argument("word_path", type=str, help="Path to the Word document to convert")
    parser.add_argument("--excel_path", type=str, help="Path to save the converted Excel file", default=None)
    parser.add_argument("--llm_type", type=str, choices=["ollama", "lmstudio", "textgen"], default="ollama", help="LLM interface to use")
    parser.add_argument("--model", type=str, default="llama3", help="Model name to use with Ollama interface")
    
    args = parser.parse_args()
    
    # Initialize the WordToExcelConverter with specified LLM interface
    converter = WordToExcelConverter(llm_type=args.llm_type, model=args.model)
    
    # Convert the Word document to Excel
    excel_file = converter.convert_to_excel(args.word_path, excel_path=args.excel_path)
    
    print(f"Conversion complete. Excel file saved to: {excel_file}")

if __name__ == "__main__":
    app.run(debug=True)

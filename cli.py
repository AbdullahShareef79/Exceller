#!/usr/bin/env python3
import argparse
from app.core.document_processor import WordToExcelConverter

def main():
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
    main() 
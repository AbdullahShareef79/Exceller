from docx import Document
import pandas as pd
import os

class WordToExcelConverter:
    def __init__(self, llm_type: str = "lmstudio", model: str = "llama3"):
        """
        Initialize the converter.
        
        Args:
            llm_type (str): Type of LLM to use ('lmstudio', 'ollama', etc.)
            model (str): Name of the model to use
        """
        self.llm_type = llm_type
        self.model = model
    
    def convert_to_excel(self, input_path: str, excel_path: str = None) -> str:
        """
        Convert a Word document to Excel format.
        
        Args:
            input_path (str): Path to the input Word document
            excel_path (str, optional): Path for the output Excel file. If not provided,
                                      will use the input path with .xlsx extension
        
        Returns:
            str: Path to the generated Excel file
        """
        if not excel_path:
            excel_path = os.path.splitext(input_path)[0] + '.xlsx'
        
        # Read the Word document
        doc = Document(input_path)
        
        # Extract text from paragraphs
        data = []
        for para in doc.paragraphs:
            if para.text.strip():  # Only include non-empty paragraphs
                data.append({
                    'content': para.text,
                    'style': para.style.name
                })
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(excel_path, index=False)
        
        return excel_path 
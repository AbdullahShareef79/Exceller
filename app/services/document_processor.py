import os
from typing import Optional
from app.core.config import settings
from app.utils.word_to_excel import WordToExcelConverter
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, llm_type: str = "lmstudio", model: str = "llama3"):
        self.converter = WordToExcelConverter(llm_type=llm_type, model=model)
        
    def process(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Process a Word document and convert it to Excel format.
        
        Args:
            input_path: Path to the input Word document
            output_path: Optional path for the output Excel file
            
        Returns:
            str: Path to the generated Excel file
        """
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
                
            if output_path is None:
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(
                    settings.OUTPUT_FOLDER,
                    f"{base_name}.xlsx"
                )
                
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert document
            logger.info(f"Converting document: {input_path} -> {output_path}")
            self.converter.convert_to_excel(input_path, excel_path=output_path)
            
            if not os.path.exists(output_path):
                raise RuntimeError("Conversion failed: output file not created")
                
            return output_path
            
        except Exception as e:
            logger.exception(f"Error processing document: {input_path}")
            raise 
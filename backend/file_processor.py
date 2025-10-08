from PyPDF2 import PdfReader
from docx import Document
import os
from typing import Tuple

class FileProcessor:
    @staticmethod
    def extract_text(file_path: str, filename: str) -> Tuple[str, int]:
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension == '.pdf':
            return FileProcessor._extract_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return FileProcessor._extract_from_docx(file_path)
        elif file_extension == '.txt':
            return FileProcessor._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> Tuple[str, int]:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            word_count = len(text.split())
            return text.strip(), word_count
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def _extract_from_docx(file_path: str) -> Tuple[str, int]:
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            word_count = len(text.split())
            return text.strip(), word_count
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    @staticmethod
    def _extract_from_txt(file_path: str) -> Tuple[str, int]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            word_count = len(text.split())
            return text.strip(), word_count
        except Exception as e:
            raise Exception(f"Error extracting text from TXT: {str(e)}")

file_processor = FileProcessor()

import pdfplumber
import pandas as pd
from typing import Optional

class FileParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            return f"PDF解析失败: {str(e)}"
        return text

    @staticmethod
    def parse_excel(file_path: str) -> str:
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            return f"Excel解析失败: {str(e)}"

    @staticmethod
    def parse_file(file_path: str) -> str:
        if file_path.lower().endswith(".pdf"):
            return FileParser.parse_pdf(file_path)
        elif file_path.lower().endswith((".xlsx", ".xls")):
            return FileParser.parse_excel(file_path)
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"文件解析失败: {str(e)}"
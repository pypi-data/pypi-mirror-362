import os
import logging
import pandas as pd
from langchain_unstructured import UnstructuredLoader
from langchain.schema import Document
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class AutoLoader:
    """ AutoLoader automatically loads and processes various document formats
    including Excel, CSV, and unstructured formats like PDFs, Word docs, and PPTs, as well as email
    files from a single file or an entire directory. """

    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Provided path does not exist: {self.path}")
        self.documents = []

    def _is_excel_or_csv(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ['.xlsx', '.xls', '.csv']

    def _process_csv(self, file_path: str):
        logging.info(f"Processing CSV file: {file_path}")
        try:
            df = pd.read_csv(file_path, encoding='utf-8', encoding_errors='replace')
            for _, row in df.iterrows():
                content = row.to_json()
                self.documents.append(Document(page_content=content, metadata={"source": file_path}))
        except Exception as e:
            logging.error(f"Failed to process CSV file {file_path}: {e}")

    def _process_excel(self, file_path: str):
        logging.info(f"Processing Excel file: {file_path}")
        try:
            df_sheets = pd.read_excel(file_path, sheet_name=None)
            for sheet_name, sheet_df in df_sheets.items():
                for _, row in sheet_df.iterrows():
                    content = row.to_json()
                    self.documents.append(Document(
                        page_content=content,
                        metadata={"source": file_path, "sheet_name": sheet_name} ))
        except Exception as e:
            logging.error(f"Failed to process Excel file {file_path}: {e}")

    def _process_with_unstructured(self, file_path: str):
        logging.info(f"Processing unstructured file: {file_path}")
        try:
            loader = UnstructuredLoader(file_path)
            docs = loader.load()
            self.documents.extend(docs)
        except Exception as e:
            logging.error(f"Failed to process unstructured file {file_path}: {e}")

    def _process_file(self, file_path: str):
        """Dispatches file to appropriate processor based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            self._process_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            self._process_excel(file_path)
        else:
            self._process_with_unstructured(file_path)

    def load(self) -> List[Document]:
        """
        Loads and processes files from the given path (file or directory).
        Returns:
            List of Document objects.
        """
        logging.info(f"Starting load from path: {self.path}")
        if os.path.isfile(self.path):
            self._process_file(self.path)
        elif os.path.isdir(self.path):
            for root, _, files in os.walk(self.path):
                for file in files:
                    full_path = os.path.join(root, file)
                    self._process_file(full_path)
        else:
            logging.error(f"Invalid path: {self.path}")
        return self.documents

    def get_documents(self) -> List[Document]:
        """
        Returns the list of processed Document objects.
        """
        return self.documents
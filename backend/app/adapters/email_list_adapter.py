from abc import ABC, abstractmethod
from typing import List, Any

class SourceAdapter(ABC):
    """Abstract base class to get email list from various sources."""

    @abstractmethod
    def get_emails(self, source: Any) -> List[str]:
        pass
class JsonListEmailAdapter(SourceAdapter):
    """
    Adapter for email input coming directly from a JSON list.
    Expects `source` to be a list of email strings.
    """
    def get_emails(self, source: Any) -> List[str]:
        if not isinstance(source, list):
            raise ValueError("Expected a list of emails")
        
        # Optional: validate each item is a string (basic check)
        emails = [email for email in source if isinstance(email, str)]
        return emails
    
import io
class TxtFileEmailAdapter(SourceAdapter):
    """
    Adapter to extract emails from a TXT file.
    Expects `source` to be a file-like object or bytes.
    """
    def get_emails(self, source: Any) -> List[str]:
        # Support bytes or file-like object
        if isinstance(source, bytes):
            source = io.StringIO(source.decode('utf-8'))
        elif hasattr(source, "read"):
            # Already a file-like object
            pass
        else:
            raise ValueError("Expected a file-like object or bytes")

        emails = []
        for line in source:
            line = line.strip()
            if line:
                emails.append(line)
        return emails
    

import csv

class CsvFileEmailAdapter(SourceAdapter):
    """
    Adapter to extract emails from a CSV file.
    Expects `source` to be a file-like object or bytes.
    Assumes emails are in the first column.
    """
    def get_emails(self, source: Any) -> List[str]:
        if isinstance(source, bytes):
            source = io.StringIO(source.decode('utf-8'))
        elif hasattr(source, "read"):
            pass
        else:
            raise ValueError("Expected a file-like object or bytes")

        reader = csv.reader(source)
        emails = []
        for row in reader:
            if row:
                email = row[0].strip()
                if email:
                    emails.append(email)
        return emails
import pandas as pd

class ExcelFileEmailAdapter(SourceAdapter):
    """
    Adapter to extract emails from an Excel file.
    Expects `source` to be bytes or a file-like object.
    Extracts emails from the first column.
    """
    def get_emails(self, source: Any) -> List[str]:
        # Read Excel into a DataFrame
        if isinstance(source, bytes):
            source = io.BytesIO(source)
        elif hasattr(source, "read"):
            pass
        else:
            raise ValueError("Expected bytes or file-like object")

        df = pd.read_excel(source)
        if df.empty:
            return []

        # Get first column, drop NaNs, convert to str, strip whitespace
        emails = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        return emails

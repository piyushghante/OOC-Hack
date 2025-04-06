from typing import List

def parse_document(file_path: str) -> str:
    """
    Mock document parser that returns placeholder text.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        str: Placeholder text
    """
    # In a real implementation, this would parse different document types
    return f"This is a mock parsed document from {file_path}. In the actual implementation, this would be text extracted from the uploaded document."

def chunk_text(text: str, tokenizer=None, max_chunk_size: int = 1000) -> List[str]:
    """
    Mock text chunker that splits text into sentences.
    
    Args:
        text: Text to split into chunks
        tokenizer: Not used in this version
        max_chunk_size: Not used in this version
        
    Returns:
        List[str]: List containing the original text as a single chunk
    """
    # In a real implementation, this would split text into proper chunks
    return [text]
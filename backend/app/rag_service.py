import os

# Define the local data directory path for RAG files safely
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_rag_guidelines():
    """
    Loads text guidelines from local text or pdf files safely.
    Handles missing libraries and heavy files without raising 500 errors.
    """
    guidelines_dir = DATA_DIR
    
    # Fallback default text if directory or documents are inaccessible
    combined_text = "Systemic Guidance Baseline: Analyze user life path and core metrics in depth."
    
    if not os.path.exists(guidelines_dir):
        return combined_text

    extracted_chunks = []
    
    for file in os.listdir(guidelines_dir):
        file_path = os.path.join(guidelines_dir, file)
        
        # 1. Read standard Text / Markdown files
        if file.endswith(".txt") or file.endswith(".md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    extracted_chunks.append(f.read())
            except Exception as e:
                print(f"[RAG WARNING] Failed to read text file {file}: {e}")

        # 2. Read PDF files safely without letting failures break the API
        elif file.endswith(".pdf"):
            try:
                import pypdf
                reader = pypdf.PdfReader(file_path)
                # Limit extraction to first 10 pages if the PDF is massive (e.g. Psychology2e.pdf)
                max_pages = min(len(reader.pages), 10)
                pdf_text = "".join([reader.pages[i].extract_text() or "" for i in range(max_pages)])
                extracted_chunks.append(pdf_text)
            except ImportError:
                print(f"[RAG WARNING] 'pypdf' package not found. Run 'pip install pypdf'.")
            except Exception as e:
                print(f"[RAG WARNING] Could not parse PDF {file}: {e}")

    if extracted_chunks:
        combined_text = "\n\n".join(extracted_chunks)
        
    # Cap maximum context length to prevent exceeding LLM context limits
    return combined_text[:8000]
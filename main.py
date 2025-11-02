# # main.py
# import asyncio
# from baml_client import b
# # from baml_client.types import AnalyzeText

# import asyncio
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from baml_client.sync_client import b
#from baml_client.types import AnalyzeText
import baml_client
print(dir(baml_client))

def call_baml_analyze_text(text_chunk: str) -> str:
    """
    Calls the BAML 'AnalyzeText' function to get a summary of the text chunk.
    """
    print(f"  [BAML Call] Processing chunk of {len(text_chunk)} chars with AnalyzeText...")
    summary = b.AnalyzeText(text_chunk)
    return summary


def load_book_text() -> str:
    """Loads your book. For this demo, it's a small sample."""
    
    # In your real project, you would do:
    with open("baml_src/ingest/RomeoAndJuliet.txt", "r", encoding="utf-8") as f:
        return f.read()
    
 

def process_entire_book(book_text: str):
    """
    The main Map-Reduce pipeline.
    """
    
    # --- 1. SPLIT (Chunking) ---
    # This splitter will try to split on newlines, then spaces, etc.
    # It's a reliable way to create chunks of a desired size.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,  # The target size for each chunk in characters
        chunk_overlap=200, # How many characters to overlap between chunks
        length_function=len,
        is_separator_regex=False,
    )

    print(f"Loaded book with {len(book_text)} characters.")
    print("Splitting book into recursive chunks...")
    
    chunks = text_splitter.create_documents([book_text])
    
    print(f"Book was split into {len(chunks)} chunks.\n")
    
    # --- 2. MAP (Process each chunk) ---
    print("Beginning 'Map' phase: Processing each chunk with BAML...")
    
    # This list will hold the summary from each chunk.
    all_summaries = []
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- Processing Chunk {i+1}/{len(chunks)} (size: {len(chunk.page_content)}) ---")
        
        # This is where we call our baml function
        summary_from_chunk = call_baml_analyze_text(chunk.page_content)
        
        if summary_from_chunk:
            print(f"  [BAML Success] Received summary for chunk.")
            all_summaries.append(summary_from_chunk)
        else:
            print("  [BAML Success] Received empty summary for this chunk.")
            
    print("\n\n'Map' phase complete.")

    # --- 3. REDUCE (Combine results) ---
    print("Beginning 'Reduce' phase: Combining all results...")
    return all_summaries


# --- Main execution ---
if __name__ == "__main__":
    
    # Step 1: Load the text
    my_book = load_book_text()
    
    # Step 2: Run the full pipeline
    all_summaries = process_entire_book(my_book)
    
    # Step 3: Show the final, combined result
    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETE. FINAL COMBINED DATA:")
    print("="*50)
    
    print(json.dumps(all_summaries, indent=2))
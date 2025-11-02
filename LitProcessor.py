import json
from langchain.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings

# Import the BAML client
from baml_client import baml


def call_baml_analyze_text(text_chunk: str) -> str:
    """
    Calls the BAML 'AnalyzeText' function to get a summary of the text chunk.
    """
    print(f"  [BAML Call] Processing chunk of {len(text_chunk)} chars with AnalyzeText...")
    summary = baml.AnalyzeText(text_chunk)
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
    # We use a standard, lightweight embedding model
    # (it runs on your machine, no API key needed)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # This is the semantic chunker.
    # It will find "natural" breakpoints in the text based on
    # how much the meaning shifts.
    text_splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile" 
        # You can also try "standard_deviation" or "interquartile"
    )

    print(f"Loaded book with {len(book_text)} characters.")
    print("Splitting book into semantic chunks...")
    
    chunks = text_splitter.split_text(book_text)
    
    print(f"Book was split into {len(chunks)} chunks.\n")
    
    # --- 2. MAP (Process each chunk) ---
    print("Beginning 'Map' phase: Processing each chunk with BAML...")
    
    # This list will hold the summary from each chunk.
    all_summaries = []
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- Processing Chunk {i+1}/{len(chunks)} ---")
        
        # This is where we call our baml function
        summary_from_chunk = call_baml_analyze_text(chunk)
        
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
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from baml_client.sync_client import b
#from baml_client.types import AnalyzeText
import baml_client
from pathlib import Path
from typing import List
#import os
#import pprint

from dataclasses import dataclass, asdict

print(dir(baml_client))


FILE_PATH = Path("D:/Projects/LitAna/baml_src/ingest/RomeoAndJuliet.txt")
TITLE = FILE_PATH.name.split(".")[0]


@dataclass
class AnalysisResults:
    title: str
    characters: List[dict]
    
    def save_to_json(self, output_dir: Path) -> None:
        """Save analysis results to a JSON file"""
        output_path = output_dir / f"{self.title}_analysis.json"
        with output_path.open('w', encoding='utf-8') as f:
            json.dump({
                'title': self.title,
                'characters': self.characters
            }, f, indent=2)
            
    def to_dict(self) -> dict:
        """Convert results to dictionary format"""
        return asdict(self)


# def load_book_text(file_path: Path) -> str:
#     """Loads your book. For this demo, it's a small sample."""
    
#     # In your real project, you would do:
#     if file_path.exists():
#         with open("baml_src/ingest/RomeoAndJuliet.txt", "r", encoding="utf-8") as f:
#             content = f.read()
#         return content

def get_file_content(file_path: Path) -> str:
    if file_path.exists():
        with file_path.open(encoding='utf-8',mode='r') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"The file at {file_path} does not exist.")



def call_baml_analyze_text(text_chunk: str) -> str:
    """
    Calls the BAML 'AnalyzeText' function to get a summary of the text chunk.
    """
    print(f"  [BAML Call] Processing chunk of {len(text_chunk)} chars with AnalyzeText...")
    summary = b.AnalyzeTextForSections(text_chunk)
    return summary


def process_entire_book(book_text: str):
    """
    The main Map-Reduce pipeline.
    """
    
    # --- 1. SPLIT (Chunking) ---
    # This splitter will try to split on newlines, then spaces, etc.
    # It's a reliable way to create chunks of a desired size.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=16000,  # The target size for each chunk in characters
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
            print("[BAML Success] Received summary for chunk.")
            all_summaries.append(summary_from_chunk)
        else:
            print("  [BAML Success] Received empty summary for this chunk.")
            
    print("\n\n'Map' phase complete.")

    # --- 3. REDUCE (Combine results) ---
    print("Beginning 'Reduce' phase: Combining all results...")
    #return all_summaries

    processed_summaries = [
        summary.__dict__ if hasattr(summary, '__dict__') else summary 
        for summary in all_summaries
    ]

    # Add debug output to see the results
    print("\nReduced Results:")
    print("="*50)
    for i, summary in enumerate(processed_summaries, 1):
        print(f"\nSummary {i}:")
        print("-"*30)
        print(f"Raw summary data: {summary}")
        print("-"*30)
    print("="*50)    

    return processed_summaries


# --- Main execution ---
if __name__ == "__main__":

    output_dir = Path("D:/Projects/LitAna/output")
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Load the text
    content = get_file_content(file_path=FILE_PATH)
    
    # Step 2: Run the full pipeline
    summaries = process_entire_book(content)

    # results = AnalysisResults(
    #     title=TITLE,
    #     characters=summaries
    # )
    
    # results.save_to_json(output_dir)

    # # Step 3: Show the final, combined result
    # print("\n" + "="*50)
    # print("✅ PIPELINE COMPLETE. FINAL COMBINED DATA:")
    # print("="*50)
    
    # print(json.dumps(results.to_dict(), indent=2))

    output_file = output_dir / f"{TITLE}_analysis.txt"
    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"Analysis Results for {TITLE}\n")
        f.write("="*50 + "\n\n")
        
        for summary in summaries:
            # Write each summary as plain text
            f.write(str(summary))
            f.write("\n" + "-"*30 + "\n")
    
    print(f"\nAnalysis complete. Results saved to: {output_file}")
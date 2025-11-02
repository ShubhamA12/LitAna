# # main.py
# import asyncio
# from baml_client import b
# # from baml_client.types import AnalyzeText


# async def process_lit_from_text(text: str):
#   """Calls the BAML function to extract details from the provided invoice text."""
#   details = b.AnalyzeText(text)
#   print("--- Extracted Literature Details ---")
#   print(details)
#   print("---------------------------------")


# async def main():
#   """Reads an Literature from a text file and processes it."""
#   file_path = "D:/Projects/LitAna/baml_src/ingest/RomeoAndJuliet.txt"  # Assumes invoice.txt is in the same directory
#   with open(file_path, "r", encoding="utf-8") as f:
#     lit_content = f.read()
#   await process_lit_from_text(lit_content)

# if __name__ == "__main__":
#   asyncio.run(main())

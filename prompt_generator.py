import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import google.generativeai as genai
from docx import Document as DocxDocument
import PyPDF2
import textwrap
import csv  # Import the 'csv' module

# --- Configuration ---
WATCH_FOLDER = os.path.join(os.path.dirname(__file__), 'converter_folder')
MODEL_NAME = "models/gemini-1.5-flash-8b-latest"
GOOGLE_SHEET_ID = "YOUR_GOOGLE_SHEET_ID"
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Structured")  # Define output folder relative to this file's directory
OUTPUT_CSV_FILENAME = "structured_prompts.csv" # Define CSV filename
# ---------------------

prompt_template = """**EXTREMELY IMPORTANT: Analyze the following page of coding documentation with MAXIMUM thoroughness.**  Your ABSOLUTE TOP PRIORITY is to extract *every single* code example and *every single* piece of instructional text from this page.  The goal is to create the MOST EFFECTIVE structured prompt possible for training an AI model to generate code that is consistent with this documentation.  **DO NOT MISS ANY CODE EXAMPLES OR INSTRUCTIONS.**

Create a structured prompt that includes these sections, ensuring you are as comprehensive as possible:

1.  **Comprehensive Functionality Overview:** Provide an *extremely detailed* overview of the functionality described on this page.  Explain *everything* the code or instructions are intended to do, no matter how small or seemingly insignificant.  Leave nothing out.

2.  **ALL Code Examples (Extracted Verbatim):**  **CRITICAL:** Find and extract *every single code example* present on this documentation page.  For each code example, include:
    *   **Full Code Snippet:** Copy the code exactly as it appears in the documentation.
    *   **Programming Language (Explicitly State):** Identify and clearly state the programming language for each code example. If the language is not explicitly stated, make your best educated guess and note it.
    *   **Context and Explanation (from documentation):**  Include the *immediate surrounding text* from the documentation that explains what each code example demonstrates or how it should be used.

3.  **Detailed Step-by-Step Instructions:** Extract *every single step-by-step instruction* provided on this page.  Even if instructions seem obvious or trivial, include them. Use numbered lists for sequential instructions.

4.  **Input and Output Specifications (for Code Examples):** For *each code example*, meticulously detail:
    *   **Inputs/Parameters/Arguments:** List and describe *every* input, parameter, or argument used in the code example. Include data types, purpose, and any constraints mentioned in the documentation.
    *   **Expected Output/Return Value:** Describe the *exact output* or return value that the code example is expected to produce. Include example outputs if provided.

5.  **Complete Context and Nuances:** Capture *all* other relevant information from the page that could be important for understanding or using the code or instructions. This includes:
    *   Explanations of concepts, algorithms, or libraries.
    *   Notes, warnings, and important considerations.
    *   Links to external resources or further documentation (if relevant and directly mentioned on the page).
    *   Any details about error handling, edge cases, or limitations.

6.  **Programming Language (Overall Documentation Focus):**  State the primary programming language that this documentation page is focused on, if it is clear.

7.  **Structured Prompt for ULTIMATE Code Generation Training Effectiveness:** Format the structured prompt to be as detailed, organized, and comprehensive as possible. Use Markdown extensively (headings, lists, code blocks, bold text) to maximize clarity and make it the *absolute best training data* for a code generation AI model.  Assume that every detail is important for the model to learn effectively.

**--- Coding Documentation Page Content ---**
{page_text}
**--- End of Documentation Page ---**

**ULTRA-THOROUGH Structured Code Generation Training Prompt Output:**
"""


# Load environment variables (for API key)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    exit()
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


class DocumentationEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None

        filepath = event.src_path
        if filepath.lower().endswith(('.pdf', '.txt', '.docx', '.html')):
            print(f"New documentation file detected: {filepath}")
            process_documentation_file(filepath)


def process_documentation_file(filepath):
    import textwrap

    # --- Configuration within function ---
    MAX_RESPONSE_CHARS = 5000  # Define the maximum character limit for responses
    
    # Use the same dynamic OUTPUT_FOLDER as defined above
    csv_filepath = os.path.join(OUTPUT_FOLDER, OUTPUT_CSV_FILENAME)
    # ---------------------

    print(f"Processing file: {filepath}")
    text_content = ""
    file_extension = filepath.lower().split('.')[-1]
    base_filename = os.path.splitext(os.path.basename(filepath))[0]

    structured_prompts_for_csv = []

    try:
        if file_extension == 'docx':
            docx_doc = DocxDocument(filepath)
            for paragraph in docx_doc.paragraphs:
                text_content += paragraph.text + "\n"
            print(f"  Extracted text from DOCX file.")

        elif file_extension == 'pdf':
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text()
            print(f"  Extracted text from PDF file (Number of pages: {num_pages}).")

        elif file_extension == 'txt':
            with open(filepath, 'r', encoding='utf-8') as txt_file:
                text_content = txt_file.read()
            print(f"  Read text from TXT file.")

        else:
            print(f"  Unsupported file format for text extraction: {file_extension}")
            return

        page_length_chars = 1000
        pages = textwrap.wrap(text_content, width=page_length_chars, replace_whitespace=False, drop_whitespace=False)
        print(f"  Split content into {len(pages)} pages.")

        for i, page_text in enumerate(pages):
            page_num = i + 1
            print(f"\n  --- Page {page_num} ---")

            prompt_content = prompt_template.format(page_text=page_text)

            try:
                print(f"    [DEBUG] Sending prompt to Gemini model...")
                response = model.generate_content(prompt_content)
                print(f"    [DEBUG] Received response from Gemini model.")
                structured_prompt = response.text
                if structured_prompt:
                    print(f"  Generated Structured Prompt (Original Length: {len(structured_prompt)} chars):")
                    truncated_response = structured_prompt
                    is_truncated = False
                    if len(structured_prompt) > MAX_RESPONSE_CHARS:
                        truncated_response = structured_prompt[:MAX_RESPONSE_CHARS] + f"\n\n[RESPONSE TRUNCATED TO {MAX_RESPONSE_CHARS} CHARACTERS DUE TO LENGTH LIMIT]"
                        is_truncated = True
                        print(f"  **WARNING: Structured prompt for page {page_num} TRUNCATED.")
                    structured_prompts_for_csv.append({
                        'page_content': page_text,
                        'original_response': structured_prompt,
                        'response': truncated_response,
                        'truncated': is_truncated
                    })
                else:
                    print("  Gemini model returned an empty response for this page.")
            except Exception as e:
                print(f"  Error generating structured prompt for page {page_num}: {e}")

    except Exception as e:
        print(f"  Error processing file: {filepath}")
        print(f"  Error details: {e}")

    finally:
        if structured_prompts_for_csv:
            save_prompts_to_csv(structured_prompts_for_csv, csv_filepath)
            print(f"  Saved structured prompts to CSV file: {csv_filepath}")
        else:
            print("  No structured prompts generated for this file to save to CSV.")


def save_prompts_to_csv(structured_prompts, csv_filepath):
    try:
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=['page_content', 'original_response', 'response', 'truncated'])
            csv_writer.writeheader()
            csv_writer.writerows(structured_prompts)
        print(f"  Successfully wrote {len(structured_prompts)} prompts to CSV: {csv_filepath}")
    except Exception as e:
        print(f"  Error writing to CSV file: {csv_filepath}")
        print(f"  Error details: {e}")


if __name__ == "__main__":
    event_handler = DocumentationEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Watching for new documentation files in folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("File watching stopped.")
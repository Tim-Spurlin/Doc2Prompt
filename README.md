# Doc2Prompt 

Doc2Prompt is an automated script built by **Tim Spurlin** to convert documentation files into structured prompts, generating a CSV file optimized for AI model training. This tool processes documentation page by page, leveraging AI to create effective structured prompts that capture key information for training models to understand and utilize the documented content. It is designed to streamline the process of preparing high-quality training data from diverse documentation sources.

---

## 📜 Overview

Doc2Prompt automates the creation of structured prompts from various documentation formats (Word documents, PDFs, TXT files, HTML). It processes each page of documentation, uses AI to analyze the content, and generates a structured prompt for each page. The final output is a CSV file containing these structured prompts, ready for direct import into platforms like Google AI Studio for model tuning.

---

## 🚀 Key Features

- **Automated Structured Prompt Creation**:  
  Utilizes AI (Google AI Studio API) to automatically generate structured prompts from documentation content.

- **Page-by-Page Processing**:  
  Processes documentation one page at a time to create granular and focused structured prompts for each section of the documentation.

- **Versatile Input Format Support**:  
  Handles various documentation formats including `.docx`, `.pdf`, `.txt`, and `.html` files, providing flexibility in the types of documentation that can be processed.

- **Configurable Output to CSV**:  
  Outputs the structured prompts in a CSV (`.csv`) format, which is directly compatible with Google AI Studio and other model tuning platforms.

- **Handles Long Responses**:  
  Automatically truncates generated structured prompts to adhere to character limits for model tuning, ensuring data validity. Flags truncated responses for user awareness.

- **File System Monitoring**:  
  Uses file system monitoring (`watchdog`) to automatically detect new documentation files added to a designated folder and process them in real-time.

---

## 🔍 Detailed Functionality

### 🛠️ How It Works

1. **Folder Monitoring**:  
   The script continuously monitors a specified folder for new documentation files.

2. **File Detection and Processing**:  
   When a new documentation file is placed in the watch folder, the script automatically detects it and initiates processing.  
   It extracts text content from the documentation file, regardless of its format (`.docx`, `.pdf`, `.txt`, `.html`).

3. **Page Splitting**:  
   The extracted text content is intelligently split into manageable "pages" or sections to ensure focused processing and stay within AI model token limits.

4. **AI-Powered Prompt Generation**:  
   For each "page" of documentation, the script sends a prompt to the Google AI Studio API (Gemini model).  
   This prompt instructs the AI to analyze the page content and generate a structured prompt that captures the key instructional or code-related information.

5. **Structured Prompt Output**:  
   The AI-generated structured prompt for each page is captured.  
   The script ensures that the 'response' part of each structured prompt adheres to a 5,000 character limit, truncating if necessary and flagging truncated entries.

6. **CSV Output**:  
   All generated structured prompts, along with the original page content and truncation flags, are saved into a single CSV file (`structured_prompts.csv`) in a designated output folder.  
   This CSV file is structured with columns for 'page_content', 'original_response', 'response' (truncated and ready for tuning), and 'truncated' (flag).

---

## 🌐 Practical Applications

Doc2Prompt is designed to be broadly applicable for anyone needing to create structured training data from documentation:

- **AI Model Tuning for Code Generation**:  
  Ideal for preparing training datasets to fine-tune AI models for code generation tasks, using various forms of coding documentation.

- **Creating Training Data from API Documentation**:  
  Automatically convert API documentation into structured prompts to train models to interact with APIs effectively.

- **Processing Technical Manuals and Guides**:  
  Transform technical manuals, how-to guides, and instructional documents into structured data for AI learning.

- **Educational Material Conversion**:  
  Convert educational documents and learning resources into structured prompts for AI-driven learning platforms.

- **Knowledge Base Structuring**:  
  Process knowledge base articles and documentation to create structured representations of information for AI-powered knowledge retrieval and understanding.

---

## 🖥️ Usage Instructions

### ⚙️ Setup

1. **Install Python and Dependencies**:  
   Ensure Python 3.7 or higher is installed.  
   Create and activate a virtual environment (recommended):  
   ```bash
   python -m venv prompt_env
   source prompt_env/bin/activate  # Windows: prompt_env\Scripts\activate
   ```
   Install required Python libraries using pip:  
   ```bash
   pip install google-generativeai google-auth-oauthlib google-auth-httplib2 google-api-python-client google-auth watchdog python-dotenv pandas python-docx PyPDF2 beautifulsoup4
   ```

2. **Configure API Key**:  
   Open the included `.env` file in the project directory.  
   Replace the placeholder with your actual Google AI Studio API key:  
   ```
   GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_API_KEY
   ```

3. **Prepare Documentation**:  
   Place your documentation files (`.docx`, `.pdf`, `.txt`, `.html`) in the designated "STRUCTURED PROMPT CONVERTER" folder on your computer:  
   `C:\Users\timsp\OneDrive\Desktop\STRUCTURED PROMPT CONVERTER`.  
   Ensure the "Structured" output folder exists:  
   `C:\Users\timsp\OneDrive\Desktop\STRUCTURED PROMPT CONVERTER\Structured`.

### ▶️ Running Doc2Prompt

1. **Activate Virtual Environment**:  
   If you created a virtual environment, activate it in your terminal.

2. **Run the Script**:  
   Execute the `prompt_generator.py` script from your terminal within Visual Studio Code:  
   ```bash
   python prompt_generator.py
   ```
   The script will start watching the "STRUCTURED PROMPT CONVERTER" folder.

3. **Add Documentation Files**:  
   Copy your documentation files into the "STRUCTURED PROMPT CONVERTER" folder.  
   Doc2Prompt will automatically detect and process these files one by one.

4. **Check Output**:  
   Once processing is complete, a `structured_prompts.csv` file will be created in the "Structured" output folder:  
   `C:\Users\timsp\OneDrive\Desktop\STRUCTURED PROMPT CONVERTER\Structured`.  
   This CSV file contains your structured prompts, ready for import into Google AI Studio or other model tuning platforms.

---

## 📁 Project Structure

```plaintext
Doc2Prompt/
├── prompt_env/         # Virtual environment folder (optional)
├── prompt_generator.py # Main Python script
├── test_api.py         # Script to test API key setup
├── .env                # File to store API key (add to .gitignore)
├── Structured/         # Output folder for CSV file
├── README.md           # This README file
```

---

## 💡 Detailed Recommendations

For optimal use of Doc2Prompt:

- **Review and Refine Prompt Template**:  
  Customize the `prompt_template` variable in `prompt_generator.py` to further refine the structure and content of the generated prompts based on your specific documentation and training needs.

- **Experiment with `page_length_chars`**:  
  Adjust the `page_length_chars` configuration variable to control the granularity of page splitting, balancing context window size and page focus.

- **Monitor Output Quality**:  
  Review the generated `structured_prompts.csv` file to ensure the quality and relevance of the structured prompts for your model training tasks. Iterate on the prompt template and script as needed to optimize output quality.

- **Handle Large Documentation Sets**:  
  For very large documentation collections, consider running Doc2Prompt in batches and monitoring Google AI Studio API usage to stay within rate limits.

---

## 🤝 Benefits for Collaborators

- **Automate Data Preparation**:  
  Significantly reduces manual effort in creating structured training data from documentation, accelerating AI model development.

- **Improve Model Training Quality**:  
  Generates structured prompts designed to capture key information effectively, leading to potentially better-trained AI models.

- **Versatile and Customizable**:  
  Adaptable to various documentation formats and customizable through prompt template adjustments to suit different training objectives.

- **Open and Extensible**:  
  The Python script is well-structured and can be further extended or integrated into larger data processing pipelines.

---

## 🔗 Cloning the Repository

To get started with Doc2Prompt, clone the repository from GitHub:

```bash
git clone https://github.com/Tim-Spurlin/Doc2Prompt.git
cd Doc2Prompt
```

Explore the code, customize it to your needs, and feel free to contribute improvements!

---

## ✍️ Contributing

Contributions to enhance Doc2Prompt are welcome!  Consider contributing improvements to:

- **Prompt Template Optimization**:  
  Experiment with and suggest improved prompt templates for different types of documentation and training tasks.

- **Enhanced File Handling**:  
  Add support for more documentation formats or improve text extraction robustness.

- **Advanced Page Splitting**:  
  Implement more sophisticated page splitting logic (e.g., semantic splitting).

- **Error Handling and Logging**:  
  Improve error handling and add more detailed logging for script execution.

- **Performance Optimization**:  
  Explore ways to optimize the script's performance for processing very large documentation sets.

To contribute, fork the repository, create a feature branch, and submit a pull request. For issues or feature requests, please open an issue on GitHub.

---

## 📜 License

Doc2Prompt is licensed under the MIT License, a permissive open-source license that allows free use, modification, and distribution of the software. Users can incorporate it into their projects with minimal restrictions, provided they include the original copyright and license notice.

---

## 🌟 Connect and Collaborate

Doc2Prompt is designed to be a valuable tool for the AI development community, simplifying the creation of training data from documentation. If you have suggestions, improvements, or want to share how you are using Doc2Prompt, please connect and collaborate!

- **GitHub:** [Tim-Spurlin](https://github.com/Tim-Spurlin)
- **Email:** [Tim.Spurlin@SaphyreSolutions.com](mailto:Tim.Spurlin@SaphyreSolutions.com)
- **Phone:** 701-941-0811 (Call or text for an immediate response)
- **LinkedIn:** [Professional Profile](https://www.linkedin.com/in/christianspurlin93/)
- **Organization:** [Saphyre Solutions LLC](https://github.com/Saphyre-Solutions-LLC)

Let's make AI model training more efficient and accessible together!

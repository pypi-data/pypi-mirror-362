# AutoLoader

**AutoLoader** is a Python utility that automatically loads and processes both **structured** and **unstructured** documents using the [LangChain](https://www.langchain.com/) framework.

It supports:
- **Structured files**: CSV, Excel (`.csv`, `.xlsx`, `.xls`)
- **Unstructured files**: PDFs, Word docs, PowerPoints, Emails, and more

---

## 📦 Features

- ✅ Load files from a **single file or a directory**
- ✅ Automatically detects file type
- ✅ Converts rows to `langchain.schema.Document` objects
- ✅ Extracts metadata (source file, sheet name)
- ✅ Logs file loading progress and errors
- ✅ Supports LangChain-compatible document structure

---

## 🛠 Installation

```bash
pip install pandas langchain langchain-unstructured

```
## 🚀 Usage
```
from autoloader import AutoLoader

# Load from a single file or directory
loader = AutoLoader(path="./data")

# Process all supported files
documents = loader.load()

# Join and format documents into a single string
structured_docs = "\n\n".join(
    f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
    for doc in documents
)

# Print the first 1000 characters
print(structured_docs[:1000])
 
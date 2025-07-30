from auto_loader import AutoLoader

if __name__ == "__main__":
    path = r"C:\Users\DELL\Downloads\New folder"  # Change to your actual path
    loader = AutoLoader(path)
    docs = loader.load()

    # Pretty print first few docs
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Document #{i+1} ---")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Content:\n{doc.page_content}")

import tkinter as tk
from tkinter import filedialog
from llm import BudgetAssistantManager

root = tk.Tk()
root.withdraw()

print("Please select your receipt image...")
receipt_path = filedialog.askopenfilename(
    title="Select Receipt Image",
    filetypes=[
        ("Image files", "*.jpg *.jpeg *.png"),
        ("All files", "*.*")
    ]
)

if receipt_path:
    print(f"\nSelected: {receipt_path}")
    print("Processing...\n")
    
    assistant = BudgetAssistantManager()
    result = assistant.receipt_reader.read_receipt(receipt_path)
    print(result)
else:
    print("No file selected")
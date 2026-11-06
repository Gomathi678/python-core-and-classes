import fitz

doc = fitz.open()

page = doc.new_page()

page.insert_text(
    (50, 50),
    "Yoho Employee Data Service - Sample PDF. "
    "This document is created for Task 2 PDF text extraction.",
)

doc.save("sample.pdf")
doc.close()

print("Sample PDF created successfully")

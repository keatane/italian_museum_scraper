import pandas as pd
import re

# Read the input text file
with open('museum.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Split by categories
category_blocks = re.split(r'#+\nCategory: (.+?)\n#+', content)

# Initialize Excel writer (using 'with' so it closes properly)
with pd.ExcelWriter('museum.xlsx', engine='openpyxl') as writer:
    # category_blocks[0] is empty if text starts with "#####", so step by 2
    for i in range(1, len(category_blocks), 2):
        category = category_blocks[i].strip()
        data = category_blocks[i+1]
        
        # Find all entries within the category
        entries = re.findall(r"Name: (.*?)\nDescription: \[(.*?)\]\n-+", data, re.DOTALL)

        rows = []
        for name, desc_block in entries:
            # Split the description into details
            details = [d.strip(" '") for d in desc_block.split(",")]
            # Ensure exactly 3 details
            while len(details) < 3:
                details.append('')
            rows.append([name] + details[:3])

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=['Name', 'Detail1', 'Detail2', 'Detail3'])
        
        # Write to a sheet named after the category
        safe_category = category[:31]
        df.to_excel(writer, sheet_name=safe_category, index=False)

# Text Blocks 

## What is TextBlocks?

The `TextBlocks` class is a powerful tool that helps you extract structured information from unorganized text data.  
It's like a smart assistant for processing text and updating databases with the relevant details.

## How to Use TextBlocks

```py
# Import the TextBlocks class
from text_block_local.text_block import TextBlocks

# Initialize the TextBlocks class
text_blocks_processor = TextBlocks()

# Example 1: Process a Specific Text Block
# This will process a text block with the specified ID and update the database.
text_blocks_processor.process_text_block_by_id(text_block_id=123)

# Example 2: Process All Text Blocks
# This will process all text blocks and update the database (update=True by default).
text_blocks_processor.check_all_text_blocks()

# Example 3: Identify and Update Text Block Type
# Identify and update the text block type based on the text content.
# Replace '123' with the actual text block ID and provide the text.
text_blocks_processor.identify_and_update_text_block_type(text_block_id=123, text="Your text here")

# Example 4: Create a Person Profile
# Create a person profile and update related tables with the extracted fields.
# Replace the example fields with actual data.
person_id = text_blocks_processor.create_person_profile(fields_dict={"First Name": ["John"], "Last Name": ["Doe"]})

# You can use these examples as a reference to use the TextBlocks class in your project.
# Customize the data and text block IDs as needed for your specific use case.
```
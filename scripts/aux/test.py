import sys
import os

# Check if an argument is provided
if len(sys.argv) > 1:
    # Get the passed script_name argument
    script_name = sys.argv[1]

    # Get the base name of the file
    file_name = os.path.basename(script_name)

    print(file_name)
else:
    print("No script name provided.")
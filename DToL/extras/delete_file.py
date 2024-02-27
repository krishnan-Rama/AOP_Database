import os
import glob
import shutil

def clean_directory(root_dir):
    for subdir, dirs, files in os.walk(root_dir, topdown=False):
        # Find all files matching the patterns
        pep_files = sorted(glob.glob(os.path.join(subdir, '*-pep.fa.gz')))
        xref_files = sorted(glob.glob(os.path.join(subdir, '*-xref.tsv.gz')))

        # Function to keep the last file of a pattern, remove the rest
        def keep_last_file_only(file_list):
            if len(file_list) > 1:
                for file in file_list[:-1]:  # Keep the last file, delete the rest
                    os.remove(file)

        # Apply the cleaning function to each set of files
        keep_last_file_only(pep_files)
        keep_last_file_only(xref_files)

        # After cleaning, check the number of items in the directory
        remaining_items = os.listdir(subdir)

        # Check if the directory is empty, and if so, delete the directory
        if not remaining_items:
            shutil.rmtree(subdir)
            print(f"Deleted empty directory: {subdir}")
        # If there is exactly one file or directory, delete the directory
        elif len(remaining_items) == 1:
            shutil.rmtree(subdir)
            print(f"Deleted directory with a single item: {subdir}")
        else:
            print(f"Cleaned directory: {subdir}")

# Example usage
root_directory = "/home/c23048124/Desktop/DToL/SPECIES"  # Change this to your root directory path
clean_directory(root_directory)


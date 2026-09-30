import os

def display_contents(path, indent=0):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            print("  " * indent + f"[Folder] {item}")
            display_contents(full_path, indent + 1)
        else:
            print("  " * indent + f"[File] {item}")

folder_path = input("Enter folder path: ")
display_contents(folder_path)

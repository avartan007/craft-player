import os

folder = "music"
prefix_to_remove = "shinkanzen_chokai_n4_"

if not os.path.isdir(folder):
    print(f"Folder `{folder}` not found")
    exit()

files = os.listdir(folder)
renamed_count = 0

for file in files:
    if file.startswith(prefix_to_remove):
        old_path = os.path.join(folder, file)
        new_name = file.replace(prefix_to_remove, "")
        new_path = os.path.join(folder, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {file} → {new_name}")
        renamed_count += 1

print(f"\n✅ Renamed {renamed_count} files!")

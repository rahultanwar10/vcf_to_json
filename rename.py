import re
import json
import os

vcf_path = "contacts.vcf"  # Path to your .vcf file
folder_path = "/Users/rahultanwar/Downloads/crypt 15/result"  # Folder containing the .html files

def parse_vcf(file_path):
    contacts = {}

    with open(file_path, 'r') as file:
        name = None
        phone_number = None
        for line in file:
            if line.startswith("FN:"):
                name = line.strip().replace("FN:", "").strip()
            elif "TEL" in line:
                phone_number = re.sub(r"\D", "", line.split(":")[1].strip())
                contacts[phone_number] = name
    return contacts

def rename_files(vcf_path, folder_path):
    contacts = parse_vcf(vcf_path)

    for filename in os.listdir(folder_path):
        # Check if the filename matches the pattern of contact_number.html
        match = re.match(r"(\d+)\.html", filename)
        if match:
            contact_number = match.group(1)
            if contact_number in contacts:
                contact_name = contacts[contact_number]
                new_filename = f"{contact_name}.html"
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")

rename_files(vcf_path, folder_path)

contacts_dict = parse_vcf(vcf_path)
# print(contacts_dict)
with open("contacts.json",'w', encoding='utf-8') as file:
    json.dump(contacts_dict, file, indent=4)
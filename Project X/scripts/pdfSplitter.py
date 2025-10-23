import os
import PyPDF2
import sys
import shutil

def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def split_pdf(filename, folder):
    if folder:
        path = f'input/{folder}/{filename}'
    else:
        path = f'input/{filename}'
    pdfFileObj = open(path, 'rb')
    reader = PyPDF2.PdfReader(pdfFileObj)

    print(f'Processing {filename}')

    split_folder = os.path.join('temp/files_split', filename)
    ensure_folder_exists(split_folder)

    for pageNum in range(len(reader.pages)):
        pdfWriter = PyPDF2.PdfWriter()
        pdfWriter.add_page(reader.pages[pageNum])
        pdfOutputFile = open(f'{split_folder}/{filename.split(".")[0]}_page{pageNum + 1}.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()

    pdfFileObj.close()

def copy_pdf(filename, folder):
    if folder:
        path = f'input/{folder}/{filename}'
    else:
        path = f'input/{filename}'

    split_folder = os.path.join('temp/files_split', filename)
    ensure_folder_exists(split_folder)
    shutil.copy2(path, f'{split_folder}/{filename}')

def main(input_filename, split, folder=""):
    if split == 'y':
        split_pdf(input_filename, folder)
    elif split == 'n':
        copy_pdf(input_filename, folder)
    else:
        print('Invalid input. Please enter y or n.')
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        input_filename = input('Enter the filename: ')
        split = input('Split (y/n): ')
    else:
        input_filename = sys.argv[1]
        split = sys.argv[2]
    
    main(input_filename, split)

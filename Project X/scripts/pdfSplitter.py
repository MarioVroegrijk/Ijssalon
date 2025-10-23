import os
import PyPDF2
import sys
import shutil

# Split the PDF files into a PDF file per page
def split_pdf(filename, folder):
    if folder:
        path = f'input/{folder}/{filename}'
    else:
        path = f'input/{filename}'
    
    pdfFileObj = open(path, 'rb')
    reader = PyPDF2.PdfReader(pdfFileObj)

    print(f'Processing {filename}')

    for pageNum in range(len(reader.pages)):
        output_folder = f'temp/files_split/{filename}'
        os.makedirs(output_folder, exist_ok=True)
        
        pdfWriter = PyPDF2.PdfWriter()
        pdfWriter.add_page(reader.pages[pageNum])
        
        pdfOutputFile = open(f'{output_folder}/{filename.split(".")[0]}_page{str(pageNum + 1)}.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()

    pdfFileObj.close()

def copy_pdf(filename, folder):
    if folder:
        path = f'input/{folder}/{filename}'
    else:
        path = f'input/{filename}'
    
    output_folder = f'temp/files_split/{filename}'
    os.makedirs(output_folder, exist_ok=True)
    shutil.copy2(path, f'{output_folder}/{filename}')

def main(input_filename, split, folder=""):
    if split.lower() == 'y':
        split_pdf(input_filename, folder)
    elif split.lower() == 'n':
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

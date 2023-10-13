import streamlit as st
import pytesseract
from gtts import gTTS
from IPython.display import Audio
from PIL import Image
from pdf2image import convert_from_path
import os



def get_filename_without_extension(file_path):
    file_basename = os.path.basename(file_path)
    filename_without_extension = file_basename.split('.')[0]
    return filename_without_extension

def percentage(curr,total):
  return curr/total * 100

IMAGES_DIR = "/Images/"
AUDIO_DIR = "/Audio/"


def pdf2Image(fn):
  file = get_filename_without_extension(fn)
  print(fn);
  pages = convert_from_path(fn, 500)
  print(pages)
  filenames = [];
  

  # Counter to store images of each page of PDF to image
  image_counter = 1
  total = len(pages)
    
  # Parent Directory path  
  parent_dir = "Images"

  # Path  
  path = os.path.join(parent_dir, file) 
  pdf_img_dir = os.mkdir(path)
  # Iterate through all the pages stored above
  for page in pages:
    filename = os.path.join(path, f"page_{image_counter}.jpg")
    filenames.append(filename)
    page.save(filename, "JPEG")


    image_counter = image_counter + 1

  return filenames

def convertImagesToText(filenames, ofilename):
  # Creating a text file to write the output
  outfile = "Texts/out_text_"+ofilename+".txt"

  # Open the file in append mode so that
  # All contents of all images are added to the same file
  f = open(outfile, "a")
  for file in filenames:
    print(file)
    text = str(((pytesseract.image_to_string(Image.open(file)))))
    text = text.replace('-\n', '')
    text = text + '\n'
    f.write(text)
  f.close()
  print(outfile + " prepared :) ")
  return outfile



st.title("PDF to Audio Converter")

uploaded_pdf = st.file_uploader("Upload a PDF file")
if uploaded_pdf is not None:
  file_details = {"FileName":uploaded_pdf.name,"FileType":uploaded_pdf.type}
  with open(os.path.join("pdfs",uploaded_pdf.name),"wb") as f: 
    f.write(uploaded_pdf.getbuffer())  
  if st.button("Convert to Audio"):
    with st.spinner(f"Converting {uploaded_pdf.name} to audio..."):
      filename = get_filename_without_extension(uploaded_pdf.name)
      path = os.path.join("pdfs", uploaded_pdf.name) 
      filenames = pdf2Image(path)
      outFile = convertImagesToText(filenames,filename)
      text = open(outFile).read()
      ta_tts = gTTS(text)
      ta_tts.save(f"Audio/{filename}.mp3")
      st.audio(f"Audio/{filename}.mp3")


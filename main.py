import pyttsx3
import PyPDF2


def read_pdf_to_speech(file_path):
    pdf_reader = PyPDF2.Pdf_Reader(open(file_path,"rb"))
    text_to_speech = pyttsx3
    
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        legible_text = text.strip().repace("\n", " ")
        print(legible_text)
        text_to_speech.say(legible_text)
        text_to_speech.runAndWait()
        
    text_to_speech.stop()
    
def save_pdf_to_audio(file_path,output_file):
    pdf_reader = PyPDF2.PdfReader(open(file_path,"rb"))
    text_to_speech = pyttsx3.init()
    
    full_text = ""
    for page in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page].extract_text()
        legible_text = text.strip().replace("\n"," ")
        full_text += legible_text 
    
    text_to_speech.save_to_file(full_text,output_file)
    text_to_speech.runAndWait()
    text_to_speech.stop()
    
pdf_file_path = "path_to_your_pdf_file.pdf"
read_pdf_to_speech(pdf_file_path)

        
        
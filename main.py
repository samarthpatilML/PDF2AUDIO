import pyttsx3
import PyPDF2


def read_pdf_to_speech(file_path):
    try:
        pdf_reader = PyPDF2.PdfReader(open(file_path, "rb"))
        text_to_speech = pyttsx3.init()
        
        for page in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page].extract_text()
            if text:  # Ensure the page contains text
                legible_text = text.strip().replace("\n", " ")
                print(legible_text)
                text_to_speech.say(legible_text)
                text_to_speech.runAndWait()
        
        text_to_speech.stop()
    except Exception as e:
        print(f"Error: {e}")


def save_pdf_to_audio(file_path, output_file):
    try:
        pdf_reader = PyPDF2.PdfReader(open(file_path, "rb"))
        text_to_speech = pyttsx3.init()
        
        full_text = ""
        for page in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page].extract_text()
            if text:  # Ensure the page contains text
                legible_text = text.strip().replace("\n", " ")
                full_text += legible_text
        
        text_to_speech.save_to_file(full_text, output_file)
        text_to_speech.runAndWait()
    except Exception as e:
        print(f"Error: {e}")


# Example Usage
pdf_file_path = "newdemo.pdf"  # Replace with your PDF file path
output_audio_file = "file.mp3"  # Ensure the file name includes the correct extension

# Read and speak PDF text
read_pdf_to_speech(pdf_file_path)

# Save PDF text to an audio file
save_pdf_to_audio(pdf_file_path, output_audio_file)

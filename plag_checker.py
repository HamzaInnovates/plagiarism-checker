import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from customtkinter import filedialog
import customtkinter
import tkinter
from tkinter import messagebox
from docx import Document
import PyPDF2

# Load spaCy model for text preprocessing
nlp = spacy.load('en_core_web_sm')

root = customtkinter.CTk()
root.title("Plagiarism Checker")
root.geometry("500x400+400+100")
root.resizable(0,0)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Load first file
def loadfile1():
    try:
        global doc1
        file1 = filedialog.askopenfilename()
        if file1:
            doc1 = preprocess_text(read_file(file1))
            choosenlbl1.configure(text="File 1 chosen")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open the file: {str(e)}")

# Load second file
def loadfile2():
    try:
        global doc2
        file2 = filedialog.askopenfilename()
        if file2:
            doc2 = preprocess_text(read_file(file2))
            choosenlbl2.configure(text="File 2 chosen")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open the file: {str(e)}")

# Read files
def read_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_path.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file_path)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        messagebox.showerror("Error", "Unsupported file type.")

# Preprocess text using spaCy
def preprocess_text(text):
    doc = nlp(text)
    # Remove stop words and punctuation, and lemmatize
    return ' '.join(token.lemma_ for token in doc if not token.is_stop and not token.is_punct)

# Check plagiarism
def check_plag():
    try:
        if choosenlbl1.cget("text") == "" or choosenlbl2.cget("text") == "":
            messagebox.showerror("Error", "Please choose both files. Thank you!")
        else:
            doc_1_data = doc1
            doc_2_data = doc2
            vectorizer = TfidfVectorizer()
            matrix = vectorizer.fit_transform([doc_1_data, doc_2_data])
            sim = cosine_similarity(matrix)
            s = sim[0, 1]
            s = round(s * 100)
            result_lbl.configure(text=f"{str(s)}% plagiarism detected")
    except Exception as e:
        messagebox.showerror("Error", f"Due to {str(e)}, the file cannot be handled")

# GUI setup
heading_lbl = customtkinter.CTkLabel(root, font=('american', 30, 'bold'), text="Plagiarism Checker", fg_color="Yellow", text_color="Black", corner_radius=30).place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
buttons_frame = customtkinter.CTkFrame(root, height=250, width=400).place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
choose_lbl = customtkinter.CTkLabel(buttons_frame, text="Choose both files to check the plagiarism", font=('american', 10, 'bold')).place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
choosenlbl1 = customtkinter.CTkLabel(buttons_frame, text="", font=('american', 10, 'bold'), state="disable")
choosenlbl1.place(relx=0.27, rely=0.5)
choosenlbl2 = customtkinter.CTkLabel(buttons_frame, text="", font=('american', 10, 'bold'), state="disable")
choosenlbl2.place(relx=0.57, rely=0.5)
file1_btn = customtkinter.CTkButton(buttons_frame, text="Choose", font=('american', 15, 'bold'), command=loadfile1).place(relx=0.2, rely=0.6)
file2_btn = customtkinter.CTkButton(buttons_frame, text="Choose", font=('american', 15, 'bold'), command=loadfile2).place(relx=0.5, rely=0.6)
result_btn = customtkinter.CTkButton(buttons_frame, text="Check", font=('american', 20, 'bold'), fg_color="green4", command=check_plag).place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
result_lbl = customtkinter.CTkLabel(buttons_frame, text="", font=('american', 15, 'bold'), fg_color="red", pady=10)
result_lbl.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

root.mainloop()

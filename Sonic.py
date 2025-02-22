import os
import google.generativeai as genai
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# Configure Gemini AI
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyD8eTQvrCVDFizlD4fLnO90h_eXXNDEfW4"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
   system_instruction="""
You are SONIC, an AI chatbot that specializes in converting natural language into optimized SQL queries.  
When the conversation starts, introduce yourself in an engaging manner as SONIC, maintaining a friendly and energetic tone.  

After your introduction, focus solely on generating SQL queries from natural language inputs, ensuring correctness and efficiency.  
- If a user receives a wrong query, regenerate another improved query.  
- If incorrect queries persist (after 4-5 attempts), log a grievance and provide contact information for 'Naveen'.  

Additionally, after successfully generating 4-5 correct queries, request feedback from the user on improvements and incorporate their suggestions in subsequent interactions.  
"""

)

chat_session = model.start_chat(history=[])

# Function to handle user input
def send_message():
    user_input = user_entry.get().strip()
    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_input}\n", "user")

    try:
        response = chat_session.send_message(user_input)
        ai_response = response.text if response else "Error: No response from AI."
    except Exception as e:
        ai_response = f"Error: {str(e)}"

    chat_box.insert(tk.END, f"Sonic: {ai_response}\n", "ai")
    chat_box.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

# Initialize Main Window
root = ctk.CTk()
root.geometry("400x600")  # Increased size
root.title("Chat with Sonic - AI SQL Bot")
ctk.set_appearance_mode("light")

# Header Section (Gradient Background)
header = ctk.CTkFrame(root, fg_color=("#0066FF", "#0099FF"), height=90, corner_radius=10)
header.pack(fill="x", pady=5)

# Load and Display Profile Image
profile_img = Image.open("sonic.jpg")  # Replace with actual image path
profile_img = profile_img.resize((50, 50))
profile_photo = ImageTk.PhotoImage(profile_img)

profile_label = tk.Label(header, image=profile_photo, bg="#0099FF")
profile_label.place(x=10, y=20)

name_label = tk.Label(header, text="Sonic - AI SQL Bot", font=("Arial", 15, "bold"), fg="white", bg="#0099FF")
name_label.place(x=70, y=25)

status_label = tk.Label(header, text="We are online!", font=("Arial", 11), fg="white", bg="#0099FF")
status_label.place(x=70, y=50)

# Chat Display Area (Scrollable)
chat_frame = tk.Frame(root, bg="white")
chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=18, font=("Arial", 12), bg="#F0F0F0")
chat_box.pack(fill="both", expand=True, padx=10, pady=5)
chat_box.tag_config("user", foreground="blue")
chat_box.tag_config("ai", foreground="green")
chat_box.config(state=tk.DISABLED)

# Input Section
input_frame = ctk.CTkFrame(root, fg_color="white", height=60)
input_frame.pack(fill="x", side="bottom", pady=5, padx=10)

user_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter your message...", width=270, height=40)
user_entry.pack(side="left", padx=10, pady=5)
user_entry.bind("<Return>", lambda event: send_message())

send_button = ctk.CTkButton(input_frame, text="➤", width=50, height=40, fg_color="#0066FF", text_color="white", corner_radius=20, command=send_message)
send_button.pack(side="right", padx=10, pady=5)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pandas as pd
import matplotlib.pyplot as plt
from libs import communicationlayer
from libs.modelpipeline import PredictionPipeline
from libs.communicationlayer import ServerSocket
from queue import Queue
import time

MODEL_PATH = "models/finetuned_model.json"
TEST_PATH = "datasets/deploy_data.csv"
SUB_PATH = "datasets/new_sub.csv"
TXSPEED = 1           # 1 second  
conncetions_ips = communicationlayer.connection_ips  # List to store connection IPs

loading = True

server_queue = Queue()   
model_pipeline = None
root = None  # Main window reference
prediction_label = None  # Label to display predictions
X_test = pd.read_csv(TEST_PATH).iloc[:, :8]  # Assuming first 8 columns are features

sub_df = pd.read_csv(SUB_PATH)
X_sub = sub_df.iloc[:, :8]
y_sub = sub_df.iloc[:, 8:]

# for better look for the GUI
plt.tight_layout()

def animate_loading():
    while loading:
        progress_bar.start(10)
        time.sleep(0.2)

def initialize_app():
    global loading, model_pipeline # Declare globals to access outside the function
    
    try:
        splash_label.config(text="Initializing AI Model...")
        splash_root.update()
        # Load the AI model
        model_pipeline = PredictionPipeline(MODEL_PATH)  
        splash_label.config(text="Model loaded successfully")
        # create a server socket for communication
        server_socket = ServerSocket(server_queue = server_queue)
        server_socket.start() 
        splash_root.update()
        time.sleep(1)

    except Exception as e:
        messagebox.showerror("Error", f"AI Model Initialization Failed: {e}")
        loading = False
        splash_root.destroy()
        return
    
    loading = False
    splash_root.after(0, lambda: (splash_root.destroy(), main_app()))

def function_one():
    """ Reads test data, makes predictions using the AI model, and sends them via serial communication. """
    if model_pipeline is None:
        messagebox.showerror("Error", "AI Model not initialized.")
        return
    
    try:
        for idx, row in X_test.iterrows():
            row_df = pd.DataFrame([row], columns=X_test.columns)
            predictions = model_pipeline.predict(row_df)  
            server_queue.put(list(predictions))              
            # Update prediction label dynamically
            prediction_label.config(text=f"Prediction: {predictions}")
            root.update()  # Refresh the window
            time.sleep(TXSPEED)  # Simulate delay
        messagebox.showinfo("Success", "Predictions sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run predictions: {e}")

def function_two():
    def train_model():
        """ Runs model training in a separate thread to keep UI responsive. """
        try:
            loading_label.config(text="Training in progress...", fg="red")
            loading_window.update()

            # Train the model
            model_pipeline.train(X_sub, y_sub)

            # Update UI after training is complete
            loading_label.config(text="Training Completed!", fg="green")
            messagebox.showinfo("Success", "Model trained successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to train model: {e}")
            loading_label.config(text="Training Failed!", fg="red")

        # Close the loading window and return to the main app
        loading_window.destroy()
        root.deiconify()

    # Create a loading window
    loading_window = tk.Toplevel(root)
    loading_window.title("Training in Progress")
    loading_window.geometry("300x150")
    loading_window.resizable(False, False)
    
    loading_label = tk.Label(loading_window, text="Training started...", font=("Arial", 12))
    loading_label.pack(pady=20)

    progress_bar = ttk.Progressbar(loading_window, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
    progress_bar.pack(pady=10)
    progress_bar.start(10)

    # Hide main window while training
    root.withdraw()

    # Run training in a separate thread
    threading.Thread(target=train_model, daemon=True).start()     

def main_app():
    global root, prediction_label, learning_status_label, feedback_label  # Declare global variables
    
    root = tk.Tk()
    root.title("Server GUI")
    root.geometry("600x400")
    root.resizable(False, False)
    
    frame = tk.Frame(root)
    frame.pack(expand=True)
    
    label = tk.Label(frame, text="Server Options", font=("Arial", 14))
    label.pack(pady=20)
    
    button1 = tk.Button(frame, text="Running", command=function_one)
    button1.pack(pady=10)
    
    button2 = tk.Button(frame, text="Learning", command=function_two)
    button2.pack(pady=10)
    
    prediction_label = tk.Label(frame, text="Finger Angles", font=("Arial", 12), fg="blue")
    prediction_label.pack(pady=10)
    
        # Label for connections
    if conncetions_ips:
        label_text = f"connections: {conncetions_ips[-1]}"
    else:
        label_text = "connections: None"

    learning_status_label = tk.Label(frame, text=label_text, font=("Arial", 12), fg="red")
    learning_status_label.pack(pady=10)

    # Periodic label update
    def update_connection_label():
        if conncetions_ips:
            learning_status_label.config(text=f"connections: {conncetions_ips[-1]}")
        else:
            learning_status_label.config(text="connections: None")
        root.after(1000, update_connection_label)  # Schedule again

    update_connection_label()  # Start the loop

    root.mainloop()

# Splash Screen
splash_root = tk.Tk()
splash_root.title("Loading Program...")
splash_root.geometry("600x400")
splash_root.resizable(False, False)

frame = tk.Frame(splash_root)
frame.pack(expand=True)

splash_label = tk.Label(frame, text="Initializing...", font=("Arial", 12))
splash_label.pack(pady=20)

progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
progress_bar.pack(pady=20)

# Run loading animation and initialization in separate threads
threading.Thread(target=animate_loading, daemon=True).start()
threading.Thread(target=initialize_app, daemon=True).start()

splash_root.mainloop()
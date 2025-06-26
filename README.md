# AI-Driven-Prosthetic-Hand-System
An integrated system that leverages AI and real-time communication to control a prosthetic hand using muscle signals (EMG) and Machine learning. The system is composed of multiple interconnected modules built with Python, Blender, and communication protocols using socket programming.

**Project Structure and Components**
1. AI Model Pipeline
Purpose: Predict joint angles of fingers based on muscle signal input (EMG features).

Tech: Trained using XGBoost, with feature engineering and fine-tuning.

Inputs: 8-channel EMG signals.

Outputs: 14 predicted joint angles.

Features:

Model saving/loading.

Fine-tuning on user-specific data.

Performance metrics: RMSE, R², correlation.

2. Communication Layer (Server/Client)
Purpose: Real-time data exchange between the AI system and Blender visualization or an embedded device.

Protocol: TCP socket communication.

Features:

Threaded client/server architecture.

ACK-based flow control.

Event-driven message synchronization.

Queued data streaming.

3. Blender Hand Visualization
Purpose: Real-time simulation of hand motion based on AI predictions.

Tech: Blender scripting with Python and bpy API.

Features:

Armature-based bone rotation.

Smooth animation using keyframes.

Modular client for socket integration.

Uses a queue to synchronize with the server.

4. Desktop Application (GUI)
Purpose: Central user interface for running and controlling the system.

Tech: Tkinter for GUI.

Features:

Model inference and training control.

Progress feedback and status logging.

Splash screen with loading bar.

Seamless backend integration with server and AI model.

5. Data Management
Files:

deploy_data.csv: Real test data for inference.

new_sub.csv: Fine-tuning dataset.

finetuned_model.json: Serialized model.

Operations:

Data preprocessing.

Feature selection.

Label scaling and thresholding.

How to run the system:
First, you need to install (XGBoost, socket, tkinter, pandas, numpy, threading, queue) modules.

1- Run "app.py" using Python interpreter and wait until fully load the model.

2- Open "simulation.blend" (ensure you installed the Blender software)

3- Run the Python script opened in the file typically (client.py) inside Blender

4- Press the "Running" button in the app GUI.

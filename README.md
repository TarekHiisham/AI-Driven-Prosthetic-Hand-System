# AI-Driven Prosthetic Hand System

An AI-powered prosthetic hand that predicts finger joint angles using EMG signals. The system integrates machine learning with real-time 3D simulation using Blender and supports live control through a socket-based communication layer.

---

## Project Overview

This project represents an end-to-end pipeline for:
- Training an ML model to predict joint angles from EMG features.
- Sending real-time predictions to Blender for 3D animation.
- Supporting a feedback loop and online fine-tuning.

---

## Project Structure

```text
├── datasets/
│   ├── deploy_data.csv           # Processed test data for deployment
│   ├── new_sub.csv               # Dataset used for incremental learning
│   └── X_test.csv                # Optional input test features
├── models/
│   ├── Pretrained_xgbmodel.json  # Base model
│   └── finetuned_model.json      # finetuned model to desired generated data
├── libs/
│   ├── communicationlayer.py     # Socket server/client classes
│   └── modelpipeline.py          # ML pipeline: predict, train, save
├── client.py                     # Blender Python script for real-time animation                 
├── app.py                        # Main GUI application using Tkinter
└── README.md
```
---
## Prerequisites
Before running the project, ensure the following Python packages are installed:
```bash
pip install xgboost pandas numpy
```
---
## How to run the project

1. Launch the Server Application
- Open a terminal or Git Bash window.

Run the main application:
```bash
python app.py
```
- Wait for the loading screen to initialize the AI model completely.

- Once loaded, the main GUI window will appear.

2. Open the Blender File
- Launch Blender.

- Open the provided file: ```simulation.blend```.

3. Run the Blender Client Script
- Inside Blender, go to the Text Editor.

- Open the script file (typically named client.py and communicationlayer.py).

- Press Run Script.

4. Start the Prediction Stream
- Go back to the application GUI window.

- Click the “Running” button to start sending predictions to Blender.

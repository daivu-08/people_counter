Face Recognition People Counter
This project uses OpenCV and dlib to detect and recognize faces in a video stream, count the number of people, and store their appearance data in a SQLite database.
Prerequisites

Windows 10 (or another supported operating system)
Webcam

Installation Guide

Install Miniconda:

Download Miniconda for Windows from: https://docs.conda.io/en/latest/miniconda.html
Choose the Python 3.9 version for Windows 64-bit
Run the installer and follow the prompts
During installation, make sure to check the option "Add Miniconda3 to my PATH environment variable"


Open a new Command Prompt (to ensure the PATH is updated)
Create a new conda environment:
Copyconda create -n face_rec python=3.9
conda activate face_rec

Install required packages:
Copyconda install -c conda-forge dlib
pip install opencv-python numpy

Download the required dlib models:

Download shape_predictor_68_face_landmarks.dat
Download dlib_face_recognition_resnet_model_v1.dat
Extract these files (you may need a tool like 7-Zip)
Place the extracted .dat files in the project directory



Usage

Clone this repository:
Copygit clone https://github.com/your-username/face-recognition-people-counter.git
cd face-recognition-people-counter

Activate the conda environment:
Copyconda activate face_rec

Run the script:
Copypython people_counter_improved.py

The webcam feed will open in a new window. The script will detect faces, assign IDs to unique individuals, and display the count of people in the frame.
Press 'q' to quit the application.

Viewing the Database
To view the contents of the SQLite database after running the script, use the view_database.py script:
Copypython view_database.py
This will display the ID, first seen time, and last seen time for each detected individual.
Troubleshooting
If you encounter any issues:

Ensure all prerequisites are correctly installed.
Check that the dlib model files are in the correct location.
Verify that your webcam is working properly.
If you get a "DLL load failed" error, try installing Visual C++ Redistributable: https://aka.ms/vs/16/release/vc_redist.x64.exe

Contributing
Feel free to fork this repository and submit pull requests with any improvements or bug fixes.
License
This project is licensed under the MIT License - see the LICENSE file for details.
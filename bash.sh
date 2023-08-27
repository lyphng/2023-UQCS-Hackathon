#!/bin/bash

# Run npm install
cd extension/
npm install
cd ..

python3 install pandas numpy scikit-learn 

# Print welcome message
echo "Welcome to UQ Grade Predictor"

# Prompt user to paste academic transcript
echo "Please paste your academic transcript into the current folder and rename it to 'transcript.pdf'. "
echo "Press Enter to proceed."
read -p "Press Enter when you're ready."

# Prompt user for courses next semester
courses=()
while true; do
    read -p "Enter a course you will be doing next semester (or 'done' if finished): " course
    if [ "$course" == "done" ]; then
        break
    fi
    courses+=("$course")
done

# Run gradeReader.js
cd extension/
node gradeReader.js
cd ..

# Run gradepredictor.py
python3 grade_predictor.py "${courses[@]}"


# Script finished
echo "Script completed."

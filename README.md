# Execution

To execute run in the shell `./init.sh` this initializes `control.py` with some arguments. `control.py`  takes picture by calling `camera.py` when the button (connected at pin 13) is pressed. When the button at pin 11 is pressed, `images_to_text.py` extracts the text from the images. This can be done either offline with tesseract, or online using a google cloud service. 


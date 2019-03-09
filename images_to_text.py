# python3 images_to_text.py -f scanned_images -m online -o results
# Extracts text from images and saves it in home/pi/hackdemyk/text_results/{}.txt, {} specified by --output 
import argparse
import cv2
from PIL import Image
import pytesseract
import sh

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required = True,
        help = "Path of the folders of the images that were scanned")
ap.add_argument("-m", '--mode', default='offline',
        help ='Wether to translate with Tesseract or Google Vision API')
ap.add_argument("-o", "--output",
        help = "Name of the extracted text file saved in /home/pi/text_results/")
args = vars(ap.parse_args())

# Accesing folder with images
sh.cd('/home/pi/hackdemyk/{}'.format(args['folder']))
# creating a list of images to be processed
# ! assumes files are stored in order. Reversing the order to read from first to end
scanned_images = sh.ls().split()[::-1]


# Initializing text file
file = open("/home/pi/hackdemyk/text_results/{}.txt".format(args['output']),"w") 
  

for scanned_img in scanned_images:
    image = cv2.imread(scanned_img)

    #NOTE: Choosing Recognition Mode => Offline Tesseract / Online Google Vision
    if args['mode'] == 'offline':

        # Printing Recognized Text
        file.write(pytesseract.image_to_string(image = image))

    # Requires to have a google account and API key to google vision in folder keys
    if args['mode'] == 'online':  
        import os
        import io
        from google.cloud import vision
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/keys/annotations.json"

        def detect_document(path):
            global p
            word_storer = []
            
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()

            with io.open(path, 'rb') as image_file:
                content = image_file.read()
            image = vision.types.Image(content=content)
            response = client.document_text_detection(image=image)

            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    #print('\nBlock confidence: {}\n'.format(block.confidence))
                    for paragraph in block.paragraphs:
                        p = paragraph
                    # print('Paragraph confidence: {}'.format(
                        #    paragraph.confidence))
                    
                        for word in paragraph.words:
                            word_text = ''.join([
                                symbol.text for symbol in word.symbols
                            ])
                            #print('Word text: {} (confidence: {})'.format(
                                #word_text, word.confidence))
                            word_storer.append(word_text)
                        word_storer.append('\n\n')
                            #for symbol in word.symbols:
                                #print('\tSymbol: {} (confidence: {})'.format(
                                    #symbol.text, symbol.confidence))
            return(' '.join(word_storer))

        file.write(detect_document('/home/pi/hackdemyk/scanned_images/{}'.format(scanned_img)))

file.close() 
 


        

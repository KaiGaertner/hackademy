# pytesseract
# https://pypi.org/project/pytesseract/

# processes a given picture and returns a textblob
def ocr_scan(picture='../pics/test.png'):
	try:
		from PIL import Image
		from pytesseract import image_to_string
	except ImportError:
		import Image
	text = image_to_string(Image.open(picture))
	text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
	text.replace("'''","'")
	text.replace('"',"'")
	return text

# write text to file for further scenarios
def write_textfile(path='../texts/', name='testtesxt', text='Das ist ein Test'):
	with open(path+name+'.txt', 'w') as outfile:
		outfile.write(text)

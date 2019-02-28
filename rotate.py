from PIL import Image

def pil_rotate(name):
	im = Image.open(name)
	im.rotate(90).save(name.replace(".png","_rotate.png"))

pil_rotate("test.png")

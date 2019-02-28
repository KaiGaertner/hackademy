import picamera, time
with picamera.PiCamera() as camera:
	brightness=50
	contrast=65
	camera.color_effects = (128,128)
	camera.contrast=contrast
	camera.brightness = brightness
	camera.quality=100
	camera.start_preview()
	time.sleep(500)

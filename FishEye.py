
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2
import numpy as np
from math import sqrt



def get_fish_xn_yn(sourceX, sourceY, sourceRadius, k):
	"""
	Get normalized x, y pixel coordinates from the original image and return normalized
	x, y pixel coordinates in the destination fished image.
	"""
	if(1 + k * (sourceRadius ** 2) == 0):
		return sourceX / (1.01 + k * (sourceRadius ** 2)), sourceY / (1.01 + k * (sourceRadius ** 2))
	else:
		return sourceX / (1 + k * (sourceRadius ** 2)), sourceY / (1 + k * (sourceRadius ** 2))


# -----------------------------------------------------------------------------------

def fish(img, distortion_coefficient):
	"""
	:type img: numpy.ndarray

	:param distortion_coefficient: The amount of distortion to apply.

	:return: numpy.ndarray - the image with applied effect.
	"""

	k = distortion_coefficient

	# prepare array for dst image
	dstimg = np.zeros_like(img)

	# floats for calcultions
	w, h = float(img.shape[0]), float(img.shape[1])

	for x in range(len(dstimg)):
		for y in range(len(dstimg[x])):

			# normalize x and y to be in interval of [-1, 1]
			xnd, ynd = float((2 * x - w) / w), float((2 * y - h) / h)

			# get xn and yn distance from normalized center
			rd = sqrt(xnd ** 2 + ynd ** 2)

			xdu, ydu = get_fish_xn_yn(xnd, ynd, rd, k)

			# convert the normalized distorted xdn and ydn back to image pixels
			xu, yu = int(((xdu + 1) * w) / 2), int(((ydu + 1) * h) / 2)

			# if new pixel is in bounds copy from source pixel to destination pixel
			if 0 <= xu and xu < img.shape[0] and 0 <= yu and yu < img.shape[1]:
				dstimg[x][y] = img[xu][yu]

	return dstimg

def select_image():

	# get the distortion coefficient from the scale widget
	selection = var.get()
	label.config(text=selection)

	# open a file chooser dialog and allow the user to select an input image
	path = tkFileDialog.askopenfilename(title="Select Image",filetype =(("jpeg files",("*.jpg","*.jpeg")),("png files","*.png"),("all files","*.*")) )
	print(path)
	# ensure a file path was selected
	if len(path) > 0:
		# load the image from disk, convert it to grayscale, and detect
		# edges in it
		image = cv2.imread(path)

		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		print(selection)
		fisheye = fish(image,selection)

		# OpenCV represents images in BGR order; however PIL represents
		# images in RGB order, so we need to swap the channels

		# convert the images to PIL format...
		image = Image.fromarray(image)
		fisheye = Image.fromarray(fisheye)

		# ...and then to ImageTk format
		image = ImageTk.PhotoImage(image)
		fisheye = ImageTk.PhotoImage(fisheye)

		# update the pannels
		panelA.configure(image=image)
		panelB.configure(image=fisheye)
		panelA.image = image
		panelB.image = fisheye

# initialize the window toolkit along with the two image panels
root = Tk()
root.minsize(300,100)

panelA = Label()
panelB = Label()
panelA.pack(side="left", padx=10, pady=10)
panelB.pack(side="right", padx=10, pady=10)
selection = 0.0
root.title('FishEye')

var = DoubleVar()
scale = Scale(root, variable = var ,orient=HORIZONTAL,from_=-0.99, to=0.99,resolution=0.01)
scale.pack(anchor=CENTER,fill="both")

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="no", padx="10", pady="10")

# kick off the GUI
label = Label(root)
label.pack()

root.mainloop()


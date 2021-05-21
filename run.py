import coding
import image
import sys
def compress(path):
	f = open(path,'r+')
	text = f.read()
	frequency = {}
	for character in text:
		if not character in frequency:
			frequency[character] = 0
		frequency[character] += 1
	f.close()
	h = coding.Coding(frequency,path)
	h.compress()

def decompress(input,code_path):
	h = coding.Decoding(input,code_path)
	h.decompress()

def img_compress(path):
	ob = image.ImageCoding(path)
	ob.compress()

def img_decompress(input,code_path):
	ob = image.DecompImage(input,code_path)
	ob.decompress()

img_decompress("./Screenshot from 2019-10-18 18-43-09.bin","./Screenshot from 2019-10-18 18-43-09_codemap.bin")


from PIL import Image
import os
import coding
import pickle
class ImageCoding(coding.Coding):
   def __init__(self,path):
      self.path = path
      img = Image.open(path).convert('L')
      pixel_list = list(img.getdata())
      self.pixel_list = pixel_list
      self.freq = {}
      self.heap = []
      self.codes = {}
      self.reverse = {}
      self.reverse["sz"] = img.size
      self.reverse["md"] = img.mode


   def frequency(self):
      for character in self.pixel_list:
         if not character in self.freq:
            self.freq[character] = 0
         self.freq[character] +=1

   def compress(self):
      filename, extension = os.path.splitext(self.path)
      output_path = filename + ".bin"
      with open (output_path,'wb') as output:  
         self.frequency()
         self.build_priorityQ()
         self.build_huffman_tree()
         encoded_txt = self.code(self.pixel_list)
         padded_txt = self.padding(encoded_txt)
         arr = bytearray()
         for i in range(0,len(padded_txt),8):
            byte = padded_txt[i:i+8]
            arr.append(int(byte , 2))
         output.write(bytes(arr))
         with open (filename + "_codemap.bin" ,'wb') as out:
            for key in self.codes:
               self.reverse[self.codes[key]] = key
            self.reverse["ex"] = extension
            pickle.dump(self.reverse, out)

class DecompImage(coding.Decoding):
   def decode(self,encodedtxt,reverse):
      current_code=""
      decoded = []
      for bit in encodedtxt:
         current_code += bit
         if(current_code in reverse):
            pix = reverse[current_code]
            decoded.append(pix)
            current_code = ""
      return decoded

   def decompress(self):
      filename, extension = os.path.splitext(self.inp)
      with open (self.inp,'rb') as input,open (self.code_path,'rb') as code:
         bit_string = ""
         byte = input.read(1)
         while(len(byte) > 0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8,'0')
            bit_string += bits
            byte = input.read(1)
   
         encoded_text = self.remove_pad(bit_string)
         reverse = pickle.load(code)
         decoded = self.decode(encoded_text,reverse)
         im = Image.new(reverse["md"],reverse["sz"])
         im.putdata(decoded)
         im.save(filename + '1' + reverse["ex"])
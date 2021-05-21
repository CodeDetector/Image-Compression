import heapq
import pickle
import os
from functools import total_ordering
import shutil

class Coding:
   def __init__(self, dic, path):
      self.path = path
      self.freq = dic
      self.heap = []
      self.codes = {}
      self.reverse = {}
   
   '''heapq builds a min heap thus, the character with least frequncy will have the highest priority'''

   def build_priorityQ(self):            
      for key in self.freq:
	      node = HeapNode(key,self.freq[key])
	      heapq.heappush(self.heap, node)

   #Building the huffman tree by merging the frequencies of each two min frequencies
   def build_huffman_tree(self):
      while(len(self.heap)>1):
         node1 = heapq.heappop(self.heap)
         node2 = heapq.heappop(self.heap)

         mergedNode = HeapNode(None, node1.freq + node2.freq)
         mergedNode.leftchild = node1
         mergedNode.rightchild = node2
         heapq.heappush(self.heap, mergedNode)

   def walk_tree(self , root ,current_code):
      if(root == None):
         return
      if(root.key != None):
         self.codes[root.key] = current_code
         return
      self.walk_tree(root.leftchild ,current_code+"0")
      self.walk_tree(root.rightchild ,current_code +"1")

   def code(self,text):
      root = heapq.heappop(self.heap)
      current_code = ""
      self.walk_tree(root,current_code)
      encoded_text = ""
      for char in text:
         encoded_text += self.codes[char]
      return encoded_text


   def padding(self, encoded_text):
      extra_padding = 8 - len(encoded_text) % 8
      for i in range(extra_padding):
         encoded_text += "0"

      padded_info = "{0:08b}".format(extra_padding)
      encoded_text = padded_info + encoded_text
      return encoded_text
   
   def compress(self):
      filename, extension = os.path.splitext(self.path)
      dir_name = filename[filename.rfind("/") + 1:]
      dir_path = "./" + dir_name
      os.mkdir(dir_path)
      output_path = "./" + dir_name + "/" + dir_name + ".bin"
      with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
         text = file.read()
         self.build_priorityQ()
         self.build_huffman_tree()
         encoded_txt = self.code(text)
         padded_txt = self.padding(encoded_txt)
         arr = bytearray()
         for i in range(0,len(padded_txt),8):
            byte = padded_txt[i:i+8]
            arr.append(int(byte , 2))
         output.write(bytes(arr))
      code_path = "./" + dir_name + "/" + dir_name + "_codemap.bin"
      with open (code_path,'wb') as out:
         for key in self.codes:
            self.reverse[self.codes[key]] = key
         pickle.dump(self.reverse, out)


class Decoding:
   def __init__(self,inp,code_path):
      self.inp = inp
      self.code_path = code_path


   def remove_pad(self, padded_txt):
      padded_info = padded_txt[:8]
      extra_padding = int(padded_info, 2)
      padded_txt = padded_txt[8:] 
      encoded_text = padded_txt[:-1*extra_padding]

      return encoded_text

   def decode(self,encodedtxt,reverse):
      current_code=""
      decodedtxt=""
      for bit in encodedtxt:
         current_code += bit
         if(current_code in reverse):
            char = reverse[current_code]
            decodedtxt += char
            current_code = ""
      return decodedtxt
   
   def decompress(self):
      filename, extension = os.path.splitext(self.inp)
      out_path = "./" + filename[filename.rfind("/")+1:]
      with open (self.inp,'rb') as input ,open (out_path + "_decomp.txt" , 'w') as output,open (self.code_path,'rb') as code:
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
         output.write(decoded)

@total_ordering
class HeapNode:
   def __init__(self, key , freq):
      self.freq = freq
      self.key = key
      self.rightchild = None
      self.leftchild = None
   
   def __lt__(self, other):
      return self.freq < other.freq
   
   def __eq__(self ,other):
      if(other == None):
         return False
      return self.freq == other.freq
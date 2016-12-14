
from PIL import Image
import hashlib
import time
import os
from sklearn import svm
import numpy




im = Image.open("examples/47j17b.gif")
im2 = Image.new("P",im.size,255)
im = im.convert("P")

temp = {}

print im.histogram()

for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix == 220 or pix == 227: # these are the numbers to get
      im2.putpixel((y,x),0)
    

inletter = False
foundletter=False
start = 0
end = 0

letters = []


for y in range(im2.size[0]): # slice across
  for x in range(im2.size[1]): # slice down
    pix = im2.getpixel((y,x))
    if pix != 255:
      inletter = True

  if foundletter == False and inletter == True:
    foundletter = True
    start = y

  if foundletter == True and inletter == False:
    foundletter = False
    end = y
    letters.append((start,end))
  inletter=False

# New code is here. We just extract each image and save it to disk with
# what is hopefully a unique name
  
count = 0
ch=['a','b','c','d','e','f','g']
index=0
for letter in letters:
  m = hashlib.md5()
  im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
  m.update("%s%s"%(time.time(),count))
  #im3.save("./%s.gif"%(m.hexdigest()))
  im3.save("./"+ch[index]+".gif");
  index=index+1
  count += 1



path="iconset/"
dirList = os.listdir(path) 

s=[];
p=[];
si=[];
ar={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':65,'B':66,'C':67,'D':68,'E':69,'F':70,'G':71,'H':72,'I':73,'J':74,'K':75,'L':76,'M':77,'N':78,'O':79,'P':80,'Q':81,'R':82,'S':83,'T':84,'U':85,'V':86,'W':87,'X':88,'Y':89,'Z':90}
t=[]

i=0
for dir in dirList:
  if dir.find(".gif") != -1:
    im=Image.open(path+dir)
    t.append(ar[dir[0]])
    si=im.size
    s.append(si)
    List=list(im.getdata())
    if si[0] < 8 and si[1] == 22:
      l=len(List)
      cnt=0
      dif=8-si[0]
      while cnt<dif:
        k=0
        while k<22:
          List.append(0)
          k=k+1
        cnt=cnt+1

    m=si[0]
    n=si[1]
    if m*n > 176:
      k=m*n
      while k>176:
        List.pop()
        k=k-1
    
    p.append(List)
    i=i+1

  else :
    continue


#j=0
#for j in range(i):
#  print s[j]
#  print "\n"
#  print len(p[j])
#  print "\n\n"
#  print p[j]
#  print "\n\n"
#  j=j+1


X=p
Y=t
clf= svm.SVC()
clf.fit(X, Y)
i=0
while i<index:
  im=Image.open(ch[i]+".gif")
  print ch[i]+".gif"
  List=list(im.getdata())
  si=im.size
  if si[0] < 8 and si[1] == 22:
      l=len(List)
      cnt=0
      dif=8-si[0]
      while cnt<dif:
        k=0
        while k<22:
          List.append(0)
          k=k+1
        cnt=cnt+1

  m=si[0]
  n=si[1]
  if m*n > 176:
    k=m*n
    while k>176:
      List.pop()
      k=k-1
  pre=clf.predict(List)
  print pre
  im.show()
  i=i+1




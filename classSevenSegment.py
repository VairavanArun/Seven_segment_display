import cv2
import numpy as np

class SevenSegment:

    def __init__(self,len=100):
        l=int(len/2)
        w=int(l*0.1)
        self.L=len+20+2*w
        self.W=l+10+2*w
        self.bg=np.ones((self.L,self.W,3),dtype=np.uint8)
        self.bg=cv2.copyMakeBorder(self.bg,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])
        self.a=np.array([[w+25,w+20],[2*w+25,20],[l+25,20],[w+l+25,w+20],[l+25,2*w+20],[2*w+25,2*w+20]],dtype=np.int32)
        self.f=np.array([[w+20,w+25],[2*w+20,2*w+25],[2*w+20,l+25],[w+20,w+l+25],[20,l+25],[20,2*w+25]],dtype=np.int32)
        y=np.array([[0,l+10]]*6,dtype=np.int32)
        x=np.array([[l+10,0]]*6,dtype=np.int32)
        self.g=y+self.a
        self.d=y+self.g
        self.b=self.f+x
        self.e=self.f+y
        self.c=self.e+x
        self.segments=[self.a,self.b,self.c,self.d,self.e,self.f,self.g]
        self.numbers={}
        self.setNumbers()
        self.drawBorder()

    def setNumbers(self):
        self.numbers[0]=[self.segments[i] for i in range(6)]
        self.numbers[1]=[self.segments[i] for i in [1,2]]
        self.numbers[2]=[self.segments[i] for i in [0,1,6,4,3]]
        self.numbers[3]=[self.segments[i] for i in [0,1,6,2,3]]
        self.numbers[4]=[self.segments[i] for i in [5,6,1,2]]
        self.numbers[5]=[self.segments[i] for i in [0,5,6,2,3]]
        self.numbers[6]=[self.segments[i] for i in [0,5,6,2,3,4]]
        self.numbers[7]=[self.segments[i] for i in range(3)]
        self.numbers[8]=self.segments
        self.numbers[9]=[self.segments[i] for i in [0,1,2,5,6]]

    def drawBorder(self):
        l=[self.a,self.b,self.c,self.d,self.e,self.f,self.g]
        for pts in l:
            cv2.polylines(self.bg,[pts],True,(0,0,155),1)

    def display(self,num,show,img=-1):
        pts=self.numbers[num]
        try:
            if img==-1:
                I=self.bg.copy()
        except ValueError:
            I=img.copy()
        for pt in pts:
            cv2.fillPoly(I,[pt],(0,0,255))
        
        if show==0:
            return I
        cv2.imshow("Image",img)
        cv2.waitKey()
        cv2.destroyAllWindows()


    def timer(self,I=-1,obj=-1):
        try:
            if I==-1:
                I=self.bg
        except ValueError:
            pass
        if obj==-1:
            numbers=self.numbers
        else:
            numbers=obj.numbers
        for n in numbers:
            img=I.copy()
            for pts in numbers[n]:
                cv2.fillPoly(img,[pts],(0,0,255))
            cv2.imshow("Image",img)
            cv2.waitKey(1000)


class TwoDigitSS(SevenSegment):

     def __init__(self,len):
        self.one=SevenSegment(len)
        self.two=SevenSegment(len)
        offset=np.array([[self.one.W+40,0]]*6,dtype=np.int32)
        for i in range(7):
            self.two.segments[i]=self.two.segments[i]+offset
        self.two.setNumbers()
        self.bg=cv2.hconcat([self.one.bg,self.two.bg])
    
     def timer(self):
        for i in range(2):
            I=self.one.display(i,img=self.bg,show=0)
            super().timer(I,self.two)
        cv2.destroyAllWindows()
        

SS=TwoDigitSS(600)
SS.timer()

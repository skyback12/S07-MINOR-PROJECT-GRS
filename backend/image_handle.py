import cv2
import os

class ImageHandler:
    def __init__(self, folderpath, hs, ws):
        self.folderpath = folderpath
        self.hs, self.ws = hs, ws
        self.pathimages = sorted(os.listdir(folderpath), key=len)
        self.imgnumber = 0
        self.annotations = [[]]
        self.annotationnumber = 0
        self.annotationstart = False

    def load_image(self):
        pathFullImage = os.path.join(self.folderpath, self.pathimages[self.imgnumber])
        imgcurrent = cv2.imread(pathFullImage)
        return imgcurrent

    def resize_for_overlay(self, img):
        imgSmall = cv2.resize(img, (self.ws, self.hs))
        return imgSmall

    def overlay_image(self, imgcurrent, imgSmall):
        h, w, _ = imgcurrent.shape
        imgcurrent[0:self.hs, w-self.ws:w] = imgSmall
        return imgcurrent

    def update_annotations(self, indexFinger):
        if self.annotationstart:
            self.annotations[self.annotationnumber].append(indexFinger)
        else:
            self.annotationstart = True
            self.annotationnumber += 1
            self.annotations.append([indexFinger])

    def reset_annotations(self):
        self.annotations = [[]]
        self.annotationnumber = 0

    def clear_annotations(self):
        if self.annotations:
            self.annotations.clear()
            self.annotations.append([])
            self.annotationnumber = 0

    def draw_annotations(self, imgcurrent):
        for annotation in self.annotations:
            for i in range(1, len(annotation)):
                cv2.line(imgcurrent, annotation[i - 1], annotation[i], (0, 0, 200), 12)
        return imgcurrent

    def get_slide_count(self):
        return len(self.pathimages)
    
    def increment_slide(self):
        if self.imgnumber < len(self.pathimages) - 1:
            self.imgnumber += 1
            self.reset_annotations()

    def decrement_slide(self):
        if self.imgnumber > 0:
            self.imgnumber -= 1
            self.reset_annotations()
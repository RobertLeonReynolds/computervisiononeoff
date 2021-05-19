import cv2

class BackgroundDataCapture:
    def __init__(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index)
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        x = 30
        while x > 0:
            ret, img = self.cap.read()
            if ret:
                self.backSub.apply(img)
            x -= 1
    def get_largest_change(self):
        # Open Camera
        cap = self.cap
        backSub = self.backSub
        ret, img = cap.read()
        #if there is a return value
        if ret:
            cv2.imshow("Camera", img)
            key_pressed = cv2.waitKey(1)
            # If S is pressed
            if key_pressed == ord('s'):
                fgMask = backSub.apply(img)
                cv2.imshow("fg", fgMask)
                img = self.prep_image_for_contours(img)
                contours = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                sorted_contours = sorted(contours[0], key=lambda x: cv2.contourArea(x))
                # get the bb for the largest contour.
                bb = cv2.boundingRect(sorted_contours[-1])

                return img, bb
        print("Camera didn't open, check index")
        raise RuntimeError()
    def prep_image_for_contours(self, image):
        # There is a chance the mask is rather noisy, and not all the blobs connect.
        # I leave it to the reader to fix this
        return image
    def save_annotation(self, bb, detected_class, path):
        min_x = bb[0]
        min_y = bb[1]
        max_x = min_x + bb[2]
        max_y = min_y + bb[3]

        # Save the file in w.e format

        pass

    def save_image(self, img, path):
        cv2.imwrite(path, img)

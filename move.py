import glob
import os
import shutil

if __name__ == "__main__":
    look_for_images = 'C:/Users/Aldina/Desktop/dataset/textural_defect/cv_*.jpg'

    images = [file for file in glob.glob(look_for_images)]
    for img in images:
        path, ext1 = os.path.split(img)
        src = 'C:/Users/Aldina/Desktop/images/' + ext1
        if os.path.exists(img):
            print(src)
            shutil.move(img, 'C:/Users/Aldina/Desktop/cv_leather/textural_defect/' + ext1)

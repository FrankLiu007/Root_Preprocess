from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2

def cv2_to_qpixmap(cv_img):
    # Check the number of channels in the image
    if len(cv_img.shape) == 2:
        # Grayscale image
        height, width = cv_img.shape
        bytes_per_line = width
        q_image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    elif len(cv_img.shape) == 3:
        # Color image
        height, width, channels = cv_img.shape
        if channels == 3:
            # Convert BGR to RGB
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            bytes_per_line = 3 * width
            q_image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        elif channels == 4:
            # Convert BGRA to RGBA
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA)
            bytes_per_line = 4 * width
            q_image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
    else:
        raise ValueError("Unsupported image format")

    return QPixmap.fromImage(q_image)

def qpixmap_to_cv2(qpixmap):
    # Convert QPixmap to QImage
    qimage = qpixmap.toImage()
    
    # Get image dimensions
    width = qimage.width()
    height = qimage.height()
    
    # Check the format of the QImage
    if qimage.format() == QImage.Format_Grayscale8:
        # Grayscale image
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width)
        return arr
    elif qimage.format() == QImage.Format_RGB32:
        # RGB32 image
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # 4 channels: RGBA
        arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
        return arr
    elif qimage.format() == QImage.Format_RGB888:
        # RGB888 image
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)  # 3 channels: RGB
        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        return arr
    
    elif qimage.format() == QImage.Format_ARGB32_Premultiplied:

        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
        
        # ARGB (Qt Format_ARGB32_Premultiplied) 转换为 BGRA (OpenCV 格式)
        return cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)

    else:
        raise ValueError("Unsupported QImage format")
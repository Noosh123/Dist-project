import cv2
import numpy as np

def __process_image(image, operation):
    # Load the image
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    result = None
    # Perform the specified operation
    if operation == 'edge-detection':
        result = cv2.Canny(img, 100, 200)
    elif operation == 'color-inversion':
        result = cv2.bitwise_not(img)
    elif operation == 'gray-scale':
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif operation == 'blur':
        result = cv2.GaussianBlur(img, (15, 15), 0)
    elif operation == 'sharpen':
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        result = cv2.filter2D(img, -1, kernel)
    
    return result

def __save_result(result):
    # Send the result to the master node
    result_filename = f"result.jpg"  
    success = cv2.imwrite(result_filename, result)
    if not success:
        print("Failed to save result image")  
            

def process_main(image, operation):
    result = __process_image(image, operation)
    if result is not None:
        __save_result(result)
        return 1
    else:
        return 0

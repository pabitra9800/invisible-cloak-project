import cv2
import numpy as np
import time

# Function to capture the background image
def take_background(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    time.sleep(3) # Give the camera time to initialize

    background = None
    for i in range(30): # Try to capture a few frames to get a stable background
        ret, frame = cap.read()
        if ret:
            background = frame
            break # Exit loop once a frame is successfully captured
        time.sleep(0.1)

    cap.release() # Release the camera after capturing the background

    if background is None:
        print("Error: Could not capture a background frame. Please ensure camera is accessible.")
        return None
    else:
        # Flip the background image horizontally
        background = np.flip(background, axis=1)
        print("Background captured successfully!")
        return background

# Main function for the invisible cloak
def run_invisible_cloak():
    background = take_background(0) # Capture background using camera index 0

    if background is None:
        return # Exit if background capture failed

    cap = cv2.VideoCapture(0) # Open the camera for the real-time feed
    time.sleep(3) # Give the camera time to initialize

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range for the blue color in HSV
        lower_blue = np.array([100, 40, 40])
        upper_blue = np.array([140, 255, 255])

        # Create a mask to detect the blue color
        mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

        # Improve the mask with morphological operations
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        # Create an inverse mask to get everything except the blue color
        mask2 = cv2.bitwise_not(mask1)

        # Apply the masks
        # res1: pixels in the background where the blue color is detected in the current frame
        res1 = cv2.bitwise_and(background, background, mask=mask1)
        # res2: pixels in the current frame where the blue color is NOT detected
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)

        # Combine the two results
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Display the output
        cv2.imshow("Invisible Cloak", final_output)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    run_invisible_cloak()
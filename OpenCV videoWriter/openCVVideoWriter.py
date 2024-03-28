import cv2
cap = cv2.VideoCapture(0) # 0 represents the default camera, change it if you have multiple cameras

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error opening camera")
    

# Set the video's frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create a VideoWriter object to save the video
video_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))

# Check if the VideoWriter object is created successfully
if not video_writer.isOpened():
    print("Error opening video writer")
    
print("Camera open now")
while(True):
    # Capture frame
    ret, frame = cap.read()
    
    # Check if frame actually captured
    if not ret:
        print("ERROR CAPTURING FRAME")
        break
    
    # Display frame
    #cv2.imshow("Camera",frame)
    
    # Write frame to video file
    video_writer.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
                
# Release the camera and video writer
cap.release()
video_writer.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
print("Program finsihed")
# applix_test


### Basics:
-   UI → Gradio (Python)    
-   Structure → Input button, upload button, output image component, save button.
-   Code → Github ([https://github.com/kambleakash0/applix_test](https://github.com/kambleakash0/applix_test))
-   Hosting → Render.com ([https://applix-test.onrender.com](https://applix-test.onrender.com))

### Assumptions:
-   Only one image processing at a time.
-   The nut and bolt's center is at the image's center.
    
### Flow/Approach:
-   The user accesses the web app using the URL and captures an image.
-   Image data gets stored in the ‘tmp/’ directory as a PNG image upon clicking the upload button. With this step, the image processing starts.
-   The coordinates for the center of the image are calculated and three concentric circles with radius ratios of 3:5:9 are to be drawn to separate the areas where the bolt, nut, and bare metal lie on the image, respectively.
-   The image is converted to grayscale for edge detection and line detection. (Not Working)
-   The lines’ alignment is checked using the angles and deviations.
-   Based on the findings, the result is stored (Aligned, Misaligned, or No-Mark), and accordingly, the three concentric circles are colored.
-   The results are stored with the timestamp of the time when the save button was clicked and the result with the format ‘timestamp_result.png’ in the ‘saved_outputs/’ directory.

### Shortcomings:
-   Couldn’t get the edge detection to work properly.
-   Couldn’t implement the database-based result storage.
    
### Pending tasks/future improvements:
-   Can be made more robust.
-   Can improve the image processing part.
-   Can introduce LLMs as well.

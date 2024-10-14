import os
import cv2
import numpy as np
import gradio as gr
from PIL import Image

def input_image_select(input_img: gr.Image):
    input_img = Image.fromarray(input_img)
    input_img.save("tmp/saved_image.png")
    return gr.Button(interactive=True)

def input_image_clear():
    gr.Warning("Please provide an input image to start the process.")
    return gr.Button(interactive=False)

def upload_btn_click(input_img: gr.Image):
    # Load the image
    image = cv2.imread("tmp/saved_image.png")

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Compute the center of the image (center for the circles)
    center_x, center_y = width // 2, height // 2
    
    # Define the maximum radius as a proportion of the image size (e.g., half of the smallest dimension)
    max_radius = min(center_x, center_y)  # Take the smaller of the two to ensure the circles fit

    # Define the radius proportions (3:2:4)
    proportions = [3, 2, 4]
    total = sum(proportions)
    
    # Calculate the actual radii for each of the three concentric circles
    radius1 = (proportions[0] / total) * max_radius
    radius2 = (proportions[1] / total) * max_radius
    radius3 = (proportions[2] / total) * max_radius

    # Convert radii to integers
    radius1 = int(radius1)
    radius2 = int(radius2 + radius1)
    radius3 = int(radius3 + radius2)

    # Draw the three concentric circles
    # Circle 1 (innermost)
    cv2.circle(image, (center_x, center_y), radius1, (0, 255, 0), 2)  # Green circle
    # Circle 2 (middle)
    cv2.circle(image, (center_x, center_y), radius2, (255, 0, 0), 2)  # Blue circle
    # Circle 3 (outermost)
    cv2.circle(image, (center_x, center_y), radius3, (0, 0, 255), 2)  # Red circle

    # Show the image with the concentric circles
    cv2.imshow('Concentric Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save the image if needed
    cv2.imwrite('tmp/output_with_circles.jpg', image)

    return gr.Image(image, visible=True)

def save_btn_click(output_img: gr.Image):
    return

with gr.Blocks() as demo:
        
        demo.title = "Applix AI"
        gr.Markdown("# Applix AI demo")
        
        input_image = gr.Image(mirror_webcam=False)
        upload_btn = gr.Button("Upload", variant="secondary", interactive=False)
        output_image = gr.Image(visible=False)
        save_btn = gr.Button("Save results", variant="primary", visible=False)
        
        ## Event listener triggers for the input image
        # when input is given 
        input_image.input(
            fn = input_image_select, 
            inputs = [input_image], 
            outputs = [upload_btn]
        )
        # when input is cleared
        input_image.clear(
            fn=input_image_clear,
            inputs=[],
            outputs=[upload_btn]
        )
        
        ## Event listener for the upload button
        upload_btn.click(
            fn=upload_btn_click,
            inputs=[input_image],
            outputs=[output_image]
        )
        
        ## Event listener for the save button
        save_btn.click(
            fn=save_btn_click,
            inputs=[output_image],
            outputs=[]
        )
        

if __name__ == "__main__":
    
    # Gradio stuff starts here
    gr.close_all()
    demo.launch(
        debug=True,
        show_error=True,
        server_port=int(os.environ.get("PORT", 7860)),
    )
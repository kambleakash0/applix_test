import os
import cv2
import math

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

def detect_lines(image, edges, min_length=50, max_gap=10):
    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=min_length, maxLineGap=max_gap)
    return lines

def check_alignment(lines, center_x, center_y, radii, tolerance=0.1):
    if lines is None:
        return False, False  # No line detected
    
    # To check alignment, we will calculate the angle of the line and see if it's the same for all circles
    angles = []
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            # Compute angle of the line
            angle = math.atan2(y2 - y1, x2 - x1) * (180 / np.pi)
            angles.append(angle)
    
    # Compute the average angle and compare with others (check alignment)
    avg_angle = np.mean(angles)
    deviation = np.std(angles)
    
    # If deviation is within tolerance, consider lines as aligned
    aligned = deviation <= tolerance * avg_angle
    
    # Return whether lines are detected and whether they are aligned
    return True, aligned

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
    radii = [radius1, radius2, radius3]
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('grayscaled', gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    # print(edges)
    
    # Detect the white-ish thick lines using Hough Line Transform
    lines = detect_lines(image, edges)

    # Check if lines are detected and aligned
    line_detected, aligned = check_alignment(lines, center_x, center_y, radii)

    # Draw concentric circles and color them based on the results
    colors = [(0, 0, 255), (0, 0, 255), (0, 0, 255)]  # Default to red

    if line_detected:
        if aligned:
            colors = [(0, 255, 0), (0, 255, 0), (0, 255, 0)]  # Green for aligned
        else:
            colors = [(0, 255, 255), (0, 255, 255), (0, 255, 255)]  # Yellow for misaligned

    # Draw the circles
    for i, radius in enumerate(radii):
        cv2.circle(image, (center_x, center_y), radius, colors[i], 2)

    # # Show the image with the concentric circles
    # cv2.imshow('Concentric Circles', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the image if needed
    cv2.imwrite("tmp/output_with_circles.png", image)

    return [gr.Image("tmp/output_with_circles.png", visible=True), gr.Button(visible=True)]


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
    input_image.input(fn=input_image_select, inputs=[input_image], outputs=[upload_btn])
    # when input is cleared
    input_image.clear(fn=input_image_clear, inputs=[], outputs=[upload_btn])

    ## Event listener for the upload button
    upload_btn.click(fn=upload_btn_click, inputs=[input_image], outputs=[output_image, save_btn])

    ## Event listener for the save button
    save_btn.click(fn=save_btn_click, inputs=[output_image], outputs=[])


if __name__ == "__main__":

    # Gradio stuff starts here
    gr.close_all()
    demo.launch(
        debug=True,
        show_error=True,
        server_port=int(os.environ.get("PORT", 7860)),
    )

import gradio as gr

def welcome(name):
    return f"Welcome to Gradio, {name}!"

def input_image_select(input_image, upload_btn):
    
    if input_image.select:
        upload_btn(interactive=True)

with gr.Blocks() as demo:
        
        demo.title = "Applix AI"
        gr.Markdown("# Applix AI demo")
        
        input_image = gr.Image(mirror_webcam=False)
        upload_btn = gr.Button("Upload", variant="secondary", interactive=False)
        output_image = gr.Image("Output image will appear here.", visible=False)
        
        # Event listener triggers for the input image
        input_image.input()
        

if __name__ == "__main__":
    
    
    
    demo.launch()
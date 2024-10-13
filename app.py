import gradio as gr

def input_image_select():
    return gr.Button(interactive=True)

def input_image_clear():
    gr.Warning("Please provide an input image to start the process.")
    return gr.Button(interactive=False)

def upload_btn_click(input_img: gr.Image):
    return gr.Image(input_img, visible=True)

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
            # inputs = [input_image], 
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
    demo.launch()
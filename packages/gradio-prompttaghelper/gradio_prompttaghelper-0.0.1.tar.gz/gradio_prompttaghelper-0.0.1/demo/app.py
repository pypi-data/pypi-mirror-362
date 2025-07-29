#
# demo/app.py
#
import gradio as gr
from gradio_prompttaghelper import PromptTagHelper 

# Example data structure for the tags and groups
TAG_DATA = {
    "Quality": [
        "best quality", "masterpiece", "high resolution", "4k", "8k", 
        "sharp focus", "detailed", "photorealistic"
    ],
    "Lighting": [
        "cinematic lighting", "volumetric lighting", "god rays", 
        "golden hour", "studio lighting", "dramatic lighting"
    ],
    "Style": [
        "anime style", "oil painting", "concept art", "fantasy", 
        "steampunk", "vaporwave", "line art"
    ],
    "Negative Prompts": [
        "blurry", "noisy", "low resolution", "low quality", "watermark",
        "text", "bad anatomy", "extra limbs", "disfigured"
    ]
}

with gr.Blocks() as demo:
    gr.Markdown("# Prompt Tag Helper Demo")
    gr.Markdown("Click on the tags below to add them to the prompt textboxes.")

    with gr.Row():
        with gr.Column(scale=2): # Give more space to the textboxes
            # Create the target Textbox and give it a unique `elem_id`.
            positive_prompt_box = gr.Textbox(
                label="Positive Prompt",
                placeholder="Click tags from 'Prompt Keywords' to add them here...",
                lines=5,
                elem_id="positive-prompt-textbox" # This ID must be unique
            )
            negative_prompt_box = gr.Textbox(
                label="Negative Prompt",
                placeholder="Click tags from 'Negative Keywords' to add them here...",
                lines=5,
                elem_id="negative-prompt-textbox" # This ID must be unique
            )

        with gr.Column(scale=1): # Give less space to the helpers
            # Create an instance of the PromptTagHelper for the Positive Prompt box.
            PromptTagHelper(
                label="Prompt Keywords",
                value={k: v for k, v in TAG_DATA.items() if "Negative" not in k},
                target_textbox_id="positive-prompt-textbox"
            )
            
            # Create another instance for the Negative Prompt box.
            PromptTagHelper(
                label="Negative Keywords",
                value={"Negative Prompts": TAG_DATA["Negative Prompts"]},
                target_textbox_id="negative-prompt-textbox",
                min_width=150
            )

if __name__ == '__main__':
    demo.launch()
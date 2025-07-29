
import gradio as gr
from app import demo as app
import os

_docs = {'PromptTagHelper': {'description': "A custom component that displays groups of clickable tags to help build prompts.\nWhen a tag is clicked, it's appended to a target Textbox component.\nThis component does not have a submittable value itself.", 'members': {'__init__': {'value': {'type': 'typing.Optional[typing.Dict[str, typing.List[str]]][\n    typing.Dict[str, typing.List[str]][\n        str, typing.List[str][str]\n    ],\n    None,\n]', 'default': 'None', 'description': 'A dictionary where keys are group names and values are lists of tags.'}, 'target_textbox_id': {'type': 'str | None', 'default': 'None', 'description': 'The `elem_id` of the `gr.Textbox` component to target. Required.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component, displayed above the groups.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, the component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'The relative size of the component compared to others in a `gr.Row` or `gr.Column`.'}, 'min_width': {'type': 'int | None', 'default': 'None', 'description': 'The minimum-width of the component in pixels.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If False, the component will not be wrapped in a container.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings to assign as CSS classes to the component.'}}, 'postprocess': {'value': {'type': 'typing.Optional[typing.Dict[str, typing.List[str]]][\n    typing.Dict[str, typing.List[str]][\n        str, typing.List[str][str]\n    ],\n    None,\n]', 'description': None}}, 'preprocess': {'return': {'type': 'Any', 'description': None}, 'value': None}}, 'events': {}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'PromptTagHelper': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_prompttaghelper`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

A fast prompt generator based on tagged words
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_prompttaghelper
```

## Usage

```python
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
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PromptTagHelper`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PromptTagHelper"]["members"]["__init__"], linkify=[])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: Any
) -> typing.Optional[typing.Dict[str, typing.List[str]]][
    typing.Dict[str, typing.List[str]][
        str, typing.List[str][str]
    ],
    None,
]:
    return value
```
""", elem_classes=["md-custom", "PromptTagHelper-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          PromptTagHelper: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()

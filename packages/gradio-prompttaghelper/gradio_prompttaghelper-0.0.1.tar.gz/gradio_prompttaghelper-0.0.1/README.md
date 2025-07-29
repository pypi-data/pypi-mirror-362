---
tags: [gradio-custom-component, ]
title: gradio_prompttaghelper
short_description: A fast prompt generator based on tagged words
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_prompttaghelper`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  

A fast prompt generator based on tagged words

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

## `PromptTagHelper`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
typing.Optional[typing.Dict[str, typing.List[str]]][
    typing.Dict[str, typing.List[str]][
        str, typing.List[str][str]
    ],
    None,
]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A dictionary where keys are group names and values are lists of tags.</td>
</tr>

<tr>
<td align="left"><code>target_textbox_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The `elem_id` of the `gr.Textbox` component to target. Required.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component, displayed above the groups.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, the component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The relative size of the component compared to others in a `gr.Row` or `gr.Column`.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The minimum-width of the component in pixels.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, the component will not be wrapped in a container.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings to assign as CSS classes to the component.</td>
</tr>
</tbody></table>




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
 

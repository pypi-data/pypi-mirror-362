---
tags: [gradio-custom-component, HighlightedText]
title: gradio_markdownlabel
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_markdownlabel`
<a href="https://pypi.org/project/gradio_markdownlabel/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_markdownlabel"></a>  

Python library for easily interacting with trained machine learning models

## Installation

```bash
pip install gradio_markdownlabel
```

## Usage

```python

import gradio as gr
from gradio_markdownlabel import MarkdownLabel

# Create a comprehensive example with rich markdown content and multiple highlights
example_data = {
    "markdown_content": """# AI and Machine Learning Research Report

## Introduction

This document explores the rapidly evolving field of **artificial intelligence** and its various applications in modern technology. The study focuses on *machine learning* techniques and their impact on different industries.

## Key Technologies

### Deep Learning
*Deep learning* represents a subset of machine learning that uses **neural networks** with multiple layers. This approach has revolutionized areas such as:

- Computer vision
- Natural language processing
- Speech recognition

### Natural Language Processing
**Natural language processing** (NLP) enables computers to understand and interpret human language. Key applications include:

1. Text analysis
2. Sentiment analysis
3. Language translation

## Applications

The integration of **computer vision** in autonomous vehicles has transformed the automotive industry. Similarly, **reinforcement learning** has shown remarkable success in gaming and robotics.

## Conclusion

As **artificial intelligence** continues to advance, we expect to see more sophisticated applications of these technologies across various domains.
""",
    "highlights": [
        {
            "term": "artificial intelligence",
            "title": "Artificial Intelligence (AI)",
            "content": "**Artificial Intelligence** refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. AI systems can perform tasks that typically require human intelligence, such as:\n\n- Visual perception\n- Speech recognition\n- Decision-making\n- Language translation\n\nAI is broadly categorized into:\n1. **Narrow AI** - designed for specific tasks\n2. **General AI** - hypothetical AI with human-level cognitive abilities",
            "category": "Core Technology",
            "color": "#e3f2fd"
        },
        {
            "term": "machine learning",
            "title": "Machine Learning (ML)",
            "content": "**Machine Learning** is a subset of AI that focuses on the development of algorithms that can learn and improve from experience without being explicitly programmed.\n\n### Types of Machine Learning:\n- **Supervised Learning**: Learning with labeled examples\n- **Unsupervised Learning**: Finding patterns in unlabeled data\n- **Reinforcement Learning**: Learning through interaction with environment\n\n### Applications:\n- Recommendation systems\n- Fraud detection\n- Medical diagnosis\n- Autonomous vehicles",
            "category": "Core Technology", 
            "color": "#f3e5f5"
        },
        {
            "term": "deep learning",
            "title": "Deep Learning",
            "content": "**Deep Learning** is a specialized subset of machine learning that uses artificial neural networks with multiple layers (deep neural networks) to model and understand complex patterns.\n\n### Key Characteristics:\n- Multiple hidden layers\n- Automatic feature extraction\n- Hierarchical learning\n\n### Popular Architectures:\n- Convolutional Neural Networks (CNNs)\n- Recurrent Neural Networks (RNNs)\n- Transformers\n\n### Applications:\n- Image recognition\n- Natural language processing\n- Speech synthesis",
            "category": "Advanced Technique",
            "color": "#e8f5e8"
        },
        {
            "term": "neural networks",
            "title": "Neural Networks",
            "content": "**Neural Networks** are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information.\n\n### Components:\n- **Input Layer**: Receives data\n- **Hidden Layers**: Process information\n- **Output Layer**: Produces results\n\n### Types:\n- Feedforward networks\n- Recurrent networks\n- Convolutional networks\n\nNeural networks learn by adjusting the weights of connections between neurons based on training data.",
            "category": "Architecture",
            "color": "#fff3e0"
        },
        {
            "term": "natural language processing",
            "title": "Natural Language Processing (NLP)",
            "content": "**Natural Language Processing** combines computational linguistics with machine learning to enable computers to understand, interpret, and generate human language.\n\n### Core Tasks:\n- **Tokenization**: Breaking text into words/sentences\n- **Part-of-speech tagging**: Identifying grammatical roles\n- **Named entity recognition**: Identifying people, places, organizations\n- **Sentiment analysis**: Determining emotional tone\n\n### Modern Approaches:\n- Transformer models (BERT, GPT)\n- Attention mechanisms\n- Pre-trained language models",
            "category": "Application Domain",
            "color": "#fce4ec"
        },
        {
            "position": [615, 632],
            "title": "Computer Vision (Position-based)",
            "content": "**Computer Vision** highlighted by character position rather than term matching. This demonstrates precise control over highlighting specific text segments.\n\n### Position-based Benefits:\n- Exact character-level precision\n- No ambiguity with similar terms\n- Works with any text, including special characters\n- Useful for pre-processed documents",
            "category": "Position Highlight",
            "color": "#ffeb3b"
        },
        {
            "term": "computer vision",
            "title": "Computer Vision", 
            "content": "**Computer Vision** is a field of AI that enables machines to interpret and understand visual information from the world, mimicking human vision capabilities.\n\n### Key Tasks:\n- **Object Detection**: Locating objects in images\n- **Image Classification**: Categorizing images\n- **Semantic Segmentation**: Pixel-level understanding\n- **Face Recognition**: Identifying individuals\n\n### Applications:\n- Autonomous vehicles\n- Medical imaging\n- Security systems\n- Augmented reality",
            "category": "Application Domain",
            "color": "#e1f5fe"
        },
        {
            "term": "reinforcement learning",
            "title": "Reinforcement Learning (RL)",
            "content": "**Reinforcement Learning** is a type of machine learning where an agent learns to make decisions by performing actions in an environment to maximize cumulative reward.\n\n### Key Concepts:\n- **Agent**: The learner/decision maker\n- **Environment**: The world the agent interacts with\n- **Actions**: Choices available to the agent\n- **Rewards**: Feedback from the environment\n- **Policy**: Strategy for choosing actions\n\n### Famous Applications:\n- Game playing (AlphaGo, OpenAI Five)\n- Robotics control\n- Trading algorithms\n- Resource allocation",
            "category": "Learning Paradigm",
            "color": "#f1f8e9"
        },
        {
            "position": [169, 190],
            "title": "Machine Learning (Position)",
            "content": "This **machine learning** instance is highlighted using position-based highlighting at characters 169-190.\n\n### Position Highlighting Use Cases:\n- Academic paper annotations\n- Legal document markup\n- Code documentation\n- Precise text analysis\n\nPosition-based highlighting ensures exact text selection without ambiguity.",
            "category": "Position Demo",
            "color": "#e8eaf6"
        }
    ]
}

with gr.Blocks(title="Markdown Label Demo") as demo:
    gr.Markdown("# MarkdownLabel Component Demo")
    gr.Markdown("This demo showcases the MarkdownLabel component with **both term-based and position-based** interactive highlighting and detailed side panel.")
    
    gr.Markdown("Includes both term-based (e.g., 'artificial intelligence') and position-based highlighting (yellow highlights).")
    MarkdownLabel(
        value=example_data,
        label="AI Research Report - Mixed Highlighting",
        show_side_panel=True,
        panel_width="350px",
        interactive=True
    )
    
    # Simple position-based example
    simple_example = {
        "markdown_content": "The quick **brown fox** jumps over the lazy dog. This is a simple example.",
        "highlights": [
            {
                "position": [4, 9],  # "quick"
                "title": "Quick (Position 4-9)",
                "content": "Highlighted using exact character positions 4-9.",
                "category": "Position Demo",
                "color": "#ffeb3b"
            },
            {
                "term": "brown fox",
                "title": "Brown Fox (Term Match)",
                "content": "Highlighted using term matching.",
                "category": "Term Demo", 
                "color": "#e3f2fd"
            },
            {
                "position": [35, 43],  # "the lazy"
                "title": "The Lazy (Position 35-43)", 
                "content": "Another position-based highlight at characters 35-43.",
                "category": "Position Demo",
                "color": "#f3e5f5"
            }
        ]
    }
    
    gr.Markdown("## Position vs Term Highlighting Comparison")
    gr.Markdown("This example shows the difference between position-based (yellow/purple) and term-based (blue) highlighting.")
    MarkdownLabel(
        value=simple_example,
        label="Simple Position vs Term Example",
        show_side_panel=True,
        panel_width="300px",
        interactive=True
    )

if __name__ == "__main__":
    demo.launch()

```

## `MarkdownLabel`

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
dict | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Dictionary containing markdown_content and highlights array. If a function is provided, the function will be called each time the app loads to set the initial value of this component.</td>
</tr>

<tr>
<td align="left"><code>show_side_panel</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to show the detailed information side panel.</td>
</tr>

<tr>
<td align="left"><code>panel_width</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"300px"</code></td>
<td align="left">Width of the side panel (CSS value like "300px", "25%", etc.).</td>
</tr>

<tr>
<td align="left"><code>edit_mode</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"split"</code></td>
<td align="left">Layout for editing mode - "split" (side-by-side), "tabs", or "overlay".</td>
</tr>

<tr>
<td align="left"><code>show_preview</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to show live preview in edit mode.</td>
</tr>

<tr>
<td align="left"><code>markdown_editor</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"textarea"</code></td>
<td align="left">Type of markdown editor - "textarea" or "codemirror" (future).</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | I18nData | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | tuple[int | str, ...] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render.</td>
</tr>

<tr>
<td align="left"><code>preserved_by_key</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>"value"</code></td>
<td align="left">A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, the component will be editable allowing users to modify markdown content.</td>
</tr>

<tr>
<td align="left"><code>rtl</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, will display the text in right-to-left direction.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the MarkdownLabel changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `select` | Event listener for when the user selects or deselects the MarkdownLabel. Uses event data gradio.SelectData to carry `value` referring to the label of the MarkdownLabel, and `selected` to refer to state of the MarkdownLabel. See EventData documentation on how to use this event data |
| `edit` | This listener is triggered when the user edits the MarkdownLabel (e.g. image) using the built-in editor. |
| `submit` | This listener is triggered when the user presses the Enter key while the MarkdownLabel is focused. |
| `clear` | This listener is triggered when the user clears the MarkdownLabel using the clear button for the component. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the value as a dictionary with markdown_content and highlights.
- **As input:** Should return, expects a dictionary with 'markdown_content' and 'highlights' keys.

 ```python
 def predict(
     value: dict | None
 ) -> dict | None:
     return value
 ```
 


import gradio as gr
from app import demo as app
import os

_docs = {'MarkdownLabel': {'description': 'Displays markdown-formatted text with interactive term highlighting and detailed side panel.\n\nThis component allows for rich markdown content with clickable term highlights that display\ndetailed information in a side panel.', 'members': {'__init__': {'value': {'type': 'dict | Callable | None', 'default': 'None', 'description': 'Dictionary containing markdown_content and highlights array. If a function is provided, the function will be called each time the app loads to set the initial value of this component.'}, 'show_side_panel': {'type': 'bool', 'default': 'True', 'description': 'Whether to show the detailed information side panel.'}, 'panel_width': {'type': 'str', 'default': '"300px"', 'description': 'Width of the side panel (CSS value like "300px", "25%", etc.).'}, 'edit_mode': {'type': 'str', 'default': '"split"', 'description': 'Layout for editing mode - "split" (side-by-side), "tabs", or "overlay".'}, 'show_preview': {'type': 'bool', 'default': 'True', 'description': 'Whether to show live preview in edit mode.'}, 'markdown_editor': {'type': 'str', 'default': '"textarea"', 'description': 'Type of markdown editor - "textarea" or "codemirror" (future).'}, 'label': {'type': 'str | I18nData | None', 'default': 'None', 'description': 'the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': "in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render."}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': "A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor."}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, the component will be editable allowing users to modify markdown content.'}, 'rtl': {'type': 'bool', 'default': 'False', 'description': 'If True, will display the text in right-to-left direction.'}}, 'postprocess': {'value': {'type': 'dict | None', 'description': "Expects a dictionary with 'markdown_content' and 'highlights' keys"}}, 'preprocess': {'return': {'type': 'dict | None', 'description': 'Passes the value as a dictionary with markdown_content and highlights.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the MarkdownLabel changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the MarkdownLabel. Uses event data gradio.SelectData to carry `value` referring to the label of the MarkdownLabel, and `selected` to refer to state of the MarkdownLabel. See EventData documentation on how to use this event data'}, 'edit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user edits the MarkdownLabel (e.g. image) using the built-in editor.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the MarkdownLabel is focused.'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the MarkdownLabel using the clear button for the component.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'MarkdownLabel': []}}}

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
# `gradio_markdownlabel`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_markdownlabel/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_markdownlabel"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
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
    "markdown_content": \"\"\"# AI and Machine Learning Research Report

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
\"\"\",
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
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `MarkdownLabel`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["MarkdownLabel"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["MarkdownLabel"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the value as a dictionary with markdown_content and highlights.
- **As output:** Should return, expects a dictionary with 'markdown_content' and 'highlights' keys.

 ```python
def predict(
    value: dict | None
) -> dict | None:
    return value
```
""", elem_classes=["md-custom", "MarkdownLabel-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          MarkdownLabel: [], };
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

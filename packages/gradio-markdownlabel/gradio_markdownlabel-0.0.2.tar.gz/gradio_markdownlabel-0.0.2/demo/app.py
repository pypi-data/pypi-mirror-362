
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

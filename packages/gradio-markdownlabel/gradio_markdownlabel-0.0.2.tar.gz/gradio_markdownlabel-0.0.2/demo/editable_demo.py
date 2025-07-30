#!/usr/bin/env python3

import gradio as gr
from gradio_markdownlabel import MarkdownLabel

# Sample data for the editable demo
sample_data = {
    "markdown_content": """# Editable Document Example

## Introduction

This document demonstrates the **editable functionality** of the MarkdownLabel component. You can click the "Edit" button to modify this content.

## Features

- **Real-time editing**: Changes appear live in preview mode
- **Highlight preservation**: Existing highlights remain intact
- **Multiple edit modes**: Split view, tabs, and overlay options
- Position-based highlighting support

## Try Editing

1. Click the **Edit** button above
2. Modify this text in the editor
3. See live preview (in split mode)
4. Save or cancel your changes

Feel free to experiment with the content!
""",
    "highlights": [
        {
            "term": "editable functionality",
            "title": "Editable Functionality",
            "content": "This feature allows users to modify markdown content directly in the interface with real-time preview.",
            "category": "feature",
            "color": "#e3f2fd"
        },
        {
            "position": [200, 220],  # "MarkdownLabel component"
            "title": "MarkdownLabel Component",
            "content": "The main component that renders markdown with interactive highlights and editing capabilities.",
            "category": "component",
            "color": "#f3e5f5"
        },
        {
            "term": "Real-time editing",
            "title": "Real-time Editing",
            "content": "Changes in the editor are immediately reflected in the preview pane, providing instant feedback.",
            "category": "feature",
            "color": "#e8f5e8"
        },
        {
            "position": [450, 470],  # "Split view, tabs, and"
            "title": "Edit Modes",
            "content": "Different layout options for the editing interface: split view shows editor and preview side-by-side, tabs separate them, and overlay mode provides full-screen editing.",
            "category": "ui",
            "color": "#fff3e0"
        }
    ]
}

def handle_content_change(value):
    """Handle content changes (only on save)"""
    print(f"Content saved: {len(value['markdown_content'])} characters")
    return value

def handle_edit_start(value):
    """Handle when user starts editing"""
    print("User started editing")

def handle_save(value):
    """Handle when user saves changes"""
    print("Changes saved!")
    gr.Info("Document saved successfully!")
    return value

def handle_cancel(value):
    """Handle when user cancels editing"""
    print("Edit cancelled")
    gr.Info("Changes cancelled")
    return gr.update()

def load_sample_content():
    """Load sample content"""
    # Return data for both components (split and tabs editors)
    return sample_data, sample_data


with gr.Blocks(title="Editable MarkdownLabel Demo") as demo:
    gr.Markdown("# Editable MarkdownLabel Component Demo")
    gr.Markdown("This demo showcases the **interactive editing capabilities** of the MarkdownLabel component.")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("## Split View Mode (Default)")
            gr.Markdown("Editor and preview side-by-side when editing.")
            
            editor_split = MarkdownLabel(
                value=sample_data,
                interactive=True,
                edit_mode="split",
                show_preview=True,
                label="Split View Editor",
                show_side_panel=True,
                panel_width="300px"
            )
            
            # Event handlers for split view
            # Note: Removed real-time change handler to prevent infinite loops
            # Changes are now handled only on explicit save via submit event
            editor_split.edit(handle_edit_start, inputs=[editor_split])
            editor_split.submit(handle_save, inputs=[editor_split], outputs=[editor_split])
            editor_split.clear(handle_cancel, inputs=[editor_split])
            
        with gr.Column(scale=1):
            gr.Markdown("## Tab Mode")
            gr.Markdown("Switch between edit and preview tabs.")
            
            editor_tabs = MarkdownLabel(
                value=sample_data,
                interactive=True,
                edit_mode="tabs",
                show_preview=True,
                label="Tab View Editor",
                show_side_panel=False
            )
            
            # Event handlers for tab view
            # Note: Only handling submit (save) events to prevent loops
            editor_tabs.submit(handle_save, inputs=[editor_tabs], outputs=[editor_tabs])
    
    with gr.Row():
        gr.Markdown("## Control Buttons")
        
    with gr.Row():
        load_btn = gr.Button("📄 Load Sample", variant="secondary")
        
    # Button event handlers
    load_btn.click(load_sample_content, outputs=[editor_split, editor_tabs])
    
    with gr.Row():
        gr.Markdown("## Non-Interactive (Read-Only) Version")
        
    # Read-only version for comparison
    readonly_viewer = MarkdownLabel(
        value=sample_data,
        interactive=False,  # Read-only mode
        label="Read-Only Viewer",
        show_side_panel=True,
        panel_width="250px"
    )
    
    gr.Markdown("""
    ## How to Use
    
    1. **Start Editing**: Click the "✏️ Edit" button on any interactive component
    2. **Edit Content**: Modify the markdown text in the editor
    3. **Live Preview**: See changes in real-time (split mode) or switch to preview tab
    4. **Save Changes**: Click "💾 Save" to confirm and apply your changes
    5. **Cancel Changes**: Click "❌ Cancel" to discard changes and revert
    6. **Interact with Highlights**: Click on highlighted terms to see details in the side panel
    
    ## Features Demonstrated
    
    - ✅ **Interactive editing** with explicit save/cancel workflow
    - ✅ **Multiple edit modes**: Split view and tabs
    - ✅ **Live preview** with real-time markdown rendering (visual only)
    - ✅ **Highlight preservation** during editing
    - ✅ **Manual save workflow** - changes are applied only when you save
    - ✅ **Event handling** for edit, save (submit), and cancel events
    - ✅ **Mixed highlighting** with both term-based and position-based highlights
    
    ## Important Notes
    
    - **Changes are NOT auto-saved** - you must click "💾 Save" to apply changes
    - **Live preview** is for visual feedback only - actual content updates on save
    - **Cancel** reverts all changes made since editing started
    """)

if __name__ == "__main__":
    demo.launch()
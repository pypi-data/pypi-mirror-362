#!/usr/bin/env python3
"""
Example API Usage for Editable MarkdownLabel Component
Shows the recommended event handling pattern to avoid infinite loops.
"""

import gradio as gr
from gradio_markdownlabel import MarkdownLabel

def main():
    # Sample document with highlights
    document = {
        "markdown_content": """# Project Documentation

## Overview

This is an **editable document** that demonstrates the MarkdownLabel component's capabilities.

## Features

- Interactive editing with save/cancel workflow
- Position-based and term-based highlighting  
- Live preview during editing
- Manual save to prevent accidental changes

## Instructions

Click "Edit" to modify this content, then "Save" to apply changes.
""",
        "highlights": [
            {
                "term": "editable document", 
                "title": "Editable Document",
                "content": "Documents that can be modified by users through the interface.",
                "category": "feature",
                "color": "#e3f2fd"
            },
            {
                "position": [200, 220],  # "MarkdownLabel component"
                "title": "MarkdownLabel Component",
                "content": "The custom Gradio component for displaying markdown with interactive highlights.",
                "category": "technical",
                "color": "#f3e5f5"  
            }
        ]
    }

    # Event handlers - NO change handler to prevent loops
    def on_edit_start(data):
        """Called when user clicks Edit button"""
        print(f"📝 User started editing document")
        # Could initialize editing session, backup content, etc.
        return gr.update()  # No changes to component
    
    def on_save(data):
        """Called when user clicks Save button"""
        print(f"💾 Document saved with {len(data['markdown_content'])} characters")
        # Here you could:
        # - Validate the content
        # - Save to database  
        # - Update version history
        # - Send notifications
        gr.Info("Document saved successfully!")
        return data  # Return the saved data
    
    def on_cancel(data):
        """Called when user clicks Cancel button"""
        print(f"❌ Edit cancelled")
        gr.Info("Changes discarded")
        return gr.update()  # No changes needed

    def on_highlight_select(selection_data):
        """Called when user clicks a highlight"""
        print(f"🎯 Highlight selected: {selection_data}")
        return gr.update()

    # Create the interface
    with gr.Blocks(title="MarkdownLabel API Example") as demo:
        gr.Markdown("# MarkdownLabel API Usage Example")
        gr.Markdown("Demonstrates proper event handling without infinite loops.")
        
        # The component
        editor = MarkdownLabel(
            value=document,
            interactive=True,           # Enable editing
            edit_mode="split",          # Split view: editor + preview
            show_preview=True,          # Show live preview
            show_side_panel=True,       # Show highlight details
            panel_width="350px",
            label="Interactive Document Editor"
        )
        
        # Event handlers - IMPORTANT: No .change() handler during editing!
        editor.edit(
            fn=on_edit_start,
            inputs=[editor]
            # No outputs = no component update
        )
        
        editor.submit(  # This is the "Save" button
            fn=on_save,
            inputs=[editor],
            outputs=[editor]  # Update component with saved data
        )
        
        editor.clear(  # This is the "Cancel" button  
            fn=on_cancel,
            inputs=[editor]
            # No outputs = revert handled internally
        )
        
        editor.select(  # Highlight selection
            fn=on_highlight_select,
            inputs=[editor]
        )
        
        # Status display
        gr.Markdown("""
        ### Event Flow:
        1. **Edit**: User clicks edit → `on_edit_start()` called
        2. **Type**: User types → Only visual preview updates (no events)
        3. **Save**: User clicks save → `on_save()` called → Changes applied  
        4. **Cancel**: User clicks cancel → `on_cancel()` called → Changes reverted
        
        ### Key Points:
        - ❌ **DON'T** use `.change()` handlers during editing (causes loops)
        - ✅ **DO** use `.submit()` for save actions 
        - ✅ **DO** use `.clear()` for cancel actions
        - ✅ **DO** use `.edit()` for edit start actions
        - ✅ **DO** use `.select()` for highlight interactions
        """)

    return demo

if __name__ == "__main__":
    demo = main()
    demo.launch()
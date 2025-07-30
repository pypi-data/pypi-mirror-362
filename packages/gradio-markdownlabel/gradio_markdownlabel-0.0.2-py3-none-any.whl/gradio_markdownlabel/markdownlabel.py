"""gr.HighlightedText() component."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Union

from gradio_client.documentation import document

from gradio.components.base import Component
from gradio.data_classes import GradioModel, GradioRootModel
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class HighlightDefinition(GradioModel):
    term: str = ""
    position: list[int] = []  # [start, end] character positions
    title: str = ""
    content: str = ""
    category: str = ""
    color: str = ""


class MarkdownData(GradioModel):
    markdown_content: str
    highlights: list[HighlightDefinition] = []


class MarkdownLabelData(GradioRootModel):
    root: MarkdownData


class MarkdownLabel(Component):
    """
    Displays markdown-formatted text with interactive term highlighting and detailed side panel.
    
    This component allows for rich markdown content with clickable term highlights that display
    detailed information in a side panel.
    """

    data_model = MarkdownLabelData
    EVENTS = [Events.change, Events.select, Events.edit, Events.submit, Events.clear]

    def __init__(
        self,
        value: dict | Callable | None = None,
        *,
        show_side_panel: bool = True,
        panel_width: str = "300px",
        edit_mode: str = "split",
        show_preview: bool = True,
        markdown_editor: str = "textarea",
        label: str | I18nData | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
        interactive: bool | None = None,
        rtl: bool = False,
    ):
        """
        Parameters:
            value: Dictionary containing markdown_content and highlights array. If a function is provided, the function will be called each time the app loads to set the initial value of this component.
            show_side_panel: Whether to show the detailed information side panel.
            panel_width: Width of the side panel (CSS value like "300px", "25%", etc.).
            edit_mode: Layout for editing mode - "split" (side-by-side), "tabs", or "overlay".
            show_preview: Whether to show live preview in edit mode.
            markdown_editor: Type of markdown editor - "textarea" or "codemirror" (future).
            label: the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render.
            preserved_by_key: A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor.
            interactive: If True, the component will be editable allowing users to modify markdown content.
            rtl: If True, will display the text in right-to-left direction.
        """
        self.show_side_panel = show_side_panel
        self.panel_width = panel_width
        self.edit_mode = edit_mode
        self.show_preview = show_preview
        self.markdown_editor = markdown_editor
        self.rtl = rtl
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
            value=value,
            interactive=interactive,
        )
        self._value_description = "a dictionary with 'markdown_content' string and 'highlights' array containing term definitions."

    def example_payload(self) -> Any:
        return {
            "markdown_content": "# Sample Document\n\nThis contains **artificial intelligence** and *machine learning* terms.",
            "highlights": [
                {
                    "term": "artificial intelligence",
                    "title": "Artificial Intelligence",
                    "content": "AI refers to computer systems that can perform tasks typically requiring human intelligence.",
                    "category": "technology",
                    "color": "#e3f2fd"
                },
                {
                    "position": [74, 90],
                    "title": "Machine Learning",
                    "content": "ML is a subset of AI that focuses on algorithms that learn from data.",
                    "category": "technology",
                    "color": "#f3e5f5"
                }
            ]
        }

    def example_value(self) -> Any:
        return {
            "markdown_content": "# Sample Document\n\nThis contains **artificial intelligence** and *machine learning* terms.",
            "highlights": [
                {
                    "term": "artificial intelligence",
                    "title": "Artificial Intelligence",
                    "content": "AI refers to computer systems that can perform tasks typically requiring human intelligence.",
                    "category": "technology",
                    "color": "#e3f2fd"
                },
                {
                    "position": [74, 90],
                    "title": "Machine Learning",
                    "content": "ML is a subset of AI that focuses on algorithms that learn from data.",
                    "category": "technology",
                    "color": "#f3e5f5"
                }
            ]
        }

    def preprocess(
        self, payload: MarkdownLabelData | None
    ) -> dict | None:
        """
        Parameters:
            payload: An instance of MarkdownLabelData
        Returns:
            Passes the value as a dictionary with markdown_content and highlights.
        """
        if payload is None:
            return None
        return payload.root.model_dump()

    def postprocess(
        self, value: dict | None
    ) -> MarkdownLabelData | None:
        """
        Parameters:
            value: Expects a dictionary with 'markdown_content' and 'highlights' keys
        Returns:
            An instance of MarkdownLabelData
        """
        if value is None:
            return None
        
        if not isinstance(value, dict):
            raise ValueError(
                "Expected a dictionary with keys 'markdown_content' and 'highlights' "
                "for the value of the MarkdownLabel component."
            )
        
        # Ensure required keys exist
        markdown_content = value.get("markdown_content", "")
        highlights = value.get("highlights", [])
        
        # Validate highlights structure
        processed_highlights = []
        for highlight in highlights:
            if isinstance(highlight, dict):
                processed_highlights.append(HighlightDefinition(
                    term=highlight.get("term", ""),
                    position=highlight.get("position", []),
                    title=highlight.get("title", ""),
                    content=highlight.get("content", ""),
                    category=highlight.get("category", ""),
                    color=highlight.get("color", "")
                ))
        
        markdown_data = MarkdownData(
            markdown_content=markdown_content,
            highlights=processed_highlights
        )
        
        return MarkdownLabelData(root=markdown_data)

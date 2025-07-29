from gradio.components.base import Component


class PromptTagHelper(Component):
    """
    A custom component that displays groups of clickable tags to help build prompts.
    When a tag is clicked, it's appended to a target Textbox component.
    This component does not have a submittable value itself.
    """
    EVENTS = []

    def __init__(
        self,
        value: Dict[str, List[str]] | None = None,
        *,
        target_textbox_id: str | None = None,
        label: str | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        scale: int | None = None,
        min_width: int | None = None,
        container: bool = True,
        elem_classes: list[str] | str | None = None,
        
        **kwargs,
    ):
        """
        Initializes the PromptTagHelper component.

        Parameters:
            value: A dictionary where keys are group names and values are lists of tags.
            target_textbox_id: The `elem_id` of the `gr.Textbox` component to target. Required.
            label: The label for this component, displayed above the groups.
            visible: If False, the component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM.
            scale: The relative size of the component compared to others in a `gr.Row` or `gr.Column`.
            min_width: The minimum-width of the component in pixels.
            container: If False, the component will not be wrapped in a container.
            elem_classes: An optional list of strings to assign as CSS classes to the component.
        """
        if target_textbox_id is None:
            raise ValueError("The 'target_textbox_id' parameter is required for the PromptTagHelper component.")

        self.target_textbox_id = target_textbox_id
        
        # Call the parent constructor with all the arguments it understands.
        super().__init__(
            label=label,
            visible=visible,
            elem_id=elem_id,
            value=value,
            scale=scale,
            min_width=min_width,
            container=container,
            elem_classes=elem_classes,
            **kwargs,
        )
   
    def preprocess(self, payload: Any) -> Any:
        """This component does not process input from the user, so this is a no-op."""
        return None

    def postprocess(self, value: Dict[str, List[str]] | None) -> Dict[str, List[str]] | None:
        """Passes the tag group dictionary (received as 'value') to the frontend."""
        if value is None:
            return {}
        return value

    def api_info(self) -> Dict[str, Any]:
        """The API info for the component."""
        return {"type": "object", "description": "A dictionary of string-to-string-list mappings for tag groups."}

    def example_payload(self) -> Any:
        """Returns an example of the data that this component expects as its value."""
        return {
            "Quality": ["best quality", "high resolution"],
            "Style": ["anime", "photorealistic"],
            "Negative": ["blurry", "noisy"]
        }
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component

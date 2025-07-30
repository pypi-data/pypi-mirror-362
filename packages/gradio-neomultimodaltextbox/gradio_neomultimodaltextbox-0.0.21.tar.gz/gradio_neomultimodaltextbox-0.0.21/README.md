---
tags: [gradio-custom-component, MultimodalTextbox]
title: gradio_neomultimodaltextbox
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_neomultimodaltextbox`
<a href="https://pypi.org/project/gradio_neomultimodaltextbox/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_neomultimodaltextbox"></a>  

Python library for Gradio custom component MultimodalTextbox

## Installation

```bash
pip install gradio_neomultimodaltextbox
```

## Usage

```python
import gradio as gr
from gradio_neomultimodaltextbox import NeoMultimodalTextbox


example = NeoMultimodalTextbox().example_value()


def identity(i):
    return i


with gr.Blocks() as demo:
    box1 = NeoMultimodalTextbox(
        file_count="multiple",
        value={"text": "zouzou", "files": []},
        interactive=True,
    )  # interactive version of your component
    box2 = NeoMultimodalTextbox(
        upload_btn=False, interactive=False, stop_btn=True, audio_btn=True, stop_audio_btn=True
    )  # static version of your component
    box1.submit(fn=identity, inputs=box1, outputs=box2)

if __name__ == "__main__":
    demo.launch()

```

## `NeoMultimodalTextbox`

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
str | dict[str, str | list] | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Default value to show in NeoMultimodalTextbox. A string value, or a dictionary of the form {"text": "sample text", "files": [{path: "files/file.jpg", orig_name: "file.jpg", url: "http://image_url.jpg", size: 100}]}. If callable, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>file_types</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">List of file extensions or types of files to be uploaded (e.g. ['image', '.json', '.mp4']). "file" allows any file to be uploaded, "image" allows only image files to be uploaded, "audio" allows only audio files to be uploaded, "video" allows only video files to be uploaded, "text" allows only text files to be uploaded.</td>
</tr>

<tr>
<td align="left"><code>file_count</code></td>
<td align="left" style="width: 25%;">

```python
Literal["single", "multiple", "directory"]
```

</td>
<td align="left"><code>"single"</code></td>
<td align="left">if single, allows user to upload one file. If "multiple", user uploads multiple files. If "directory", user uploads all files in selected directory. Return type will be list for each file in case of "multiple" or "directory".</td>
</tr>

<tr>
<td align="left"><code>lines</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>1</code></td>
<td align="left">minimum number of line rows to provide in textarea.</td>
</tr>

<tr>
<td align="left"><code>max_lines</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>20</code></td>
<td align="left">maximum number of line rows to provide in textarea.</td>
</tr>

<tr>
<td align="left"><code>placeholder</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">placeholder hint to provide behind textarea.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.</td>
</tr>

<tr>
<td align="left"><code>info</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">additional component description, appears below the label in smaller font. Supports markdown / HTML syntax.</td>
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
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.</td>
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
<td align="left"><code>autofocus</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.</td>
</tr>

<tr>
<td align="left"><code>autoscroll</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.</td>
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
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>

<tr>
<td align="left"><code>text_align</code></td>
<td align="left" style="width: 25%;">

```python
Literal["left", "right"] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">How to align the text in the textbox, can be: "left", "right", or None (default). If None, the alignment is left if `rtl` is False, or right if `rtl` is True. Can only be changed if `type` is "text".</td>
</tr>

<tr>
<td align="left"><code>rtl</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.</td>
</tr>

<tr>
<td align="left"><code>upload_btn</code></td>
<td align="left" style="width: 25%;">

```python
str | bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>submit_btn</code></td>
<td align="left" style="width: 25%;">

```python
str | bool | None
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, will not show a submit button. If a string, will use that string as the submit button text.</td>
</tr>

<tr>
<td align="left"><code>stop_btn</code></td>
<td align="left" style="width: 25%;">

```python
str | bool | None
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, will show a stop button (useful for streaming demos). If a string, will use that string as the stop button text.</td>
</tr>

<tr>
<td align="left"><code>loading_message</code></td>
<td align="left" style="width: 25%;">

```python
str
```

</td>
<td align="left"><code>"... Loading files ..."</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>audio_btn</code></td>
<td align="left" style="width: 25%;">

```python
str | bool | None
```

</td>
<td align="left"><code>False</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>stop_audio_btn</code></td>
<td align="left" style="width: 25%;">

```python
str | bool | None
```

</td>
<td align="left"><code>False</code></td>
<td align="left">None</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the NeoMultimodalTextbox changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `input` | This listener is triggered when the user changes the value of the NeoMultimodalTextbox. |
| `select` | Event listener for when the user selects or deselects the NeoMultimodalTextbox. Uses event data gradio.SelectData to carry `value` referring to the label of the NeoMultimodalTextbox, and `selected` to refer to state of the NeoMultimodalTextbox. See EventData documentation on how to use this event data |
| `submit` | This listener is triggered when the user presses the Enter key while the NeoMultimodalTextbox is focused. |
| `focus` | This listener is triggered when the NeoMultimodalTextbox is focused. |
| `blur` | This listener is triggered when the NeoMultimodalTextbox is unfocused/blurred. |
| `stop` | This listener is triggered when the user reaches the end of the media playing in the NeoMultimodalTextbox. |
| `upload` | This listener is triggered when the user uploads a file into the NeoMultimodalTextbox. |
| `stream` | This listener is triggered when the user streams the NeoMultimodalTextbox. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes text value and list of file(s) as a {dict} into the function.
- **As input:** Should return, expects a {dict} with "text" and "files", both optional. The files array is a list of file paths or URLs.

 ```python
 def predict(
     value: MultimodalValue | None
 ) -> MultimodalValue | str | None:
     return value
 ```
 

## `MultimodalValue`
```python
class MultimodalValue(TypedDict):
    text: NotRequired[str]
    files: NotRequired[list[str]]
```

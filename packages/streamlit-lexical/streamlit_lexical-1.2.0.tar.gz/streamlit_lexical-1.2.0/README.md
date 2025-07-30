# streamlit_lexical

Streamlit component that allows you to use Meta's [Lexical](https://lexical.dev/) as a rich text plugin. 

## Installation instructions

```sh
pip install streamlit-lexical
```

## Usage instructions

```python
import streamlit as st

from streamlit_lexical import streamlit_lexical

markdown = streamlit_lexical(value="initial value in **markdown**",
                             placeholder="Enter some rich text", 
                             height=800,
                             debounce=500,
                             key='1234', 
                             on_change=None
                            )


st.markdown(rich_text_dict)
```

## Development instructions

After cloning the github repo...

In __init__.py, set:
```python
RELEASE = False
```
And you can test out the example.py with your changes by doing the following:

```sh
cd streamlit_lexical/frontend
npm install (or yarn install)
npm run start # Start the Webpack dev server
```

Then, in a separate terminal, run:
```python
pip install -e .
streamlit run example.py
```

Further, to build the package (after making changes/adding features), you can install it locally like: 
```sh
cd streamlit_lexical/frontend
npm install (or yarn install)
npm run build
cd ../..
pip install -e ./
```

Make sure the __init__.py file RELEASE is set to True in this case. 
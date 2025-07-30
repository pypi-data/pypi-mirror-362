"""Utils to show the DVC graph in streamlit.

The DVC parser is not used at the moment but will be useful in the future.
"""

import subprocess

import streamlit.components.v1 as components


def graph_container() -> None:
    """Display the DVC graph in streamlit."""
    command = ["dvc", "dag", "--mermaid"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = result.stdout
    mermaid(output)


def mermaid(code: str) -> None:
    """Render a mermaid graph in streamlit."""
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: "default", themeVariables: {{ fontSize: "12px" }} }});
        </script>
        """,
        height=350,
        scrolling=True,
    )

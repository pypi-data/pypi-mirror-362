# viewer.py
class JSONViewerPage:
    def __init__(self, data):
        self.data = data

    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {"padding": "10px", "height": "100%", "boxSizing": "border-box"},
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "content": "JSON Viewer",
                            "style": {"marginBottom": "10px"}
                        }
                    },
                    {
                        "type": "tree_viewer",
                        "props": {
                            "id": "jsonTree",
                            "data": self.data,
                            "expand_all": False,
                            "theme": "light",
                        }
                    },
                ]
            }
        }


def preview_json(data, title="Cacao JSON Viewer", width=800, height=600):
    """
    Preview JSON data in a desktop window.

    Args:
        data: JSON data to display (dict, list, or any JSON-serializable object)
        title: Window title (default: "Cacao JSON Viewer")
        width: Window width (default: 800)
        height: Window height (default: 600)
    
    Note:
        This function now includes runtime protection to prevent infinite loops.
        However, it's still recommended to wrap calls in `if __name__ == '__main__':`
        for best practices:
        
        Example:
            import json
            from cacao_json_viewer import preview_json  # New simplified import
            
            def main():
                with open("data.json", "r") as f:
                    data = json.load(f)
                preview_json(data, title="My JSON")
            
            if __name__ == "__main__":
                main()
    """
    import sys
    
    # Prevent infinite loops in framework reload scenarios
    if hasattr(sys, '_cacao_viewer_running'):
        print("Warning: Cacao JSON Viewer is already running. Ignoring duplicate call.")
        return
    
    sys._cacao_viewer_running = True
    
    try:
        from cacao import App

        app = App()
        viewer = JSONViewerPage(data)

        @app.mix("/")
        def home():
            return viewer.render()

        app.brew(
            type="desktop",
            title=title,
            width=width,
            height=height,
            resizable=True,
            fullscreen=False,
        )
    finally:
        if hasattr(sys, '_cacao_viewer_running'):
            delattr(sys, '_cacao_viewer_running')


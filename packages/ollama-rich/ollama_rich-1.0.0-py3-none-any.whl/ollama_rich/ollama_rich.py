from ollama import Client
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console()

class OllamaRichClient:
    def __init__(self, host=''):
        self.client = Client(host=host)

    def chat_and_display(self, model, messages):
        response = self.client.chat(
            model=model,
            stream=True,
            messages=messages,
        )

        full_content = ""
        with Live(Markdown(full_content), console=console, refresh_per_second=2) as live:
            for chunk in response:
                full_content += chunk['message']['content']
                live.update(Markdown(full_content))


    def chat(self, model, messages):
        with console.status("[bold green]Thinking...", spinner="dots"):
            response = self.client.chat(
                model=model,
                stream=False,
                messages=messages,
            )
        return Markdown(response['message']['content'])
    
    def models(self):
        try:
            return self.client.list()
        except ConnectionError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return []
        
    def models_name_list(self):
        try:
            models = self.client.list()
            return [model.get('model') for model in models.get('models', [])]
        except ConnectionError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return []

    def model_info(self, model):
        try:
            models = self.client.list()
            for m in models.get('models', []):
                if m.get('model') == model:
                    return m
            console.print(f"[bold red]Model '{model}' not found.[/bold red]")
            return {}
        except ConnectionError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return {}


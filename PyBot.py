import discord
from discord import app_commands
import io
import contextlib

class PythonBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = PythonBot()

@bot.tree.command(name="pycode", description="Executes Python code snippets in total safety")
@app_commands.describe(code="Enter the Python code to execute")
async def execute_python_code(interaction: discord.Interaction, code: str):
    await interaction.response.defer()
    stdout_captured = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_captured):
            safe_builtins = {"__builtins__": __import__('builtins').__dict__.copy()}

            safe_builtins["__builtins__"].pop("eval", None)
            safe_builtins["__builtins__"].pop("exec", None)
            safe_builtins["__builtins__"].pop("__import__", None)

            exec(code, safe_builtins, {})
        
        output = stdout_captured.getvalue()
        
        if not output.strip():
            output = "Code executed successfully, but no output was generated."
            
    except Exception as e:
        output = f"{type(e).__name__}: {e}"

    final_response = f"**Executed Code:**\n```python\n{code}\n```\n**Output:**\n```text\n{output}\n```"

    if len(final_response) > 2000:
        final_response = final_response[:1990] + "\n...[Output truncated due to character limit]```"

    await interaction.followup.send(final_response)

bot.run("MTU1NDU1MjQzNTA5MDEzNzE3OQ.GzmKL2.DSZGgB40OJg3Pq3zhZsBP6SJuFZntlcR-UFdMQ")
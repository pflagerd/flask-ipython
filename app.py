from flask import Flask, render_template_string, request
from IPython.terminal.embed import InteractiveShellEmbed
from io import StringIO
import sys

app = Flask(__name__)

# Initialize an IPython embedded shell
ipython_shell = InteractiveShellEmbed(banner1="Welcome to IPython Console!\n", exit_msg="Exiting IPython Console...\n")

# Redirect standard output to capture IPython outputs
output_stream = StringIO()
sys.stdout = output_stream

# Define a basic HTML template with a scrollable console
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IPython Console</title>
    <style>
        body { font-family: Arial, sans-serif; }
        #console {
            width: 90%;
            height: 70vh;
            border: 1px solid #333;
            padding: 10px;
            overflow-y: scroll;
            background-color: #f9f9f9;
            color: #333;
            white-space: pre-wrap;
        }
        #input {
            width: 90%;
            padding: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>IPython Interactive Console</h1>
    <div id="console">{{ output }}</div>
    <form action="/" method="post">
        <input id="input" name="command" placeholder="Enter command" autofocus>
        <button type="submit">Execute</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global output_stream

    if request.method == "POST":
        # Get command from the form and execute in IPython shell
        command = request.form.get("command", "")
        if command:
            ipython_shell.run_cell(command)

        # Capture output and clear the stream
        output = output_stream.getvalue()
        output_stream.truncate(0)
        output_stream.seek(0)
    else:
        output = "Type your commands below:\n"

    # Render the HTML template with console output
    return render_template_string(html_template, output=output)

if __name__ == "__main__":
    app.run(debug=True)


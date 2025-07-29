import click
import ast
from explainlike5.llm import explain_with_openai, explain_with_openrouter

@click.command()
@click.argument('file')
@click.option('--function', '-f', help="Name of the function to explain")
def main(file, function):
    click.echo("You passed the file path: {}".format(file))

    if function:
        click.echo("You want to explain the function: {}".format(function))
        function_code, error = extract_function_code(file, function)
        if error:
            click.echo(f"Error: {error}")
        else:
            click.echo("Function code:\n" + function_code)
            explain, error = explain_with_openrouter(function_code)

            if error:
                click.echo(f"Error: {error}")
            else:
                click.echo("\n🧠 Here's the explanation:\n")
                click.echo(explain)

    else:
        functions = find_functions(file)
        click.echo("Finding functions in the file...")

        for name in functions:
            click.echo("Function found: {}".format(name))

def find_functions(file):
    with open(file, 'r') as f:
        content = f.read()

    tree = ast.parse(content)
    functions = [   
        node.name for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    return functions

def extract_function_code(file, function):
    with open(file, 'r') as f:
        content = f.read()

    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            return ast.get_source_segment(content, node), None

    return None, f"Function '{function}' not found."

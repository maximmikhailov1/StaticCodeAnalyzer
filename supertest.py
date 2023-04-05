import re
import ast

code = open('main.py').read()
tree = ast.parse(code)
print(ast.dump(tree))
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        print(node.names[0].name)

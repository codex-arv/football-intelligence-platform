import nbformat

path = "data_artifacts/dataingestion2.ipynb"

nb = nbformat.read(path, as_version=4)

for cell in nb.cells:
    cell.outputs = []
    cell.execution_count = None

nb.metadata = {}

nbformat.write(nb, path)

print("Notebook cleaned successfully:", path)
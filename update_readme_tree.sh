#!/bin/bash

# Generate the directory tree
tree_output=$(tree -I '.git|.venv|__pycache__|node_modules')

# Insert the tree into README.md
awk -v tree="$tree_output" '
  BEGIN { in_tree=0 }
  /```scss/ { in_tree=1; print; print tree; next }
  in_tree && /```/ { in_tree=0; next }
  !in_tree { print }
' README.md > README.tmp && mv README.tmp README.md

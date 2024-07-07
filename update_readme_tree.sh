#!/bin/bash

# Generate the directory tree
tree_output=$(tree -I '.git|.venv|__pycache__|node_modules')

# Insert the tree into README.md and remove sections between markers
awk -v tree="$tree_output" '
  /## Project Structure/,/```scss/ {
    if (/```scss/) {
      print "```scss"
      print tree
      in_target_section=0
    }
    if (!in_target_section) {
      in_target_section=1
      next
    }
    next
  }
  /```/,0 {
    if (/```/) {
      print "```"
      in_target_section=0
    }
    if (!in_target_section) {
      in_target_section=1
      next
    }
    next
  }
  { if (!in_target_section) print }
' README.md > README.tmp && mv README.tmp README.md

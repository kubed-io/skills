---
description: Draw a new diagram on its own page of the draw.io diagram you have open.
argument-hint: "<what to draw>"
---
Draw this on a new page of the draw.io diagram I have open: $ARGUMENTS

Read the drawio skill first and the file under its
`references/diagrams/` that matches this kind of diagram, if there is one. Write the page as XML and
load it with one `import-diagram` in `new-page` mode, named after what it shows. Check it once as XML,
then tell me the page name and anything you had to guess.

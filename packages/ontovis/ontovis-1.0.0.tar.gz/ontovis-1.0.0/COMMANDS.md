# `ontovis`

Visualize and analyze WissKI pathbuilder definitions

**Usage**:

```console
$ ontovis [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `render`: Render a graphical representation of a...
* `stats`: Provide a set of key network analytical...

## `ontovis render`

Render a graphical representation of a pathbuilder definition.

Use `--template` to select a builtin template, or use `--template-custom` to
pass your own template.


The builtin templates are:

* no_groups (default): render only the ontology-classes and omit grouping
  into fields and path-groups.

* no_fields: group the ontology classes into path-groups, omit fields.

* full: group classes into fields, and fields into path-groups. **Warning:**
  the resulting representation can become very dense.

To pass a custom template using `--template-custom`, use
[jinja2](https://jinja.palletsprojects.com/en/stable/templates/)
to author a template.

Your template will have to work with the parser&#x27;s intermediate
representation; pass the `--raw` flag to see this.

**Usage**:

```console
$ ontovis render [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: The pathbuilder XML-dump. Can be a local or remote (http(s)) resource.  [required]

**Options**:

* `--template [no_groups|no_fields|full]`: The builtin template to use for rendering the pathbuilder.  [default: no_groups]
* `--template-custom PATH`: Custom jinja2-template for rendering the pathbuilder; use this option to render to other languages than DOT.
* `--save FILENAME`: In addition to printing to the screen, save the output to the specified file.
* `--skip-disabled / --include-disabled`: Skip path definitions that are disabled, or include disabled paths in the rendering.  [default: skip-disabled]
* `-r, --raw`: Dump the raw parse-tree; useful for inspecting the structure when authoring custom templates.
* `--help`: Show this message and exit.

## `ontovis stats`

Provide a set of key network analytical measures for a graph.

The graph must be provided in graphviz&#x27; dot-format; `ontovis render` can do this, so you can pipe its output into here:
```
ontovis render ... | ontovis stats -
```

**Usage**:

```console
$ ontovis stats [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: The graph to analyze, in DOT format. You can pass a filename, or use &#x27;-&#x27; to read from standard input.  [required]

**Options**:

* `--n INTEGER`: Number of top-results to include in rankings  [default: 3]
* `--help`: Show this message and exit.


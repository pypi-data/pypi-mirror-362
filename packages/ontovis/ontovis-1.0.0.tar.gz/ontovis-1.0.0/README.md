# Ontovis
[![Publish](https://github.com/AM-Digital-Research-Environment/ontovis/actions/workflows/publish.yaml/badge.svg?branch=main)](https://github.com/AM-Digital-Research-Environment/ontovis/actions/workflows/publish.yaml) ![PyPI - Version](https://img.shields.io/pypi/v/ontovis) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ontovis)

Visualize and analyze the pathbuilder of a WissKI-system.

A more detailed [rationale](#rationale) is available at the end of this document.

## Install

Get it from PyPI:

``` console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install ontovis
```

### From source

Or clone from source; note that these instructions recommend and assume [uv](https://docs.astral.sh/uv) over pip:

``` console
$ git clone https://github.com/AM-Digital-Research-Environment/ontovis
$ cd ontovis
$ uv sync
$ uv run ontovis
```

### From source, with Docker

Or, if you don't want to mess with dependencies, run it from docker:

``` console
$ git clone https://github.com/AM-Digital-Research-Environment/ontovis
$ cd ontovis
$ docker build -f docker/Dockerfile-3.11 -t "ontovis:3.11" .
$ docker run ontovis:3.11 render <URL>
```

Please note that output redirection with `docker run` isn't working yet.
You'll have to store the output produced by the above command to a file, then mount that into the container in order for `ontovis stats` to be able to pick it up.

## Requirements

* a WissKI pathbuilder definition, in XML; can be created via the "backup pathbuilder"-feature

### Optional

* [graphviz](https://graphviz.org/), for rendering the representation to an image.
    If you don't want to install graphviz, [there's a graphical editor](https://magjac.com/graphviz-visual-editor/) that you can paste the output into.

## Usage

**Also see [COMMANDS](./COMMANDS.md) for the complete documentation.**

### Quickstart

To produce a graph-specification in DOT-format:

``` console
$ ontovis render https://example.com/pathbuilder.xml
// lengthy output follows
```

If you have graphviz installed on your machine, pipe the output to the `dot` command and into an image file:

``` console
$ ontovis render https://example.com/pathbuilder.xml | dot -Tpng > pathbuilder.png
// now view pathbuilder.png in your preferred image viewer
```

You can also redirect the output to a file, or to the clipboard so that you can paste it into [an online editor](https://magjac.com/graphviz-visual-editor/):

``` console
// redirect to file
$ ontovis render https://example.com/pathbuilder.xml > pathbuilder.dot
// redirect to system clipboard (UNIX only, probably)
$ ontovis render https://example.com/pathbuilder.xml | xclip -selection c
```

### Walk-through

You will typically start off with a pathbuilder definition in XML.
This may exist on your local drive, or as a remote resource somewhere on your WissKI instance; we'll assume a remote resource here.

Starting off, you can use one of the builtin templates to render this pathbuilder to a graph in graphviz' DOT language.
By default, this will render a network of classes, without field and group hierarchy.
`ontovis` ships with three builtin templates, and you can also author your own; see [Templates](#templates) below for more info.

``` console
$ ontovis render https://example.com/pathbuilder.xml
digraph G {
    concentrate=true;
    graph [fontname = "Courier"];
    node [fontname = "Courier"];
    edge [fontname = "Courier"];
    node [style=filled,color=pink];
    fontsize=20;

    bgcolor=transparent;

    # group: g_somethting
    "Class A" -> "Relation X" -> "Class B";
    ...
```

`ontovis` uses graphviz' DOT-format to create a representation of the network.
As illustrated in the [Quickstart](#quickstart)-section, you can pipe the output to the `dot`-command if you have it installed, or simply copy it to an online editor that renders networks on the fly.

#### Templates

The templates provided by `ontovis` are:

* `no_groups` (default): render only the ontology-classes and omit grouping into fields and path-groups.
* `no_fields`: group the ontology classes into path-groups, omit fields.
* `full`: group classes into fields, and fields into path-groups. Warning: the resulting representation can become very dense.

You can select a template with the `--template`-option:

``` console
$ ontovis render https://example.com/pathbuilder.xml \
    --template no_fields
```

The builtin templates operate on different hierarchical representations.
A pathbuilder will typically contain groups of fields mapped out via concepts and relations of the employed ontology; additionally, groups may contain subgroups.
The default template `no_groups` will disregard any grouping hierarchy, and simply render all concepts and relations that appear in the pathbuilder, and how they are connected.

`no_fields` applies one level of grouping: it creates a sub-graph for each group defined in the pathbuilder, placing the concepts appearing in that group within.

`full` renders the full hierarchy of groups, subgroups, and fields; this representation can quickly get large and unwieldy.
However, it is valuable to see what fields are mapped out, and how the concepts interrelate.

While these builtin templates should provide a decent starting point, you can pass a custom template as well, using the `--custom-template` option.
This allows you to render any representation of the parse tree:

``` console
$ ontovis render https://example.com/pathbuilder.xml \
    --template-custom ./my-template.html.jinja2
```

This doesn't even have to be a graphviz-specification, so you could render to HTML, LaTeX, plain text or any other format you can think of.
The only requirement is that you author the template in [jinja2](https://jinja.palletsprojects.com/en/stable/templates/).

To help you in authoring such templates, you can dump the parse tree `ontovis` uses internally with the `--raw` option:

``` console
$ ontovis render https://example.com/pathbuilder.xml \
    --raw
```

### Network Metrics

`ontovis` can produce a network analytical overview of key metrics, such as number of edges, number of nodes, degree centrality, and others.
You can pass a file containing a graph-specification (in DOT format) to the `ontovis stats` sub-command, or you can simply pipe the output of `ontovis render` into it:

``` console
// read local file
$ ontovis stats ./graph.dot
// pipe output of render in; be sure to pass the dash "-" to indicate it should read from stdin
$ ontovis render https://example.com/pathbuilder.xml | ontovis stats -
```

The analysis is powered by [NetworkX](https://networkx.org/) under the hood and could be extended with other metrics provided by that library.

## Rationale

The pathbuilder is a core component of any WissKI system.
It relates the metadata of the items to concepts and relations in a top-level ontology.

Over time, a WissKI can grow in complexity, with further groups, subgroups, and fields being added to the pathbuilder, mapping out complex paths in the ontology.
While this increase in complexity is (probably) desired, it can become harder to understand how the top-level ontology is being used: what concepts and relations are mapped, what custom concepts were introduced, and how do they all interrelate?

It is often easier to understand these dynamics through the visual system, rather than the tabular view within the pathbuilder interface itself.
To aid in this understanding, `ontovis` can render a pathbuilder XML-dump to DOT-syntax, an easy-to-grasp, yet powerful representation of complex networks.
This DOT-representation can then be rendered by graphviz, which is often superior in terms of layouting than the drawing capabilities of common network-analysis libraries.

Furthermore, the pathbuilder essentially describes an ontology-graph of concepts and relations, and therefore lends itself to network analysis.
The `ontovis stats` command takes as input a graph in DOT-syntax, and computes a set of key network metrics that can aid in answering questions such as,

* what are the most used concepts and relations?
* what are the "central" concepts and relations?

In summary, `ontovis` is intended as a tool to help you understand your data model, and potentially refine and extend it.

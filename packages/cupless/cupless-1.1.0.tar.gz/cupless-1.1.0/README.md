# cupless
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/) - [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined
)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

Printing on Linux without CUPS.

[This is a first-cut - but I'm throwing it live because... I'm done with printers for today]. I might add more features when i need to rpint more stuff.

## Motivation
I don't like [CUPS](https://openprinting.github.io/cups/). It's this hidden daemon that hides in the background and gets in the way of printing can go wrong and is then difficult to debug. We live in the future with standard file formats (`.pwg`) and standardized printer protocols (ipp) - we should be able to print directly on the command-line immediately and just see the errors right there, rather than debugging through a layer of queues with errors and obscure commands.

## Installation
This tool depends on [mutool](https://www.mankier.com/1/mutool), [ipptool](https://www.cups.org/doc/man-ipptool.html), and [pdfjam](https://github.com/pdfjam/pdfjam). Importantly, all of these can be installed with apt on ubuntu with `sudo apt install mupdf-tools texlive cups-ipp-utils` (texlive supplies `pdfjam`)

Once you have installed these you can install this with  [pipx](https://github.com/pypa/pipx).

```
pipx install cupless
```

## Usage
`cupless file` will print a file with ipptools. Images will be scaled to fit a page.
At the moment only single page files are supported - I image i will fix this as soon as I have to print something with multiple pages.

## Some technical details
`ipp` is an HTTP-based standard that most printers support that allows files to be sent to the printer and printed. Unfortunately, likely to make printers simpler, standard formats such as PDF or PNG are not supported - rather than either niche (PWF, URF) or proprietary or lossy (JPEG) formats.

This tool is a wrapper around `mutool` and `ipp` which takes a PDF converts it into a niche format and sends it to a printe.

## Alternatives and prior work
Obviously there has been a bunch of work on standardizing printers. This tool makes use of [mutool](https://www.mankier.com/1/mutool) for converting PDF. Attah wrote a tool called [ippclient](https://github.com/attah/ppm2pwg) (and an alternative to mutool) which I think performs a similar role to this tool - but there is no automatic installation process for this tool.

## Caveats
I didn't want to depend upon `ipptools` as this is maintained by cups (though it is a separate package). However, I had difficulty getting the print command to work so gave up and used iptools. If I feel inspired (of if you do and feel like submitting patches) I might remove this. `pdfjam` depends on latex and texlive - which is quite big - however it is quite good at resizing images.

This only works with printers that have a default resolution of 300dpi.

## About me
I am **@readwithai**. I create tools for reading, research and agency sometimes using the markdown editor [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

I also create a [stream of tools](https://readwithai.substack.com/p/my-productivity-tools) that are related to carrying out my work.

I write about lots of things - including tools like this - on [X](https://x.com/readwithai).
My [blog](https://readwithai.substack.com/) is more about reading and research and agency.

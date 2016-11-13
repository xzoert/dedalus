Dedalus
=======

## Overview
Dedalus aims to be a system that helps you in organizing resources by tags.
Resources can be documents on your hard disk, web resources, emails, personal contact etc.

Dedalus has three components: 

- [dedalus-server](#dedalus-server)
- [dedalus-tagger](#dedalus-tagger)
- [dedalus-browser](#dedalus-browser)

### <a name="dedalus-server"></a>dedalus-server
This is the dedalus backend on top of which the 
GUIs operate. It is written in nodejs, and largely based on a library called 
[tagman](https://github.com/xzoert/tagman), which does most of the job. 

### <a name="dedalus-tagger"></a>dedalus-tagger
This is the GUI for tagging resources, with tag autocompletion, 
multiple resources editing, and whose aim is to be as easy and handy to use as it can be. 
The tagger can be invoked, for example, by a nautilus action allowing you to right-click
on any file or directory and tagging it. 
Also there is a nice [extension for Firefox](https://addons.mozilla.org/en-US/firefox/addon/open-with/) 
that allows you easily to open the dedalus-tagger for tagging the current web page.

### <a name="dedalus-browser"></a>dedalus-browser

### State of the project
Dedalus is at its very early stage of development. Anyone interested to contribute 
is very welcome. 

## Installation

The installation process is at its very first stages of development. It is currently tested
on ubuntu 15.10 and 16.04, but is likely to work on 16.10 as well. You might want to 
edit manually the Makefile in order to meet your system. If you do so successfully,
please let me know! 

The first step is to clone the dedalus repository somewhere.

```
	git clone https://github.com/xzoert/dedalus.git
```

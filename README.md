# ![dedalus](dedalus.png) Dedalus

## Overview

I always wanted to have all my resources (dcuments, pictures, emails, personal 
contacts, bookmarks, etc. etc.) accessible through 
a unified interface, where they are classified in a meaningful way, linked to each 
other with relevant associations, allowing me to browse them semantically and find 
what I'm looking for in a couple of clicks without having to remember anything 
(no URLs, no directory paths, no email account and approximate date and so forth). 

And of course, I don't want to spend my whole day in classifying manually all my stuff
in order to get such a result.

I think that *tags* have proven to be a very effective mean of classification, even
for very large collections of very heterogeneous items.

Tags have several interesting characteristics:

- they do not require any pre-ordered conceptual scheme and anyone can invent his 
own step by step, reflecting the way he/she thinks and looks at the world
- they build up silently semantic links between items having (or NOT having)
some tags in common
- they build up silently a semantic network across the tags themselves, by being
used in similar contexts (that is, by items having or NOT having some tags in common)
- they are very easy and intuitive to use for everybody, being just *words*. 

With Dedalus I'm trying to provide a way to easily tag resources and browse 
them afterwards exploiting those tags and their underlying semantic structures.








Dedalus aims to be a system that allows you to organize resources by tags. 
Resources can be documents on your hard disk, web resources, emails, personal contacts etc.

The purpose is to overcome the inherent limitations of simple structures like 
lists or trees you have on your file system, browser bookmarks and so forth. 
By using tags you can access the same resource through different paths, create thematic
sub-collections of heterogeneous resources based on having (or *not* having) a set of tags, 
browse the semantic network across tags that builds up silenty while you fill in the database.

I'm writing this trying to solve the problem of a friend of mine who is doing a Phd
in antropology. She has lots of documents, interviews, pictures, web resoures and so 
forth, and desperately needs something to give a (non trivial) order to that chaos. 

Dedalus has three components: 

- [dedalus-server](#dedalus-server): in *nodejs* + *sqlite3*
- [dedalus-tagger](#dedalus-tagger): in *python3* + *qt4*
- [dedalus-browser](#dedalus-browser): in *python3* + *qt4*

### <a name="dedalus-server"></a>dedalus-server

This is the dedalus backend on top of which the 
GUIs operate. It is written in nodejs, and largely based on a library called 
[tagman](https://github.com/xzoert/tagman), which does most of the job. 
Data are saved on an sqlite3 database, located at *~/.tagman/default.sql*.

### <a name="dedalus-tagger"></a>dedalus-tagger

This is the GUI for tagging resources, with tag autocompletion, 
multiple resource editing, and whose aim is to be as easy and handy to use as it can be. 

![dedalus-tagger](tagger-screenshot.png)

The tagger can be invoked by right clicking on a file or directory 
in your file manager (using [nautilus-actions](http://www.nautilus-actions.org/) for nautilus,
configuring a *custom action* in thunar etc.).
Also there is a nice [extension for Firefox](https://addons.mozilla.org/en-US/firefox/addon/open-with/) 
that can easily be configured to open the dedalus-tagger for tagging the current web page.
It is pretty easy as well to create an open/libre-office macro which opens the dedalus-tagger
on the currently edited document.

### <a name="dedalus-browser"></a>dedalus-browser

The browser lets you navigate through the tagged resources. It creates a tag cloud
contextual to the current search criteria.

![dedalus-browser](browser-screenshot1.png)
![dedalus-browser](browser-screenshot2.png)



### State of the project
The current version of Dedalus is a kind of *proof of concept*. It works pretty well
and there are no bugs known to me at the moment, but I've written the code with the only 
purpose in mind to have something working as quickly as possible. 
The most stable part is the database, which will probably not change too much in
the future. The remaining has to be rewritten in a much cleaner way, and also i'd like to use Qt5
instead of Qt4.
Anyone who wants to try it out is very welcome, and I promise that I'll do my best to 
migrate any data generated with this version of Dedalus towards any newer version if 
it happens to become incompatible. 


## Installation

The current Makefile has been tested on ubuntu 15.10 and 16.04, but is likely to work 
on 16.10 as well. 

You might want to edit manually the Makefile in order to meet your system. If you do so successfully,
please let me know! 

The first step is to clone the dedalus repository somewhere.

```
git clone https://github.com/xzoert/dedalus.git
```

Then enter the dedalus directory, make and install:

```
cd dedalus
make
make install
```

The `make` command does the following:

- install (using apt-get) any required package if not present 
(a recent version of nodejs, nautilus-actions, pyside and qt4). For this reason 
you might be requested for your password.

- checkout from git the three dedalus components (tagger, browser and server)

- launch `npm install` in the server in order to install the required nodejs
packages


While `make install` will:

- copy the code into /usr/share/dedalus

- create the entries *dedalus-browser*, *dedalus-tagger* and *dedalus-server* in */usr/bin*

- add the dedalus server to the startup applications for the current user

- install the dedalus action for nautilus for the current user

If you want to undo what `make install` has done, type:

```
make remove
```

## Usage

After installation, you'll better logout and login again (or restart the computer). 
This is the easiest way to start the dedalus server automatically and to retsart
Nautilus in order to refresh its custom actions.

But if you want to do this all manually, you can open a termina and type:

```
nautils -q
dedalus-server
```
Don't close the terminal (the dedalus server is running in there), and re-open Nautilus.

Now you should have in Nautilus a new entry in the context menu, called "Dedalus".

You can select one or more files and/or directories and open the dedalus tagger by 
right-clicking and choosing this *Dedalus* entry in the context menu.

This will allow you to tag those resources. 







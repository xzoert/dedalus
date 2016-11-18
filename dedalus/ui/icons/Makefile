ICONS		=	assigned.svg  \
				dedalus.svg  \
				delete.svg  \
				directory.svg  \
				inherited.svg  \
				not-assigned.svg  \
				refresh.svg  \
				tagger.svg  \
				typedir.svg  \
				typefile.svg  \
				typeweb.svg

RCC			=	pyside-rcc -py3 

all: icons_rc.py

icons_rc.py: $(ICONS) icons.qrc
	$(RCC) -o icons_rc.py icons.qrc
	
	
install: all
	cp dedalus.svg /usr/share/icons

remove:
	-rm /usr/share/icons/dedalus.svg

clean:
	-rm icons_rc.py


UIS  		= taggerUi.py
UIC   		= pyside-uic --from-imports 


.PHONY: all
all: $(UIS)

taggerUi.py: taggerUi.ui
	$(UIC) taggerUi.ui -o $@



install: all
	cp dedalus-tagger /usr/bin
	chmod a+x /usr/bin/dedalus-tagger

remove:
	-rm /usr/bin/dedalus-tagger

clean:
	-rm taggerUi.py



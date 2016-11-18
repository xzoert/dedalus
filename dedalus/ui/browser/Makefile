UIS  		= browserUi.py
UIC   		= pyside-uic --from-imports 


.PHONY: all
all: $(UIS)

browserUi.py: browserUi.ui
	$(UIC) browserUi.ui -o $@



install: all
	cp dedalus-browser /usr/bin
	chmod a+x /usr/bin/dedalus-browser

remove:
	-rm /usr/bin/dedalus-browser

clean:
	-rm taggerUi.py



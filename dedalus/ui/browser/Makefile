UIS  		= browserUi.py
UIC   		= pyside-uic --from-imports 


.PHONY: all
all: $(UIS)

browserUi.py: browserUi.ui
	$(UIC) browserUi.ui -o $@



install: all
	cp dedalus-browser /usr/bin
	chmod a+x /usr/bin/dedalus-browser
	cp dedalus-browser.desktop /usr/share/applications/

remove:
	-rm /usr/bin/dedalus-browser
	-rm /usr/share/applications/dedalus-browser.desktop

clean:
	-rm taggerUi.py





setup:
	git clone https://github.com/xzoert/dedalus-tagger.git
	git clone https://github.com/xzoert/dedalus-browser.git
	git clone https://github.com/xzoert/dedalus-server.git
	cd dedalus-server
	npm install
	cd ..
	
	
install_browser:
	-mkdir /usr/share/dedalus
	-mkdir /usr/share/dedalus/dedalus-browser
	cp dedalus-browser/main.pyw /usr/share/dedalus/dedalus-browser/
	cp dedalus-browser/navigator_widget.py /usr/share/dedalus/dedalus-browser/
	cp dedalus-browser/resources_rc.py /usr/share/dedalus/dedalus-browser/
	cp dedalus-browser/dedalus-browser.desktop /usr/share/applications/
	cp dedalus-tagger/dedalus.svg /usr/share/icons/
	cp dedalus-browser/dedalus-browser /usr/bin/
	
install_tagger:
	-mkdir /usr/share/dedalus
	-mkdir /usr/share/dedalus/dedalus-tagger
	cp dedalus-tagger/main.pyw /usr/share/dedalus/dedalus-tagger/
	cp dedalus-tagger/model.py /usr/share/dedalus/dedalus-tagger/
	cp dedalus-tagger/tagger_rc.py /usr/share/dedalus/dedalus-tagger/
	cp dedalus-tagger/tagger_widget.py /usr/share/dedalus/dedalus-tagger/
	cp dedalus-tagger/dedalus-tagger /usr/bin/
	cp dedalus-tagger/dedalus-action.desktop ~/.local/share/file-manager/actions/

install_server:
	-mkdir /usr/share/dedalus
	-mkdir /usr/share/dedalus/dedalus-server
	cp dedalus-server/server.js /usr/share/dedalus/dedalus-server/
	cp -r dedalus-server/node_modules usr/share/dedalus/dedalus-server/
	cp dedalus-server/dedalus-server.desktop ~/.conf/autostart/
	
remove:
	rm -r /usr/share/dedalus
	rm /usr/share/applications/dedalus-browser.desktop
	rm /usr/share/icons/dedalus.svg
	rm /usr/bin/dedalus-tagger
	rm /usr/bin/dedalus-browser
	rm /usr/bin/dedalus-server
	rm ~/.conf/autostart/dedalus-server.desktop
	rm ~/.local/share/file-manager/actions/dedalus-action.desktop
	


packages:
	sudo apt-get install -y python3-pyside
	curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
	sudo apt-get install -y nodejs	

setup:
	-git clone https://github.com/xzoert/dedalus-tagger.git
	-git clone https://github.com/xzoert/dedalus-browser.git
	-git clone https://github.com/xzoert/dedalus-server.git
	cd dedalus-server; npm install
	
	
install_browser:
	-sudo mkdir /usr/share/dedalus
	-sudo mkdir /usr/share/dedalus/dedalus-browser
	sudo cp dedalus-browser/main.pyw /usr/share/dedalus/dedalus-browser/
	sudo cp dedalus-browser/navigator_widget.py /usr/share/dedalus/dedalus-browser/
	sudo cp dedalus-browser/resources_rc.py /usr/share/dedalus/dedalus-browser/
	sudo cp dedalus-browser/dedalus-browser.desktop /usr/share/applications/
	sudo cp dedalus-tagger/dedalus.svg /usr/share/icons/
	sudo cp dedalus-browser/dedalus-browser /usr/bin/
	sudo chmod a+x /usr/bin/dedalus-browser
	
	
install_tagger:
	-sudo mkdir /usr/share/dedalus
	-sudo mkdir /usr/share/dedalus/dedalus-tagger
	sudo cp dedalus-tagger/main.pyw /usr/share/dedalus/dedalus-tagger/
	sudo cp dedalus-tagger/model.py /usr/share/dedalus/dedalus-tagger/
	sudo cp dedalus-tagger/tagger_rc.py /usr/share/dedalus/dedalus-tagger/
	sudo cp dedalus-tagger/tagger_widget.py /usr/share/dedalus/dedalus-tagger/
	sudo cp dedalus-tagger/dedalus-tagger /usr/bin/
	sudo chmod a+x /usr/bin/dedalus-tagger
	cp dedalus-tagger/dedalus-action.desktop ~/.local/share/file-manager/actions/

install_server:
	-sudo mkdir /usr/share/dedalus
	-sudo mkdir /usr/share/dedalus/dedalus-server
	sudo cp dedalus-server/server.js /usr/share/dedalus/dedalus-server/
	sudo cp -r dedalus-server/node_modules usr/share/dedalus/dedalus-server/
	sudo cp dedalus-server/dedalus-server /usr/bin/
	sudo chmod a+x /usr/bin/dedalus-tagger
	cp dedalus-server/dedalus-server.desktop ~/.conf/autostart/
	
install: install_browser install_server install_tagger
	
all: packages setup install


remove:
	rm -r /usr/share/dedalus
	rm /usr/share/applications/dedalus-browser.desktop
	rm /usr/share/icons/dedalus.svg
	rm /usr/bin/dedalus-tagger
	rm /usr/bin/dedalus-browser
	rm /usr/bin/dedalus-server
	rm ~/.conf/autostart/dedalus-server.desktop
	rm ~/.local/share/file-manager/actions/dedalus-action.desktop
	


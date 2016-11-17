UI_SRC = qt-designer/tagCloudTestWindow.ui  qt-designer/tagger.ui
ICON_SRC = `ls icons/*.svg`


build_ui: $(UI_SRC)

build_icons: $(ICON_SRC)
	cd qt-designer; ./make.sh
	cd icons; ./make.sh

.PHONY : build
build: build_ui build_icons
	
install: build
	@sudo python3 setup.py install --record installed_files.txt

remove:
	@cat installed_files.txt | sudo xargs rm -rf



helpold:
	@echo ""
	@echo "Usage: make [COMMAND]"
	@echo ""
	@echo "Where [COMMAND] can be one of the following: "
	@echo ""
	@echo "help                    Displays this help text"
	@echo "dependencies            Installes needed packages, if not already installed."
	@echo "setup                   Downloads and configures the sub-projects from git."
	@echo "install                 Installs dedalus."
	@echo "remove                  Removes a previous installation."
	@echo "clean                   Removes the sub-projects (undoes 'setup')"
	@echo ""
	@echo "Giving no [COMMAND] is equivalent of doing 'make dependencies' followed by 'make setup'."
	@echo ""



dependencies:
	@printf "\n*** Checking dependencies.\n"
	@if [ ! "`dpkg -l python3-pyside`" ]; then sudo apt-get install -y python3-pyside; fi
	@if [ ! `command -v nodejs` ]; then \
		echo 'Installing nodejs...'; \
		@curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -; \
		@sudo apt-get install -y nodejs; \
		echo 'Installing nodejs done.'; \
	fi
	@if [ ! "`dpkg -l nautilus-actions`" ]; then sudo apt-get install -y nautilus-actions; fi
	@printf "*** Dependencies ok.\n\n"

setup:
	@printf "\n*** Setting up sub-repositories.\n"
	@if [ ! -d "dedalus-tagger" ]; then git clone https://github.com/xzoert/dedalus-tagger.git; fi
	@if [ ! -d "dedalus-browser" ]; then git clone https://github.com/xzoert/dedalus-browser.git; fi
	@if [ ! -d "dedalus-server" ]; then \
		git clone https://github.com/xzoert/dedalus-server.git; \
		cd dedalus-server; npm install; \
	fi
	@printf "*** Sub-repositories ok.\n\n"

	


install_old: 
	@printf "\n*** Installing dedalus...\n"
	
	@# dedalus dirs
	@if [ -d "/usr/share/dedalus" ]; then sudo rm -rf /usr/share/dedalus; fi
	@sudo mkdir /usr/share/dedalus
	
	
	@# browser
	@sudo mkdir /usr/share/dedalus/dedalus-browser
	@sudo cp dedalus-browser/main.pyw /usr/share/dedalus/dedalus-browser/
	@sudo cp dedalus-browser/navigator_widget.py /usr/share/dedalus/dedalus-browser/
	@sudo cp dedalus-browser/resources_rc.py /usr/share/dedalus/dedalus-browser/
	@sudo cp dedalus-browser/dedalus-browser.desktop /usr/share/applications/
	@sudo cp dedalus-tagger/dedalus.svg /usr/share/icons/
	@sudo cp dedalus-browser/dedalus-browser /usr/bin/
	@sudo chmod a+x /usr/bin/dedalus-browser
	
	@# tagger
	@sudo mkdir /usr/share/dedalus/dedalus-tagger
	@sudo cp dedalus-tagger/main.pyw /usr/share/dedalus/dedalus-tagger/
	@sudo cp dedalus-tagger/model.py /usr/share/dedalus/dedalus-tagger/
	@sudo cp dedalus-tagger/tagger_rc.py /usr/share/dedalus/dedalus-tagger/
	@sudo cp dedalus-tagger/tagger_widget.py /usr/share/dedalus/dedalus-tagger/
	@sudo cp dedalus-tagger/dedalus-tagger /usr/bin/
	@sudo chmod a+x /usr/bin/dedalus-tagger
	@mkdir -p ~/.local/share/file-manager/actions
	@cp dedalus-tagger/dedalus-action.desktop ~/.local/share/file-manager/actions/
	
	@# server
	@sudo mkdir /usr/share/dedalus/dedalus-server
	@sudo cp dedalus-server/server.js /usr/share/dedalus/dedalus-server/
	@sudo cp -r dedalus-server/node_modules /usr/share/dedalus/dedalus-server/
	@sudo cp dedalus-server/dedalus-server /usr/bin/
	@sudo chmod a+x /usr/bin/dedalus-server
	@mkdir -p ~/.config/autostart
	@cp dedalus-server/dedalus-server.desktop ~/.config/autostart/

	
	@printf "*** Dedalus has been successfully installed.\n\n"
	
clean_old:
	@printf "\n*** Cleaning up sub-repositories.\n"
	@-rm -rf dedalus-server
	@-rm -rf dedalus-browser
	@-rm -rf dedalus-tagger
	@printf "*** Sub-directories cleaned up. You will have to run \"make setup\" for a fresh restore\n\n"

remove_old:
	@printf "\n*** Removing dedalus\n"
	@-sudo rm -rf /usr/share/dedalus
	@-sudo rm /usr/share/applications/dedalus-browser.desktop
	@-sudo rm /usr/share/icons/dedalus.svg
	@-sudo rm /usr/bin/dedalus-tagger
	@-sudo rm /usr/bin/dedalus-browser
	@-sudo rm /usr/bin/dedalus-server
	@-rm ~/.config/autostart/dedalus-server.desktop
	@-rm ~/.local/share/file-manager/actions/dedalus-action.desktop
	@printf "*** Dedalus successfully removed.\n\n"



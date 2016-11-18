
all:
	if [ ! -d "node_modules/tagman/.git" ]; then \
		npm install; \
	fi

install:
	mkdir /usr/share/dedalus-server
	cp server.js /usr/share/dedalus-server/
	cp -r node_modules /usr/share/dedalus-server/
	cp dedalus-server /usr/bin/
	chmod a+x /usr/bin/dedalus-server
	cp dedalus-server.desktop /etc/xdg/autostart/

clean:

remove:
	-rm /usr/bin/dedalus-server
	-rm /etc/xdg/dedalus-server.desktop
	-rm -rf /usr/share/dedalus-server





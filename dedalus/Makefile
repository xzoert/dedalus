SUBDIRS 	= ui

.PHONY: all $(SUBDIRS)
all: $(SUBDIRS)


$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)
	
	
install: all $(SUBDIRS)

remove: $(SUBDIRS)

clean: $(SUBDIRS)





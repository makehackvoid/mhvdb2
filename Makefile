help:
	@echo "build - Build container"
	@echo "run - Run container"
        
build:
	docker build -t="makehackvoid/mhvdb2" .
        
run:	build
	docker run -p 8081:80 -t -i -d -v $(CURDIR):/opt/mhvdb2 makehackvoid/mhvdb2
	
stop:	
	docker ps | grep mhvdb2 | awk '{ print $1 }' | xargs docker stop

REPO=harbor.kongkongss.com
ORG=zhongkui
NAME=file
CATEGORY=core
VERSION?=$(shell cat VERSION)
MALWARE=test/malware
NOT_MALWARE=test/not.malware


all: build

.PHONY: build
build:
	docker build -t $(REPO)/$(ORG)/$(NAME):$(VERSION) .

# .PHONY: test
# test:
# 	echo "===> Run zk-file"
# 	docker run --name $(NAME) -it -v ${PWD}/tests/malware:/malware $(REPO)/$(ORG)/$(NAME):$(VERSION) /bin/bash
# 	docker attach file

.PHONY: stop
stop: ## Kill running docker containers
	@docker rm -f zk-daemon || true
	@docker rm -f zk-api || true

clean:
	# docker rm -f $(NAME) || true
	# docker image rm $(REPO)/$(ORG)/$(NAME):$(VERSION)
	docker volumes prune

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


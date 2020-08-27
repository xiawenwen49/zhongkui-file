ORG=zhongkuiai
NAME=zhongkui-file
#NAME=zhongkui-builder
VERSION=1.0.8


all: build

.PHONY: build
build:
	docker build -t $(ORG)/$(NAME):$(VERSION) .

.PHONY: dev
dev:
	echo "===> Run $(NAME)"
	docker run --name $(NAME) -itd -v ${PWD}:/zhongkui/file $(ORG)/$(NAME):$(VERSION) /bin/bash
	docker exec -it $(NAME) /bin/bash

.PHONY: attach
attach:
	docker exec -it $(NAME) /bin/bash

.PHONY: stop
stop: ## Kill running docker containers
	@docker rm -f $(NAME) || true

clean:
	# docker rm -f $(NAME) || true
	# docker image rm $(ORG)/$(NAME):$(VERSION)
	docker volumes prune

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


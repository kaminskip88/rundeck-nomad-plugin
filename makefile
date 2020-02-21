build: clean
	@mkdir -p ./build/rundeck-nomad-plugin
	@cp -r ./contents ./build/rundeck-nomad-plugin
	@cp -r ./resources ./build/rundeck-nomad-plugin
	@cp ./plugin.yaml ./build/rundeck-nomad-plugin
	@cd ./build && zip -r rundeck-nomad-plugin.zip rundeck-nomad-plugin
clean: down
	@rm -rf ./build

up: build
	@docker-compose up -d

down:
	@docker-compose down

sh:
	@docker-compose exec rundeck /bin/bash

logs:
	@docker-compose logs rundeck

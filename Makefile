go:
	docker compose up -d --build
logs:
	docker logs new-project-mailbot -f
kill:
	docker kill new-project-mailbot
	docker image rm new-project-mailbot --force

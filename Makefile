# Variables
COMPOSE_DEV=docker compose -f docker-compose.dev.yml
COMPOSE_PROD=docker compose -f docker-compose.prod.yml

# Development commands
dev-up:
	$(COMPOSE_DEV) up --build -d

dev-down:
	$(COMPOSE_DEV) down

dev-logs:
	$(COMPOSE_DEV) logs -f

dev-restart:
	$(COMPOSE_DEV) restart

dev-shell:
	$(COMPOSE_DEV) exec backend bash

# Production commands
prod-up:
	$(COMPOSE_PROD) up --build -d

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f

# Database commands
db-shell:
	$(COMPOSE_DEV) exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_NAME)

# Migration commands
migration-create:
	$(COMPOSE_DEV) exec backend alembic revision --autogenerate -m "$(name)"

migration-apply:
	$(COMPOSE_DEV) exec backend alembic upgrade head

migration-rollback:
	$(COMPOSE_DEV) exec backend alembic downgrade -1

migration-history:
	$(COMPOSE_DEV) exec backend alembic history --verbose

migration-current:
	$(COMPOSE_DEV) exec backend alembic current

# Quick migration (create and apply)
migration:
	$(COMPOSE_DEV) exec backend alembic revision --autogenerate -m "$(name)"
	$(COMPOSE_DEV) exec backend alembic upgrade head

# Utility commands
clean:
	docker system prune -f

status:
	$(COMPOSE_DEV) ps

# Help command
help:
	@echo "Available commands:"
	@echo "  dev-up      - Start development environment"
	@echo "  dev-down    - Stop development environment"
	@echo "  dev-logs    - Show development logs"
	@echo "  dev-restart - Restart development services"
	@echo "  dev-shell   - Access backend container shell"
	@echo "  prod-up     - Start production environment"
	@echo "  prod-down   - Stop production environment"
	@echo "  db-shell    - Access database shell"
	@echo ""
	@echo "Migration commands:"
	@echo "  migration-create name='migration_name' - Create new migration"
	@echo "  migration-apply         - Apply all pending migrations"
	@echo "  migration-rollback      - Rollback last migration"
	@echo "  migration-history       - Show migration history"
	@echo "  migration-current       - Show current migration"
	@echo "  migration name='name'   - Create and apply migration"
	@echo ""
	@echo "Utility commands:"
	@echo "  clean       - Clean docker system"
	@echo "  status      - Show service status"
	@echo "  help        - Show this help"

.PHONY: dev-up dev-down dev-logs dev-restart dev-shell prod-up prod-down db-shell clean status help
.PHONY: migration-create migration-apply migration-rollback migration-history migration-current migration
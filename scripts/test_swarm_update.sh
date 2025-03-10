#!/bin/bash
set -e

# Colors for pretty output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Initializing Docker Swarm...${NC}"
docker swarm init --advertise-addr 127.0.0.1 || echo "Swarm already initialized"

echo -e "${YELLOW}Creating test service...${NC}"
docker service create --name test-web nginx:1.19
echo "Waiting for service to start..."
sleep 5

echo -e "${YELLOW}Testing image update...${NC}"
sugar swarm update --services test-web --image nginx:1.21
echo "Verifying image..."
docker service inspect test-web --format "{{.Spec.TaskTemplate.ContainerSpec.Image}}" | grep "nginx:1.21" && echo -e "${GREEN}✓ Image update successful${NC}" || echo -e "${RED}✗ Image update failed${NC}"

echo -e "${YELLOW}Testing replicas update...${NC}"
sugar swarm update --services test-web --replicas 2
echo "Waiting for replicas to scale..."
sleep 3
docker service ls | grep "test-web" | grep "2/2" && echo -e "${GREEN}✓ Replicas update successful${NC}" || echo -e "${RED}✗ Replicas update failed${NC}"

echo -e "${YELLOW}Testing env var update...${NC}"
sugar swarm update --services test-web --env_add "DEBUG=1,LOG_LEVEL=info"
docker service inspect test-web --format "{{.Spec.TaskTemplate.ContainerSpec.Env}}" | grep "DEBUG=1" && echo -e "${GREEN}✓ Env vars update successful${NC}" || echo -e "${RED}✗ Env vars update failed${NC}"

echo -e "${YELLOW}Testing label update...${NC}"
sugar swarm update --services test-web --label_add "environment=testing,tier=frontend"
docker service inspect test-web --format "{{json .Spec.Labels}}" | grep "environment" && echo -e "${GREEN}✓ Label update successful${NC}" || echo -e "${RED}✗ Label update failed${NC}"

echo -e "${YELLOW}Testing combined options...${NC}"
sugar swarm update --services test-web --image nginx:1.22 --force --detach --env_add "NEW_VAR=test"
echo -e "${GREEN}✓ Combined update executed${NC}"

echo -e "${YELLOW}Cleaning up...${NC}"
docker service rm test-web
docker swarm leave --force
echo -e "${GREEN}Done!${NC}"

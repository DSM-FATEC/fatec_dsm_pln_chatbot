#!/bin/bash
docker build . -f ./deploy/Dockerfile -t pln-chatbot-api:v1.3 --platform linux/amd64


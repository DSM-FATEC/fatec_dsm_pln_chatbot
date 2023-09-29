#!/bin/bash
docker build . -f ./deploy/Dockerfile -t pln-chatbot-api:v1.4 --platform linux/amd64


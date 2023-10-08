#!/bin/bash
docker build . -f ./deploy/Dockerfile -t pln-chatbot-front:v1.1 --platform linux/amd64


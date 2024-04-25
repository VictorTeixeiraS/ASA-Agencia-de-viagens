#!/bin/bash

# Define the image and service names - monday
image_name="docker-ufu-asa-image"
service_name="ufu-asa-proj"

# Start Minikube
minikube start

# Ensure kubectl uses the correct context
kubectl config use-context minikube

# Set Docker environment
eval "$(minikube docker-env)"  # Ensure the correct environment

# Enabling Metrics Server
minikube addons disable heapster
minikube addons enable metrics-server

# Installing Metric Server
#kubectl apply -f metrics/custom-metrics-server.yaml
#kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Build the Docker image
docker build -t "$image_name" .  # Builds the image from the Dockerfile in the current directory

# Applying roles for the metrics server
#kubectl apply -f metrics-server-clusterrole.yaml
#kubectl apply -f metrics-server-clusterrolebinding.yaml
#kubectl rollout restart deployment/metrics-server -n kube-system

# Deploy using kubectl and a YAML configuration file
kubectl apply -f k8/deployment/deployment.yaml

# Waiting a bit for applying config
sleep 5

# Expose the deployment with LoadBalancer on the specified port
kubectl expose deployment "$service_name" --name="$service_name" --type=LoadBalancer --target-port=8000

# Check if the service exists and has endpoints
while true; do
  # Get the list of endpoints for the service
  endpoints=$(kubectl get endpoints "$service_name" -o=jsonpath='{.subsets[*].addresses[*].ip}')

  # If there are endpoints (i.e., not empty), the service is considered "on"
  if [[ -n "$endpoints" ]]; then
    echo "Service $service_name is active with endpoints: $endpoints."
    break
  else
    echo "Service $service_name is not active yet. Waiting..."
    sleep 5  # Adjust the sleep time as needed
  fi
done

# Get the service URL to access from the host machine
service_url=$(minikube service "$service_name" --url)

# Open the URL in the default browser
xdg-open "$service_url/docs" &

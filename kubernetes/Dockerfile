FROM postman/newman:alpine

# Copy your Postman collection into the Docker image
COPY postman_call/postman-test.json /etc/newman/

# Command to run the Postman tests
ENTRYPOINT ["newman", "run", "/etc/newman/postman-test.json"]

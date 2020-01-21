FROM python:2.7-slim-buster
#FROM python:2.7-buster

# Create a non-root user to run the application
RUN useradd --create-home appuser
# Change the working directory to the application user home directory
WORKDIR /home/appuser
# Change to the appuser context to run all further commands
USER appuser
# Copy files to image
COPY . /home/appuser

# Set the port number our app listens to and start the program
EXPOSE 5000
CMD ["python", "ecs-meta-search.py"]

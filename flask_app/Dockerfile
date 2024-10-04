FROM python:3.12.0

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY . ./ 

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the environment variable to enable Flask's development mode (auto-reload)
ENV FLASK_ENV=development
ENV FLASK_APP=main.py 
ENV FLASK_DEBUG=1

# Added this to print
ENV PYTHONUNBUFFERED=1
RUN echo "source activate my_env" > ~/.bashrc
ENV PATH /opt/conda/envs/my_env/bin:$PATH

# Define the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

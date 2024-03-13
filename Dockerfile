# FROM python:3.11-slim 

FROM python:3.11-slim-bullseye   

WORKDIR /app

# Install Streamlit and other dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt 

# Copy your application files
COPY . ./

# Expose the port used by Streamlit
EXPOSE 8501

# Command to start your app
CMD streamlit run main.py 
# Uses a stable, slim version of Debian (Bookworm) to keep the image size down 
FROM python:3.11-slim-bookworm

# Stops Python from creating extra 'cache' files and ensures logs show up immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Install System Dependencies
# Installs basic tools for the database (libpq), compiling code (gcc), and 
# ensuring the development environment runs smoothly (procps/git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    libpq-dev \
    gcc \
    git \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 2. Workspace setup
# Defines the folder where all our commands will run and where our code will live
WORKDIR /app

# 3. Setup 'vscode' user 
# Creates a standard user so we aren't running everything as 'root' (admin),
# which helps avoid file permission issues and improves security
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# 4. Install Python dependencies
# Copies just the requirements first so Docker can skip re-installing 
# everything if you only changed a line of code and not a package
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy code and fix ownership
# Copies the project into the image and makes sure the 'vscode' user 
# actually owns the files so they can edit them
COPY . /app/
RUN chown -R $USERNAME:$USER_GID /app

# Switches from the admin user to the 'vscode' user for the rest of the setup
USER $USERNAME

# 6. Keep container alive
# Tells the container to just stay open in the background so you can 
# connect to it and work on your code inside it
CMD sh -c "python -m streamlit run src/Visualization_App/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false" 

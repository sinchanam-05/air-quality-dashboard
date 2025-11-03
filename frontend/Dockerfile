FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package files and install dependencies (needed for a later successful build)
# Note: package.json must exist for a successful build, though we're using a placeholder command for now.
COPY package*.json ./
# We skip the heavy install command here because package.json is not yet created (Commit 010)
# RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Nuxt runs on
EXPOSE 3000

# Command to run Nuxt dev server (as specified in docker-compose.yml)
CMD ["npm", "run", "dev"]
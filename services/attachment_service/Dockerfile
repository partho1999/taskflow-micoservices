# Use official Node.js 20 LTS image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy source files
COPY . .

# Create uploads folder
RUN mkdir -p uploads

# Expose port (default 3000)
EXPOSE 3000

# Start the app
CMD ["node", "src/server.js"]
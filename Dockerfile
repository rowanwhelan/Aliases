   # Base image with Redis

   FROM redis:latest



   # Copy your Python application files

   COPY "/code/app.py" /app



   # Expose the Redis port

   EXPOSE 6379



   # Run the Redis server and your Python app

   CMD ["redis-server", "--daemonize", "yes"] && ["python", "/code/app.py"]
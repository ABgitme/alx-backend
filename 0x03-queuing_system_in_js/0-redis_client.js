import { createClient } from '@redis/client';

// Create a Redis client
const client = createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for errors
client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

// Connect to the Redis server
await client.connect();

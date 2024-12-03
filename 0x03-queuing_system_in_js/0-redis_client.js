import { createClient } from '@redis/client';

// Create a Redis client
const client = createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for errors
client.on('error', err => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Function to connect to Redis
async function connectRedis() {
  try {
    await client.connect();
  } catch (err) {
    console.error(`Redis client not connected to the server: ${err}`);
  }
}

// Call the function
connectRedis();

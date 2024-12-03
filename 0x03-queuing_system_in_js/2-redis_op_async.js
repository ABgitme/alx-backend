import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * Set a new key-value pair in Redis
 * @param {string} schoolName - The key
 * @param {string} value - The value
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Promisify the `get` method
const getAsync = promisify(client.get).bind(client);

/**
 * Display the value of a key in Redis using async/await
 * @param {string} schoolName - The key to retrieve
 */
async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.error(`Error retrieving value for ${schoolName}: ${err}`);
  }
}

// Perform operations
(async () => {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
  //client.quit(); // Gracefully close the client after operations
})();

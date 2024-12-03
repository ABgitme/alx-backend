import redis from 'redis';

const client = redis.createClient();

client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * Store a hash in Redis using hset
 */
function createHolbertonSchoolsHash() {
  client.hset('HolbertonSchools', 'Portland', 50, redis.print);
  client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
  client.hset('HolbertonSchools', 'New York', 20, redis.print);
  client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
  client.hset('HolbertonSchools', 'Cali', 40, redis.print);
  client.hset('HolbertonSchools', 'Paris', 2, redis.print);
}

/**
 * Display the hash stored in Redis
 */
function displayHolbertonSchoolsHash() {
  client.hgetall('HolbertonSchools', (err, res) => {
    if (err) {
      console.error(`Error retrieving hash: ${err}`);
    } else {
      console.log(res);
    }
  });
}

// Perform operations
createHolbertonSchoolsHash();
displayHolbertonSchoolsHash();

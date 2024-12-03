const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');
const express = require('express');
const app = express();
const queue = kue.createQueue();
const port = 1245;

// Connect to Redis server
const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Initialize reservationEnabled and set initial available seats
let reservationEnabled = true;
const initialSeats = 50;

// Function to reserve seats
const reserveSeat = async number => {
  await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
  const availableSeats = await getAsync('available_seats');
  return availableSeats ? parseInt(availableSeats, 10) : 0;
};

// Initialize the seats in Redis
reserveSeat(initialSeats);

// Seat reservation job processing
queue.process('reserve_seat', async (job, done) => {
  try {
    const availableSeats = await getCurrentAvailableSeats();

    if (availableSeats > 0) {
      await reserveSeat(availableSeats - 1);
      done();
      console.log(`Seat reservation job ${job.id} completed`);
    } else {
      done(new Error('Not enough seats available'));
      console.log(
        `Seat reservation job ${job.id} failed: Not enough seats available`,
      );
    }

    // Disable reservation when no seats are available
    const updatedAvailableSeats = await getCurrentAvailableSeats();
    if (updatedAvailableSeats === 0) {
      reservationEnabled = false;
    }
  } catch (err) {
    done(err);
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  }
});

// Routes
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Create and queue the job for reservation
  const job = queue.create('reserve_seat', {}).save(err => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the queue to reserve a seat
  await queue.process();
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

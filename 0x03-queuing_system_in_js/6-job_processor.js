import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Function to send notifications
function sendNotification(phoneNumber, message) {
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`,
  );
}

// Process jobs in the `push_notification_code` queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;

  try {
    sendNotification(phoneNumber, message);
    done();
  } catch (error) {
    done(error);
  }
});

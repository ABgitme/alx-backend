import kue from 'kue';

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Create a queue
const queue = kue.createQueue();

// Function to send notifications
function sendNotification(phoneNumber, message, job, done) {
  // Start tracking progress at 0%
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job if the number is blacklisted
    job.failed(new Error(`Phone number ${phoneNumber} is blacklisted`));
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Track progress to 50% if the phone number is not blacklisted
  job.progress(50, 100);

  // Log the sending notification message
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`,
  );

  // Simulate sending the notification (e.g., after a delay or some work)
  setTimeout(() => {
    // Successfully complete the job
    job.progress(100, 100);
    done();
  }, 2000);
}

// Process jobs in the queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// Function to create push notification jobs
function createPushNotificationsJobs(jobs, queue) {
  // Check if the jobs argument is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Iterate through each job and create a job in the queue
  jobs.forEach(jobData => {
    // Create a job in the queue
    const job = queue
      .create('push_notification_code_3', jobData)
      .on('enqueue', () => {
        console.log(`Notification job created: ${job.id}`);
      })
      .on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', errorMessage => {
        console.log(`Notification job ${job.id} failed: ${errorMessage}`);
      })
      .on('progress', progress => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      })
      .save(err => {
        if (err) {
          console.log('Error creating job:', err);
        }
      });
  });
}

export default createPushNotificationsJobs;

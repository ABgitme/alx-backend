import createPushNotificationsJobs from './8-job';
import kue from 'kue';
import { expect } from 'chai';

const queue = kue.createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account',
  },
];

describe('createPushNotificationsJobs', () => {
  before(function() {
    queue.testMode.enter(); // Enter test mode before running tests
  });

  afterEach(function() {
    queue.testMode.clear(); // Clear jobs after each test for isolation
  });

  after(function() {
    queue.testMode.exit(); // Exit test mode after all tests
  });

  // Test invalid inputs for jobs
  it('should throw an error if jobs is not an array', () => {
    const invalidInputs = [2, {}, 'Hello'];

    invalidInputs.forEach(input => {
      expect(() => {
        createPushNotificationsJobs(input, queue);
      }).to.throw('Jobs is not an array');
    });
  });

  // Test empty array input
  it('should not throw an error if jobs is an empty array', () => {
    const ret = createPushNotificationsJobs([], queue);
    expect(ret).to.equal(undefined);
  });

  // Test successful job creation
  it('should add two new jobs to the queue', () => {
    createPushNotificationsJobs(jobs, queue);

    // Check the length of jobs in the queue
    expect(queue.testMode.jobs.length).to.equal(2);

    // Check the first job's type and data
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql({
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account',
    });

    // Check the second job's type and data
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql({
      phoneNumber: '4153118782',
      message: 'This is the code 4321 to verify your account',
    });
  });
});

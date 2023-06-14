import queue
import threading

class MessagingQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def send_message(self, message):
        message_data = {
            'message': message,
            'acknowledged': threading.Event()  # Event to track message acknowledgement
        }
        self.queue.put(message_data)
        return message_data['acknowledged']

    def receive_message(self):
        message_data = self.queue.get()
        message = message_data['message']
        message_data['acknowledged'].set()  # Mark the message as acknowledged
        return message

# Example usage
mq = MessagingQueue()

def producer():
    for i in range(5):
        message = f"Message {i+1}"
        ack = mq.send_message(message)
        print(f"Sent: {message}")
        ack.wait()  # Wait for the message to be acknowledged

def consumer():
    for i in range(5):
        message = mq.receive_message()
        print(f"Received: {message}")
        # Simulate processing time
        threading.Event().wait(1)
        print("Acknowledging the message")

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for the threads to finish
producer_thread.join()
consumer_thread.join()

import pika
import json

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'ticket_purchase_queue'

def publish_ticket_purchase(user_info):
    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the queue (it should exist)
    channel.queue_declare(queue=QUEUE_NAME)

    # Convert user_info to JSON and publish to the queue
    message = json.dumps(user_info)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)

    print(f"Published message to {QUEUE_NAME}")

    # Close the connection
    connection.close()

if __name__ == '__main__':
    # Example user info (replace with actual data)
    user_info = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'ticket_number': '123456'
    }

    publish_ticket_purchase(user_info)


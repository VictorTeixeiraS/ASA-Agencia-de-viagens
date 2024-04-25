import pika
import smtplib
from email.mime.text import MIMEText

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'ticket_purchase_queue'

def send_email(user_info):
    # Email sending logic
    smtp_host = 'smtp.example.com'
    smtp_port = 587
    sender_email = 'enhance2forme@gmail.com'
    recipient_email = user_info['email']
    subject = 'Your Ticket Purchase'
    body = f"Hello {user_info['name']},\n\nThank you for purchasing a ticket! Your ticket number is {user_info['ticket_number']}."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()  # For secure connection
        server.login('your_email@example.com', 'your_email_password')
        server.sendmail(sender_email, recipient_email, msg.as_string())

def callback(ch, method, properties, body):
    # When a message is received, process it
    user_info = json.loads(body)
    send_email(user_info)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages():
    # Set up RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the queue (it should exist)
    channel.queue_declare(queue=QUEUE_NAME)

    # Start consuming messages
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print(f"Listening for messages on {QUEUE_NAME}...")
    channel.start_consuming()

if __name__ == '__main__':
    consume_messages()

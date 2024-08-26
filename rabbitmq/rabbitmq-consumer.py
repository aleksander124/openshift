import pika

def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")

def consume_messages():
    rabbitmq_host = '<RABBITMQ_HOST>'
    rabbitmq_port = 32111
    rabbitmq_user = 'dev-admin'
    rabbitmq_password = 'dev-admin'
    queue_name = 'test-quorum'  # Make sure this matches the queue name in your producer

    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host='dev-test',
            credentials=credentials
        )
    )
    channel = connection.channel()

    # Declare the quorum queue
    channel.queue_declare(queue=queue_name, durable=True, arguments={'x-queue-type': 'quorum'})

    # Set up the consumer with the callback function
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages()

import pika
import sys

def send_message():
    rabbitmq_host = '10.6.12.137'
    rabbitmq_port = 32111
    rabbitmq_user = 'dev-admin'
    rabbitmq_password = 'dev-admin'
    queue_name = 'test_queue'
    message = "Hello, RabbitMQ!"

    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)

    try:
        # Establish connection to RabbitMQ server
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                virtual_host='dev-test',
                credentials=credentials
            )
        )
        channel = connection.channel()

        # Declare a queue (if it doesn't already exist)
        channel.queue_declare(queue=queue_name)

        # Publish a message to the queue
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message)
        print(f" [x] Sent '{message}'")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        sys.exit(1)
    except pika.exceptions.ChannelError as e:
        print(f"Channel error occurred: {e}")
        sys.exit(1)
    except pika.exceptions.AMQPError as e:
        print(f"AMQP error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # Ensure the connection is closed, even if an error occurred
        try:
            connection.close()
        except NameError:
            # Connection was never established, nothing to close
            pass
        except Exception as e:
            print(f"Error closing connection: {e}")

if __name__ == "__main__":
    send_message()

import pika
import sys
import time

def send_message():
    rabbitmq_hosts = ['10.6.12.137', '10.6.12.138', '10.6.12.139']
    rabbitmq_port = 32111
    rabbitmq_user = 'dev-admin'
    rabbitmq_password = 'dev-admin'
    queue_name = 'test-quorum'
    message = "Hello, RabbitMQ!"
    number_of_messages = 50

    credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)

    # Create a list of connection parameters for each RabbitMQ host
    connection_params = [
        pika.ConnectionParameters(
            host=host,
            port=rabbitmq_port,
            virtual_host='dev-test',
            credentials=credentials
        ) for host in rabbitmq_hosts
    ]

    try:
        # Establish connection to the first available RabbitMQ server in the cluster
        connection = pika.BlockingConnection(parameters=connection_params)
        channel = connection.channel()

        # Declare a quorum queue
        channel.queue_declare(queue=queue_name, durable=True, arguments={'x-queue-type': 'quorum'})

        for i in range(number_of_messages):
            message_body = f"{message} #{i + 1}"
            properties = pika.BasicProperties(delivery_mode=2)  # Make message persistent

            # Publish a persistent message to the queue
            channel.basic_publish(exchange='',
                                  routing_key=queue_name,
                                  body=message_body,
                                  properties=properties)
            print(f" [x] Sent '{message_body}'")
            time.sleep(1)

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

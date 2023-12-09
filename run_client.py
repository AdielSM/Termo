from Client import Client, Logger

if __name__ == '__main__':
    client = Client()
    logger = Logger()
    client.subscribe(logger)
    client.run()
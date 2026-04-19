if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    server.serve_forever()
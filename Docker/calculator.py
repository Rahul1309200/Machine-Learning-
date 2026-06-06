from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/":
            response = """
            <h1>Calculator API</h1>
            <p>Usage: /calc?op=add&a=10&b=5</p>
            <p>Operations: add, subtract, multiply, divide</p>
            """
        elif parsed.path == "/calc":
            op = params.get("op", ["add"])[0]
            a = float(params.get("a", [0])[0])
            b = float(params.get("b", [0])[0])

            ops = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}
            result = ops.get(op, add)(a, b)
            response = f"<h1>{a} {op} {b} = {result}</h1>"
        else:
            response = "<h1>404 Not Found</h1>"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), CalculatorHandler)
    print("Calculator server running on port 8000...")
    server.serve_forever()

from flask import Flask, request
import json
from pathlib import Path

FIELDS = None
F_OUT = Path(Path.cwd(), "output.log")

app = Flask(__name__)


def write_data(headers, data):
    missing_header = False
    # write .csv headers if we're creating a new file
    if not F_OUT.exists():
        missing_header = True

    with open(F_OUT, "a", encoding="utf-8") as fp:
        if missing_header:
            fp.write(";".join(headers))
            fp.write("\n")
        data_entry = []

        for header in headers:
            try:
                data_entry.append(str(data[header]))
            except KeyError:
                data_entry.append("-")
        fp.write(";".join(data_entry))
        fp.write("\n")


def store_data(data):
    data = json.loads(request.data.decode())
    global FIELDS
    if not FIELDS:
        FIELDS = data.keys()
    write_data(FIELDS, data)


@app.route("/", methods=["POST", "GET"])
def getting_data():
    if request.method == "GET":
        return "Hello, server started"
    if request.method == "POST":
        store_data(request.data)
        return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

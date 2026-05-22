from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for macOS
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def fifo(pages, capacity):
    memory = []
    page_faults = 0
    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
    return page_faults

def lru(pages, capacity):
    memory = []
    page_faults = 0
    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                memory.pop(0)
            page_faults += 1
        else:
            memory.remove(page)
        memory.append(page)
    return page_faults

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    pages = list(map(int, request.form["pages"].split()))
    capacity = int(request.form["capacity"])

    fifo_faults = fifo(pages, capacity)
    lru_faults = lru(pages, capacity)

    # Plot and save chart
    algorithms = ['FIFO', 'LRU']
    faults = [fifo_faults, lru_faults]

    plt.figure(figsize=(5, 4))
    plt.bar(algorithms, faults, color=['orange', 'skyblue'])
    plt.title('FIFO vs LRU Page Fault Comparison')
    plt.xlabel('Algorithm')
    plt.ylabel('Page Faults')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    chart_path = "static/chart.png"
    plt.savefig(chart_path)
    plt.close()

    result_data = {
        "pages": pages,
        "capacity": capacity,
        "fifo_faults": fifo_faults,
        "lru_faults": lru_faults,
        "better": "FIFO" if fifo_faults < lru_faults else "LRU" if lru_faults < fifo_faults else "Equal"
    }

    return render_template("result.html", result=result_data, chart_path=chart_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

inventory = [
    {"id": 1, "sku": "NK-001", "brand": "Nike", "category": "athletic", "quantity": 42},
    {"id": 2, "sku": "AD-002", "brand": "Adidas", "category": "athletic", "quantity": 18},
    {"id": 3, "sku": "ZL-003", "brand": "Zella", "category": "leisure", "quantity": 35},
    {"id": 4, "sku": "BP-004", "brand": "BP.", "category": "casual", "quantity": 27},
    {"id": 5, "sku": "TN-005", "brand": "Topman", "category": "formal", "quantity": 9}
]

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/inventory")
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>")
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
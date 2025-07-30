import webbrowser
import threading
import json
import uuid
from datetime import datetime
from pathlib import Path
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


def create_app(sight_instance):
    static_folder = Path(__file__).parent / "static"

    app = Flask(__name__, static_folder=str(static_folder), static_url_path="")
    CORS(app)

    static_path = str(static_folder)

    # store operations instead of full states (caused issues)
    operations_history = []
    initial_graph_data = None

    @app.route("/")
    def index():
        return send_from_directory(static_path, "index.html")

    @app.route("/<path:path>")
    def static_files(path):
        if path and os.path.exists(os.path.join(static_path, path)):
            return send_from_directory(static_path, path)
        else:
            return send_from_directory(static_path, "index.html")

    @app.route("/api/graph-data")
    def get_graph_data():
        nonlocal initial_graph_data
        data = sight_instance.get_data()
        if initial_graph_data is None:
            initial_graph_data = {
                "nodes": json.loads(json.dumps(data["data"]["nodes"])),
                "links": json.loads(json.dumps(data["data"]["links"])),
                "faces": json.loads(json.dumps(data["data"].get("faces", []))),
            }

            original_operation = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "type": "original",
                "description": "Original graph state",
                "data": {
                    "nodeCount": len(initial_graph_data["nodes"]),
                    "linkCount": len(initial_graph_data["links"]),
                    "faceCount": len(initial_graph_data["faces"]),
                },
            }
            operations_history.append(original_operation)
        return jsonify(data)

    @app.route("/api/update-config", methods=["POST"])
    def update_config():
        config = request.json
        sight_instance.set_config(config)
        return jsonify(sight_instance.get_data())

    @app.route("/api/set-type/<graph_type>")
    def set_graph_type(graph_type):
        sight_instance.set_graph_type(graph_type)
        return jsonify(sight_instance.get_data())

    @app.route("/api/save-operation", methods=["POST"])
    def save_operation():
        try:
            operation_data = request.json

            operation_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": operation_data.get(
                    "timestamp", datetime.now().isoformat()
                ),
                "type": operation_data.get("type", "unknown"),
                "description": operation_data.get("description", "Unknown operation"),
                "data": operation_data.get("data", {}),
            }

            operations_history.append(operation_entry)

            return jsonify({"success": True, "operationId": operation_entry["id"]})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/operations-history")
    def get_operations_history():
        try:
            simplified_history = []
            for i, operation in enumerate(operations_history):
                simplified_history.append(
                    {
                        "id": operation["id"],
                        "index": i,
                        "timestamp": operation["timestamp"],
                        "type": operation["type"],
                        "description": operation["description"],
                    }
                )

            return jsonify({"history": simplified_history})

        except Exception as e:
            return jsonify({"history": [], "error": str(e)}), 500

    @app.route("/api/replay-to-operation/<int:operation_index>")
    def replay_to_operation(operation_index):
        try:
            if initial_graph_data is None:
                return jsonify({"error": "No initial graph data available"}), 400

            # start with initial graph data (deep copy to preserve colors)
            current_graph = {
                "nodes": json.loads(json.dumps(initial_graph_data["nodes"])),
                "links": json.loads(json.dumps(initial_graph_data["links"])),
                "faces": json.loads(json.dumps(initial_graph_data["faces"])),
            }

            affected_nodes_colors = {}

            # Replay operations ignoring original graph operation up to the index
            for i in range(1, min(operation_index + 1, len(operations_history))):
                operation = operations_history[i]
                current_graph, affected_nodes_colors = apply_operation(
                    current_graph, operation, affected_nodes_colors
                )

            return jsonify({"graph": current_graph})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def apply_operation(graph_data, operation, affected_nodes_colors):
        """Apply a single operation to graph data while preserving colors"""
        if operation["type"] == "cut_nodes":
            node_ids_to_cut = set(operation["data"]["nodeIds"])
            cut_color = operation["data"].get("cutColor", "#ff6969")
            affected_node_ids = set(operation["data"].get("affectedNodeIds", []))

            for node_id in affected_node_ids:
                affected_nodes_colors[node_id] = cut_color

            graph_data["nodes"] = [
                node
                for node in graph_data["nodes"]
                if node["id"] not in node_ids_to_cut
            ]

            for node in graph_data["nodes"]:
                if node["id"] in affected_nodes_colors:
                    node["color"] = affected_nodes_colors[node["id"]]

            graph_data["links"] = [
                link
                for link in graph_data["links"]
                if (
                    link["source"] not in node_ids_to_cut
                    and link["target"] not in node_ids_to_cut
                )
            ]

            graph_data["faces"] = [
                face
                for face in graph_data["faces"]
                if not any(node_id in node_ids_to_cut for node_id in face["nodes"])
            ]

        elif operation["type"] == "duplicate_nodes":
            original_node_ids = set(operation["data"]["originalNodeIds"])
            duplicated_node_ids = operation["data"]["duplicatedNodeIds"]
            duplicate_color = operation["data"].get("duplicateColor", "#69ff69")

            node_id_mapping = {}
            for i, original_id in enumerate(operation["data"]["originalNodeIds"]):
                if i < len(duplicated_node_ids):
                    node_id_mapping[original_id] = duplicated_node_ids[i]

            # Color original nodes
            for original_id in original_node_ids:
                affected_nodes_colors[original_id] = duplicate_color

            # Create duplicate nodes
            for original_id in original_node_ids:
                original_node = next(
                    (node for node in graph_data["nodes"] if node["id"] == original_id),
                    None,
                )
                if original_node and original_id in node_id_mapping:
                    duplicated_id = node_id_mapping[original_id]
                    duplicated_node = json.loads(json.dumps(original_node))  # Deep copy
                    duplicated_node["id"] = duplicated_id
                    duplicated_node["color"] = duplicate_color

                    # Offset position slightly for visibility
                    if "x" in duplicated_node:
                        duplicated_node["x"] += hash(duplicated_id) % 40 - 20
                    if "y" in duplicated_node:
                        duplicated_node["y"] += hash(duplicated_id) % 40 - 20
                    if "z" in duplicated_node:
                        duplicated_node["z"] += hash(duplicated_id) % 40 - 20

                    graph_data["nodes"].append(duplicated_node)
                    affected_nodes_colors[duplicated_id] = duplicate_color

            new_links = []
            for link in graph_data["links"]:
                source_id = link["source"]
                target_id = link["target"]

                if (
                    source_id in original_node_ids
                    and target_id not in original_node_ids
                ):
                    if source_id in node_id_mapping:
                        new_link = json.loads(json.dumps(link))
                        new_link["source"] = node_id_mapping[source_id]
                        new_links.append(new_link)

                elif (
                    source_id not in original_node_ids
                    and target_id in original_node_ids
                ):
                    if target_id in node_id_mapping:
                        new_link = json.loads(json.dumps(link))
                        new_link["target"] = node_id_mapping[target_id]
                        new_links.append(new_link)

                elif source_id in original_node_ids and target_id in original_node_ids:
                    if source_id in node_id_mapping and target_id in node_id_mapping:
                        new_link = json.loads(json.dumps(link))
                        new_link["source"] = node_id_mapping[source_id]
                        new_link["target"] = node_id_mapping[target_id]
                        new_links.append(new_link)

            graph_data["links"].extend(new_links)

            new_faces = []
            for face in graph_data["faces"]:
                has_selected_node = any(
                    node_id in original_node_ids for node_id in face["nodes"]
                )

                # If face contains selected nodes, create a duplicate face
                if has_selected_node:
                    new_face = json.loads(json.dumps(face))  # Deep copy
                    new_face["id"] = f"{face['id']}_duplicate_{str(uuid.uuid4())[:8]}"

                    # Replace selected nodes with duplicates
                    new_face_nodes = []
                    for node_id in face["nodes"]:
                        if node_id in original_node_ids and node_id in node_id_mapping:
                            new_face_nodes.append(node_id_mapping[node_id])
                        else:
                            new_face_nodes.append(node_id)

                    new_face["nodes"] = new_face_nodes
                    new_faces.append(new_face)

            # Add the new faces
            graph_data["faces"].extend(new_faces)

            # Apply colors
            for node in graph_data["nodes"]:
                if node["id"] in affected_nodes_colors:
                    node["color"] = affected_nodes_colors[node["id"]]

        return graph_data, affected_nodes_colors

    return app


def run_server(sight_instance, port=5050):
    """Run the visualization server"""
    app = create_app(sight_instance)

    # auto open browser
    url = f"http://localhost:{port}"
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    print(f"Zen Sight running at {url}")
    print("Press Ctrl+C to stop")

    app.run(port=port, debug=False)

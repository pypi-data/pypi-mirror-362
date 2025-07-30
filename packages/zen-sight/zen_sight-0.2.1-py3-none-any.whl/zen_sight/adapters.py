from zen_sight import Sight
import networkx as nx
from zen_mapper.types import MapperResult
import numpy as np


def vis_zen_mapper(
    result: MapperResult,
    data: np.ndarray = None,
    projection: np.ndarray = None,
    port: int = 5050,
):
    nodes = []
    links = []
    faces = []

    try:
        for i, node_simplex in enumerate(result.nerve[0]):
            node_id = node_simplex[0]

            cluster_indices = []
            if node_id < len(result.nodes):
                cluster_data = result.nodes[node_id]
                if hasattr(cluster_data, "tolist"):
                    cluster_indices = cluster_data.tolist()
                elif hasattr(cluster_data, "__iter__"):
                    cluster_indices = list(cluster_data)
                else:
                    cluster_indices = [cluster_data]

            node_data = {
                "id": str(node_id),
                "name": f"Node {node_id} with {len(cluster_indices)} datapoints",
                "mapperNodeId": int(node_id),
                "clusterIndices": cluster_indices,
                "clusterSize": len(cluster_indices),
                "stats": {},
            }

            if data is not None and len(cluster_indices) > 0:
                try:
                    cluster_data_points = data[cluster_indices]
                    node_data["originalDataPoints"] = cluster_data_points.tolist()
                    node_data["stats"] = {
                        "mean": str(np.mean(cluster_data_points, axis=0)),
                        "std": str(np.std(cluster_data_points, axis=0)),
                        "min": str(np.min(cluster_data_points, axis=0)),
                        "max": str(np.max(cluster_data_points, axis=0)),
                    }
                except (IndexError, TypeError):
                    node_data["originalDataPoints"] = None

            if projection is not None and len(cluster_indices) > 0:
                try:
                    cluster_projections = projection[cluster_indices]
                    node_data["projectionValues"] = cluster_projections.tolist()

                    # Compute per-dimension projection statistics
                    node_data["stats"]["projectionMean"] = str(
                        np.mean(cluster_projections, axis=0)
                    )
                    node_data["stats"]["projectionStd"] = str(
                        np.std(cluster_projections, axis=0)
                    )

                    # overall statistics
                    node_data["stats"]["projectionMeanOverall"] = str(
                        np.mean(cluster_projections)
                    )
                    node_data["stats"]["projectionStdOverall"] = str(
                        np.std(cluster_projections)
                    )

                except (IndexError, TypeError):
                    node_data["projectionValues"] = None

            nodes.append(node_data)

        for edge in result.nerve[1]:
            source_id, target_id = edge[0], edge[1]

            source_cluster = []
            target_cluster = []

            if source_id < len(result.nodes):
                source_data = result.nodes[source_id]
                if hasattr(source_data, "tolist"):
                    source_cluster = source_data.tolist()
                elif hasattr(source_data, "__iter__"):
                    source_cluster = list(source_data)

            if target_id < len(result.nodes):
                target_data = result.nodes[target_id]
                if hasattr(target_data, "tolist"):
                    target_cluster = target_data.tolist()
                elif hasattr(target_data, "__iter__"):
                    target_cluster = list(target_data)

            intersection = list(set(source_cluster) & set(target_cluster))

            link_data = {
                "source": str(source_id),
                "target": str(target_id),
                "mapperEdge": [int(edge[0]), int(edge[1])],
                "intersectionIndices": intersection,
                "intersectionSize": len(intersection),
                "sourceClusterSize": len(source_cluster),
                "targetClusterSize": len(target_cluster),
            }

            if data is not None and len(intersection) > 0:
                try:
                    link_data["intersectionDataPoints"] = data[intersection].tolist()
                except (IndexError, TypeError):
                    link_data["intersectionDataPoints"] = None

            if projection is not None and len(intersection) > 0:
                try:
                    link_data["intersectionProjectionValues"] = projection[
                        intersection
                    ].tolist()
                except (IndexError, TypeError):
                    link_data["intersectionProjectionValues"] = None

            links.append(link_data)

        # Process faces - create face objects with id and nodes properties
        for face_idx, face in enumerate(result.nerve[2]):
            face_vertices = [
                str(v) for v in face
            ]  # Convert to strings to match node IDs

            if len(face_vertices) == 3:
                face_data = {
                    "id": f"face_{face_idx}",
                    "nodes": face_vertices,
                    "type": "triangle",
                    "mapperFace": [int(v) for v in face],
                }
                faces.append(face_data)

    except Exception as e:
        print(f"Error processing mapper data: {e}")
        for i in result.nerve[0]:
            nodes.append(
                {
                    "id": str(i[0]),
                    "name": f"Node {i[0]}",
                }
            )
        for edge in result.nerve[1]:
            links.append(
                {
                    "source": str(edge[0]),
                    "target": str(edge[1]),
                }
            )
        # Fallback
        for face_idx, face in enumerate(result.nerve[2]):
            face_vertices = [str(v) for v in face]
            if len(face_vertices) == 3:
                face_data = {
                    "id": f"face_{face_idx}",
                    "nodes": face_vertices,
                    "type": "triangle",
                    "mapperFace": [int(v) for v in face],
                }
                faces.append(face_data)

    sight = Sight()

    try:
        nodes_list = list(result.nodes) if hasattr(result.nodes, "__iter__") else []
        nerve_0_list = (
            list(result.nerve[0]) if hasattr(result.nerve[0], "__iter__") else []
        )
        nerve_1_list = (
            list(result.nerve[1]) if hasattr(result.nerve[1], "__iter__") else []
        )
        nerve_2_list = (
            list(result.nerve[2])
            if len(result.nerve) > 2 and hasattr(result.nerve[2], "__iter__")
            else []
        )

        sight.set_metadata(
            {
                "mapperResult": {
                    "totalNodes": len(nodes_list),
                    "nerveComplexity": {
                        "vertices": len(nerve_0_list),
                        "edges": len(nerve_1_list),
                        "faces": len(nerve_2_list),
                    },
                    "hasOriginalData": data is not None,
                    "hasProjectionData": projection is not None,
                    "dataShape": list(data.shape) if data is not None else None,
                    "projectionShape": (
                        list(projection.shape) if projection is not None else None
                    ),
                }
            }
        )
    except Exception as e:
        print(f"Error setting metadata: {e}")

    sight.set_nodes(nodes)
    sight.set_links(links)
    sight.set_faces(faces)

    sight.set_config(
        {
            "nodeAutoColorBy": "clusterSize",
            "nodeRelSize": 4,
            "nodeOpacity": 1,
            "nodeLabel": "name",
            "linkColor": "#000000",
            "linkWidth": 1,
            "linkOpacity": 1,
            "backgroundColor": "#f2f2f2",
            "faceFillColor": "rgba(52, 152, 219, 0.3)",
            "faceStrokeColor": "rgba(52, 152, 219, 0.5)",
            "faceStrokeWidth": 1,
            "faceOpacity": 0.3,
        }
    )
    sight.show(port=port)

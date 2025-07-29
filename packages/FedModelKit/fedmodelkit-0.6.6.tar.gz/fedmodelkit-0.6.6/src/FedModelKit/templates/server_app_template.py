
# from tkinter import Grid
from typing import List
import time

import flwr as fl
from flwr.common import (
    Context,
    NDArrays,
    Message,
    MessageType,
    Metrics,
    RecordDict,
    ConfigRecord,
    DEFAULT_TTL,
)
from flwr.server import Grid

from EXPERIMENT_NAME.task import Net, Strategy #type: ignore[import]


# Run via `flower-server-app server:app`
app = fl.server.ServerApp()




@app.main()
def main(grid: Grid, context: Context):
    """
    Main function to run the federated learning server.

    Structure:
    - Send a query message to clients for creating the local learner and loading the data
    - Start global epochs loop for training and evaluation
        - Send training messages to clients
        - Aggregate parameters received from clients
        - Send evaluation messages to clients
        - Aggregate evaluation metrics
    """
    print("Starting test run")

    # Get node IDs of connected clients
    node_ids = grid.get_node_ids()

    # Initialize the federated model
    global_model = Net()
    aggregation_strategy = Strategy()

    # Send a query message to clients for creating the local learner and loading the data
    messages = []
    for idx, node_id in enumerate(node_ids):
        # Create messages to send to clients
        record_dict = RecordDict()

        # Add a config with information to send the client for the query
        record_dict.config_records["fancy_config"] = ConfigRecord({"num_clients": len(node_ids), "client_id": idx})

        # Create a query message for each client
        message = Message(
            content=record_dict,
            message_type=MessageType.QUERY,
            dst_node_id=node_id,
            group_id=str(1),
            ttl=DEFAULT_TTL,
        )
        messages.append(message)

    # Send training messages to clients
    all_replies = list(grid.send_and_receive(messages))
    print(f"Received {len(all_replies)} answers")
    

    # Run federated training and evaluation for a fixed number of rounds
    for server_round in range(3):
        print(f"Commencing server train and evaluation round {server_round + 1}")

        messages = []
        for idx, node_id in enumerate(node_ids):
            # Create messages to send to clients
            record_dict = RecordDict()

            # Add model parameters to record
            record_dict.array_records["fancy_model"] = global_model.get_parameters()
            # Add a config with information to send the client for training
            record_dict.config_records["fancy_config"] = ConfigRecord({"local_epochs": 3})

            # Create a training message for each client
            message = Message(
                content=record_dict,
                message_type=MessageType.TRAIN,
                dst_node_id=node_id,
                group_id=str(server_round),
                ttl=DEFAULT_TTL,
            )
            messages.append(message)

        # Send training messages to clients
        all_replies = list(grid.send_and_receive(messages))
        print(f"Received {len(all_replies)} results")

        # Print metrics received from clients
        for reply in all_replies:
            print(reply.content.metric_records)

        # Aggregate parameters received from clients
        array_records_list = [reply.content.array_records["fancy_model_returned"] for reply in all_replies]
        new_array_records = aggregation_strategy.aggregate_parameters(array_records_list)
        global_model.set_parameters(new_array_records)

        # Evaluate the updated global model
        messages = []
        for idx, node_id in enumerate(node_ids):
            # Create evaluation messages for clients
            record_dict = RecordDict()

            # Add updated model parameters to record
            record_dict.array_records["fancy_model"] = new_array_records
            # Add a config with information to send the client for evaluation
            record_dict.config_records["fancy_config"] = ConfigRecord({"local_epochs": 3})

            # Create an evaluation message for each client
            message = Message(
                content=record_dict,
                message_type=MessageType.EVALUATE,
                dst_node_id=node_id,
                group_id=str(server_round),
                ttl=DEFAULT_TTL,
            )
            messages.append(message)

        # Send evaluation messages to clients
        all_replies = list(grid.send_and_receive(messages))
        print(f"Received {len(all_replies)} results")

        # Print evaluation metrics received from clients
        metrics_records_list = [reply.content.metric_records['eval_metrics'] for reply in all_replies]
        for i, reply in enumerate(all_replies):
            print(f"Client {i+1} metrics:   ", reply.content.metric_records['eval_metrics'])

        # Aggregate evaluation metrics
        print("Aggregated metrics result:   ", aggregation_strategy.aggregate_metrics(metrics_records_list))
    
    print("🎉🎉🎉 Successfully completed federated learning run! 🎉🎉🎉")

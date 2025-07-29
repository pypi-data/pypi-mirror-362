import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from flwr.client import ClientApp
from flwr.common import Message, Context
from flwr.common.record import RecordDict, MetricRecord, ConfigRecord
from sklearn.preprocessing import OneHotEncoder
import FedModelKit as msi
import FedModelKit as msi

from EXPERIMENT_NAME.task import Net # Type: ignore[import]


# Initialize the Flower ClientApp
app = ClientApp()

@app.query()
def query(msg: Message, ctx: Context) -> Message:
    """
    Query function to be executed by the Flower client. This function handles the
    initial configuration sent by the server.
    """

    # Retrieve the configuration sent by the server
    fancy_config = msg.content.config_records['fancy_config']
    
    # Instantiate the federated model
    federated_model = Net()

    # Load the client split data using the load_data function
    federated_model.prepare_data(fancy_config['client_id'], fancy_config['num_clients'])

    # Store the local learner and the data split in the context
    # To store in context other objects, you can use ctx.state.<object_name> = <object>
    ctx.state.local_learner = federated_model

    return Message(RecordDict(), reply_to=msg)

@app.train()
def train(msg: Message, ctx: Context):
    """
    Train function to be executed by the Flower client.
    This function handles the training of the local model using the data provided.
    """

    # Retrieve the local learner and the client split from the context
    local_learner = ctx.state.local_learner

    # Retrieve configuration sent by the server - example
    #fancy_config = msg.content.configs_records['fancy_config']
    #local_epochs = fancy_config['local_epochs']

    # Retrieve the model parameters sent by the server
    fancy_parameters = msg.content.array_records['fancy_model']
    local_learner.set_parameters(fancy_parameters)    

    # Perform local training and obtain training metrics
    train_metrics = local_learner.train_round()

    # Retrieve the trained model parameters
    new_array_records = local_learner.get_parameters()

    # Construct a reply message carrying updated model parameters and generated metrics
    reply_content = RecordDict()
    reply_content.array_records['fancy_model_returned'] = new_array_records
    reply_content.metric_records['train_metrics'] = MetricRecord(train_metrics)

    # Store the metrics and the local learner in the context for future reference
    ctx.state.metric_records['prev'] = MetricRecord(train_metrics)
    ctx.state.local_learner =  local_learner

    # Return the reply message to the server
    return Message(reply_content, reply_to=msg)

@app.evaluate()
def eval(msg: Message, ctx: Context):
    """
    Evaluate function to be executed by the Flower client.
    This function handles the evaluation of the local model using the data provided.
    """

    # Retrieve the local learner and the client split from the context
    local_learner = ctx.state.local_learner

    # Retrieve configuration sent by the server - example
    #fancy_config = msg.content.configs_records['fancy_config']
    #local_epochs = fancy_config['local_epochs']

    # Retrieve the model parameters sent by the server
    fancy_parameters = msg.content.array_records['fancy_model']
    local_learner.set_parameters(fancy_parameters)

    # Evaluate the model and obtain evaluation metrics
    eval_metrics = local_learner.evaluate()

    # Construct a reply message with evaluation metrics
    reply_content = RecordDict()
    reply_content.metric_records['eval_metrics'] = MetricRecord(eval_metrics)

    # Store the metrics and the local learner in the context for future reference
    ctx.state.metric_records['prev'] = MetricRecord(eval_metrics)
    ctx.state.local_learner =  local_learner

    # Return the reply message to the server
    return Message(reply_content, reply_to=msg)

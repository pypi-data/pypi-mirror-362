from collections import OrderedDict

import torch
import torch.nn as nn
import torch.optim as optim
import flwr
import numpy as np
from typing import Optional
from flwr_datasets import FederatedDataset
from flwr_datasets.partitioner import IidPartitioner
from imblearn.over_sampling import SMOTE
from loguru import logger
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset


def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.xpu.is_available():
        return torch.device("xpu")
    else:
        return torch.device("cpu")


DEVICE = get_device()
logger.info(f"Using device: {DEVICE}")


class Net(nn.Module):
    def __init__(self, input_dim=6):
        super(Net, self).__init__()
        self.trainloader = None
        self.testloader = None
        self.fds = None  # Cache FederatedDataset
        # First layer with more units and batch normalization
        self.layer1 = nn.Sequential(
            nn.Linear(input_dim, 32),  # Increased from 20 to 32
            nn.BatchNorm1d(32),  # Added batch normalization
            nn.LeakyReLU(0.1),  # LeakyReLU instead of ReLU
            nn.Dropout(0.2),  # Increased dropout
        )

        # Second layer with more units
        self.layer2 = nn.Sequential(
            nn.Linear(32, 24),  # Increased from 14 to 24
            nn.BatchNorm1d(24),  # Added batch normalization
            nn.LeakyReLU(0.1),
            nn.Dropout(0.25),
        )

        # Third layer
        self.layer3 = nn.Sequential(
            nn.Linear(24, 16), nn.BatchNorm1d(16), nn.LeakyReLU(0.1)
        )

        # Output layer
        self.output_layer = nn.Sequential(nn.Linear(16, 1), nn.Sigmoid())

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output_layer(x)
        return x
    
    


    def dataset_processing(
        self, train_df: DataFrame, test_df: DataFrame
    ) -> tuple[DataLoader, DataLoader]:
        def preprocess_df(df: DataFrame) -> DataFrame:
            columns_to_drop = ["SkinThickness", "Insulin"]
            df_new: DataFrame = df.drop(columns_to_drop, axis=1)

            # Calculate mean and median (excluding zeros)
            mean_glucose = df_new[df_new["Glucose"] != 0]["Glucose"].mean()
            median_bmi = df_new[df_new["BMI"] != 0]["BMI"].median()
            median_bp = df_new[df_new["BloodPressure"] != 0]["BloodPressure"].median()

            # Replace zeros values with mean/median
            df_new.replace(
                {
                    "Glucose": {0: mean_glucose},
                    "BMI": {0: median_bmi},
                    "BloodPressure": {0: median_bp},
                },
                inplace=True,
            )

            return df_new

        # Preprocess both datasets
        train_processed = preprocess_df(train_df)
        test_processed = preprocess_df(test_df)

        # Split features and labels for both sets
        X_train = train_processed.values[:, :6]
        y_train = train_processed.values[:, 6:]
        X_test = test_processed.values[:, :6]
        y_test = test_processed.values[:, 6:]

        from collections import Counter

        def get_minority_class_count(y):
            return min(Counter(y.flatten()).values())

        minority_count = get_minority_class_count(y_train)
        k_neighbors = min(5, minority_count - 1) if minority_count > 1 else 1

        # Resample the training data to fix the class imbalance
        smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

        # Scale the data to have zero mean and unit variance
        scaler = StandardScaler()
        X_train_resampled = scaler.fit_transform(X_train_resampled)
        X_test = scaler.transform(X_test)

        # Convert numpy arrays to PyTorch tensors
        X_train_tensor = torch.FloatTensor(X_train_resampled)
        y_train_tensor = torch.FloatTensor(y_train_resampled).reshape(
            -1, 1
        )  # Add this reshape
        X_test_tensor = torch.FloatTensor(X_test)
        y_test_tensor = torch.FloatTensor(y_test).reshape(-1, 1)

        # Create datasets and dataloaders
        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

        train_loader = DataLoader(dataset=train_dataset, batch_size=10, shuffle=True)
        test_loader = DataLoader(
            dataset=test_dataset, batch_size=len(test_dataset), shuffle=False
        )

        return train_loader, test_loader

    def _parameters_to_dict(self, params_record: flwr.common.ParametersRecord) -> OrderedDict:
        # Convert ParametersRecord to an OrderedDict
        state_dict = OrderedDict()
        for k, v in params_record.items():
            state_dict[k] = self._basic_array_deserialisation(v)
        return state_dict

    def _dict_to_parameter_record(self, 
        parameters: OrderedDict["str", flwr.common.NDArray],
    ) -> flwr.common.ParametersRecord:
        # Convert OrderedDict to ParametersRecord
        state_dict = OrderedDict()
        for k, v in parameters.items():
            state_dict[k] = self._ndarray_to_array(v)

        return flwr.common.ParametersRecord(state_dict)

    def _ndarray_to_array(self, ndarray: flwr.common.NDArray) -> flwr.common.Array:
        """Represent NumPy ndarray as Array."""
        return flwr.common.Array(
            data=ndarray.tobytes(),
            dtype=str(ndarray.dtype),
            stype="numpy.ndarray.tobytes",
            shape=list(ndarray.shape),
        )

    def _basic_array_deserialisation(self, array: flwr.common.Array) -> flwr.common.NDArray:
        # Deserialize Array to NumPy ndarray
        return np.frombuffer(buffer=array.data, dtype=array.dtype).reshape(array.shape)

    def load_syftbox_dataset(self) -> None: 
        import pandas as pd

        from syft_flwr.utils import get_syftbox_dataset_path

        data_dir = get_syftbox_dataset_path()
        logger.info(f"Loading dataset from {data_dir}")

        train_df = pd.read_csv(data_dir / "train.csv")
        test_df = pd.read_csv(data_dir / "test.csv")

        self.trainloader, self.testloader = self.dataset_processing(train_df, test_df)


    def load_flwr_data(
        self, partition_id: int, num_partitions: int
    ) -> None:
        """
        Load the `fl-diabetes-prediction` dataset to memory
        """
        # global fds
        if self.fds is None:
            partitioner = IidPartitioner(num_partitions=num_partitions)
            self.fds = FederatedDataset(
                dataset="khoaguin/pima-indians-diabetes-database",
                partitioners={"train": partitioner},
            )

        partition: DataFrame = self.fds.load_partition(partition_id, "train").with_format(
            "pandas"
        )[:]
        train_df, test_df = train_test_split(partition, test_size=0.2, random_state=95)

        self.trainloader, self.testloader = self.dataset_processing(train_df, test_df)


    def prepare_data(
        self, partition_id: int, num_partitions: int
    ) -> None:
        from syft_flwr.utils import run_syft_flwr
        if not run_syft_flwr():
            logger.info("Running flwr locally")
            self.load_flwr_data(
                partition_id=partition_id,
                num_partitions=num_partitions,
            )
        else:
            logger.info("Running with syft_flwr")
            self.load_syftbox_dataset()


    def train_round(self, local_epochs=1):
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.parameters(), lr=0.001, weight_decay=0.0005)
        history = {"train_loss": [], "train_acc": []}
        self.to(DEVICE)

        for epoch in range(local_epochs):
            self.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for inputs, labels in self.trainloader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

                optimizer.zero_grad()
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                predicted = (outputs > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            epoch_loss = running_loss / len(self.trainloader.dataset)
            epoch_acc = correct / total
            history["train_loss"].append(epoch_loss)
            history["train_acc"].append(epoch_acc)

        return history


    def evaluate(self):
        self.to(DEVICE)
        self.eval()
        criterion = nn.BCELoss()

        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in self.testloader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                running_loss += loss.item() * inputs.size(0)
                predicted = (outputs > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(self.testloader.dataset)
        epoch_acc = correct / total

        return {"epoch_loss": epoch_loss, "epoch_accuracy": epoch_acc}


    def get_parameters(self) -> flwr.common.ArrayRecord:
        return self.pytorch_to_parameter_record(self.state_dict())

    def set_parameters(self, parameters: flwr.common.ArrayRecord) -> None:
        self.load_state_dict(self.parameters_to_pytorch_state_dict(parameters))

    def pytorch_to_parameter_record(
        self, state_dict: dict,
    ) -> flwr.common.ArrayRecord:
        """Serialise your PyTorch model."""
        transformed_state_dict = OrderedDict()

        for k, v in state_dict.items():
            transformed_state_dict[k] = self._ndarray_to_array(v.cpu().numpy())

        return flwr.common.ArrayRecord(transformed_state_dict)

    def parameters_to_pytorch_state_dict(
        self, params_record: flwr.common.ArrayRecord,
    ) -> dict:
        # Make sure to import locally torch as it is only available in the server
        import torch

        """Reconstruct PyTorch state_dict from its serialised representation."""
        state_dict = {}
        for k, v in params_record.items():
            state_dict[k] = torch.tensor(self._basic_array_deserialisation(v))

        return state_dict


class Strategy:

    def _parameters_to_dict(self, params_record: flwr.common.ArrayRecord) -> OrderedDict:
        # Convert ParametersRecord to an OrderedDict
        state_dict = OrderedDict()
        for k, v in params_record.items():
            state_dict[k] = self._basic_array_deserialisation(v)
        return state_dict

    def _dict_to_parameter_record(self, 
        parameters: OrderedDict["str", flwr.common.NDArray],
    ) -> flwr.common.ArrayRecord:
        # Convert OrderedDict to ParametersRecord
        state_dict = OrderedDict()
        for k, v in parameters.items():
            state_dict[k] = self._ndarray_to_array(v)

        return flwr.common.ArrayRecord(state_dict)

    def _ndarray_to_array(self, ndarray: flwr.common.NDArray) -> flwr.common.Array:
        """Represent NumPy ndarray as Array."""
        return flwr.common.Array(
            data=ndarray.tobytes(),
            dtype=str(ndarray.dtype),
            stype="numpy.ndarray.tobytes",
            shape=list(ndarray.shape),
        )

    def _basic_array_deserialisation(self, array: flwr.common.Array) -> flwr.common.NDArray:
        # Deserialize Array to NumPy ndarray
        return np.frombuffer(buffer=array.data, dtype=array.dtype).reshape(array.shape)

    def aggregate_parameters(self, results: list[flwr.common.ArrayRecord], config: Optional[flwr.common.ConfigRecord]=None
        ) -> flwr.common.ArrayRecord:
            parameters = [self._parameters_to_dict(param) for param in results]
            keys = parameters[0].keys()
            result = OrderedDict()
            for key in keys:
                # Init array
                this_array: np.ndarray = np.zeros_like(parameters[0][key])
                for p in parameters:
                    this_array += p[key]
                result[key] = this_array / len(results)
            return self._dict_to_parameter_record(result)

    def aggregate_metrics(self, results: list[flwr.common.MetricRecord], config: Optional[flwr.common.ConfigRecord]=None) -> flwr.common.MetricRecord:
            keys = results[0].keys()
            result = OrderedDict()
            for key in keys:
                # Init array
                cumsum = 0.0
                for m in results:
                    if not isinstance(m[key], (int, float)):
                        raise ValueError(
                            f"flwr.common.MetricsRecord value type not supported: {type(m[key])}"
                        )
                    cumsum += m[key]  # type: ignore
                result[key] = cumsum / len(results)
            return flwr.common.MetricRecord(result)
from pathlib import Path
from torch import nn
import lightning as L
import torchapp as ta
from torch.utils.data import DataLoader
from rich.console import Console
console = Console()

class {{ cookiecutter.app_name }}(ta.TorchApp):
    """
    {{ cookiecutter.description }}
    """
    def data(
        self,
        inputs:Path = ta.Param(help="The input file."), 
        batch_size:int = ta.Param(default=32, help="The batch size."),
    ) -> L.LightningDataModule:
        """
        Creates a LightningDataModule object which {{ cookiecutter.app_name }} uses in training.

        Args:
            inputs (Path): The input file.
            batch_size (int, optional): The number of elements to use in a batch for training. Defaults to 32.

        Returns:
            LightningDataModule: The LightningDataModule object.
        """
        raise NotImplemented("Dataloaders function not implemented yet.") 

    def model(
        self,
    ) -> nn.Module:
        """
        Creates a deep learning model for the {{ cookiecutter.app_name }} to use.

        Returns:
            nn.Module: The created model.
        """
        raise NotImplemented("Model function not implemented yet.") 
        return nn.Sequential(
        )

    @ta.method
    def loss_function(self):
        return nn.CrossEntropyLoss()

    @ta.method
    def prediction_dataloader(
        self, 
        module, 
        batch_size:int = 32,
        **kwargs
    ) -> DataLoader:
        """
        Creates a dataloader for prediction.

        Args:
            module (nn.Module): The model to use for prediction.
            batch_size (int, optional): The number of elements to use in a batch for prediction. Defaults to 32.

        Returns:
            DataLoader: The dataloader for the prediction step.
        """
        raise NotImplemented("Prediction dataloader function not implemented yet.")

    @ta.method
    def output_results(
        self, 
        results, 
        output_csv:Path = None,
        **kwargs
    ):
        """
        Outputs the results of the model predictions.
        Args:
            results: The results of the model predictions.
            output_csv (Path, optional): Path to write predictions in CSV format. Defaults to None.
        """
        raise NotImplemented("Output Results function not implemented yet.") 

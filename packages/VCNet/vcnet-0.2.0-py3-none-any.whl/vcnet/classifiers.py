"""Classifier Models for VCNet.

A VCNet architecture is made of a counterfactual generator and a classifier. 
This module implements the classes for defining classifiers in the architecture.

Two classes are provided:

* :py:class:`Classifier`: the implementation of a default classifier architecture for the
  joint-model of VCNet.
  It is implemented as lighting module. The same architecture can be ued in a post-hoc model. 
* :py:class:`SKLearnClassifier`: the embedding of a shallow classifier to explain with post-hoc.


.. note::
    You can define you own classifier by inheriting from one of these two classes. 


.. warning::
    :py:class:`SKLearnClassifier` can not be used in a joint-learning fashion. 

"""
import warnings
import torch
import torch.nn as nn
import torch.optim as optim
import lightning as L
import pandas as pd

# pylint: disable=W0611
# pylint: disable=W0123
# pylint: disable=C0103

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


class SKLearnClassifier:
    """Wrapper for using a sklearn classifiers in the VCNet pipeline.

    Args:
        hp (Dict): configuration of the classifier (hyperparameters) and the dataset
    
    Example of minimal configuration:
    ---------------------------------
    Exemple of minimal dictionary to set up a :py:class:`SKLearnClassifier` in VCNet.

    .. code-block:: python
    
        hp = {
            "dataset": {
                "target":"income",
            },
            "classifier_params" : {
                "skname":  "RandomForestClassifier",
                "kwargs": {
                    "n_estimators" : 50,
                }
            }
        }
        classifier = SKLearnClassifier(hp)
        classifier.fit(dataset.df_train)

    .. note::
        This class allows to use an `XGBoostClassifier` as classifier.

    .. note::
        We refer the user to the `sklearn` API to check the list of the classifier parameters. 
        In case of use of XGBoost, parameters can be checked in the (XGBoost API)[https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html]
    """

    def __init__(self, hp):
        if "classifier_params" in hp and "skname" in hp["classifier_params"]:
            if "kwargs" in hp["classifier_params"]:
                self.clf = eval(hp["classifier_params"]["skname"])(
                    **hp["classifier_params"]["kwargs"]
                )
            else:
                self.clf = eval(hp["classifier_params"]["skname"])()
            self.hp = hp
        else:
            raise RuntimeError(
                "invalid parameters: the ['classifier_params']['skname'] parameter is missing."
            )

    def __call__(self, x: torch.tensor) -> torch.tensor:
        """Application of the classifier on a tensor

        Args:
            x (torch.tensor): tensor to classify

        Returns:
            np.array: vector containing the probability of the class 1
        """
        p = self.clf.predict_proba(x.detach().cpu())
        return torch.tensor(p, dtype=torch.float32, requires_grad=False, device=device)

    def fit(self, X: pd.DataFrame):
        """function to fit the model

        Args:
            X (pd.DataFrame): dataset to train the model on
        """
        self.clf.fit(
            X.drop(self.hp["dataset"]["target"], axis=1).to_numpy(),
            X[self.hp["dataset"]["target"]],
        )


class Classifier(L.LightningModule):
    """Simple fully convolutional classifier that is used bu default for the classification
    of numerical tabular data.

    The network architecture is made of 3 fully connected layers, with relu activation
    function between layers and a sigmoid at the end. 

    The size of the layers are defined in the hyperparameters provided while the model
    is instanciated.

    The mandatory parameters to define in the dictionary are:
    
        * the input size (in `dataset`>`feature_sze`)
        * the layer sizes (in the `classifier_params` : `l1_size`, `l2_size` and `l3_size`
        * the output size (in `dataset`>`class_sze`)

    The learning rate (defined by `lr` in the `classifier_params`) is also recommanded. It's 
    default value is 0.01.

    Args:
        hp (Dict): configuration of the classifier (hyperparameters) and the dataset.

    Raise:
        KeyError is the settings does not contain all required parameter
    """

    def __init__(self, hp):
        super().__init__()

        self._hp = hp

        try:
            self.model = nn.Sequential(
                nn.Linear(
                    hp["dataset"]["feature_size"], hp["classifier_params"]["l1_size"]
                ),
                nn.ReLU(),
                # nn.BatchNorm1d(hp['classifier_params']["l1_size"]),
                # nn.Dropout(p=0.1),
                nn.Linear(
                    hp["classifier_params"]["l1_size"], hp["classifier_params"]["l2_size"]
                ),
                nn.ReLU(),
                # nn.BatchNorm1d(hp['classifier_params']["l2_size"]),
                # nn.Dropout(p=0.1),
                nn.Linear(
                    hp["classifier_params"]["l2_size"], hp["classifier_params"]["l3_size"]
                ),
                nn.ReLU(),
                nn.Linear(
                    hp["classifier_params"]["l3_size"], hp["dataset"]["class_size"]
                ),
                nn.Sigmoid(),
            )
        except KeyError:
            print("VCNet classifier: missing mandatory attribute in the \
                  definition of the classifier.\n")

        if "lr" not in hp["classifier_params"]:
            self._hp["classifier_params"]["lr"]=0.01
            warnings.warn("VCNet classifier: default learning rate is set to 0.01")
        
    def forward(self, x: torch.tensor) -> torch.tensor:  # pylint: disable=W0221
        """Apply the classification model on the input `x`.
        
        Args:
            x (torch.tensor): tensor of example to classify.

        Returns:
            torch.tensor: the probabilistic classification vector
        """
        return self.model(x)

    def training_step(self, batch, batch_idx) -> float:  # pylint: disable=W0221,W0613
        """Implementation of a training step
        """
        x, y = batch
        output_class = self.forward(x).squeeze()
        loss = nn.BCELoss(reduction="sum")(output_class, y)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(
            self.parameters(), lr=self._hp["classifier_params"]["lr"]
        )
        return optimizer

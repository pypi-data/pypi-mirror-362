import os
from typing import Any
import importlib
import logging
import sys
import yaml
from collections import namedtuple
from typing import List
from aydie_mllib.exception import AydieException

# Import all the constants from the constants file.
from aydie_mllib.constants import *

# Setting up the logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Using named tuple for return values for making it easy to read and documentable.

# Represents a model that has been initialised from the config file, but not yet trained.
InitializedModelDetail = namedtuple("InitializedModelDetail", 
                                    ["model_serial_number", 'model', 'param_grid_search', "model_name"])

# Represents the result of a grid search for a single model.
GridSearchedBestModel = namedtuple("GridSearchedBestModel",
                                 ["model_serial_number", "model", "best_model", "best_parameters", "best_score"])

# Represents the single best model founf after comparing all the models.
BestModel = namedtuple("BestModel",
                       ["model_serial_number", "model", "best_model", "best_parameters", "best_score"])



# This is the main class for picking the best model
class ModelBuilder:
    """ 
    This class is the core of the library. It reads a YAML configuration file
    to dynamically initialize, train, and tune ml-models.
    """
    
    def __init__(self, model_config_path: str):
        """ 
        Initializes the ModelBuilder with the path to the model configuration file.
        Args:
            model_config_path (str): The file path for the 'model_config.yaml' configuration.
        """
        try:
            logger.info("Initializing ModelBuilder...")
            self.config: dict = ModelBuilder.read_params(model_config_path)

            # Load grid search configuration
            self.grid_search_cv_module: str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name: str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data: dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])
            
            # Load model selection configuration
            self.models_initialisation_config: dict = dict[self.config[MODEL_SELECTION_KEY]]
            
            # These will be populated as we process the models
            self.initialised_model_list: List[InitializedModelDetail] = []
            self.grid_searched_best_model_list: List[GridSearchedBestModel] = []
            logger.info("ModelBuilder initialized successfully.")                    
        
        except Exception as e:
            logger.error(f"Error initializing ModelFactory: {e}")
            raise AydieException(e, sys) from e
        
    
    @staticmethod
    def read_params(config_path: str) -> dict:
        """
        Reads a YAML file and returns its content as a dictionary.

        Args:
            config_path (str): Path to the YAML file.

        Returns:
            dict: The configuration loaded from the YAML file.
        """
        
        try: 
            with open(config_path) as yaml_file:
                config = yaml.safe_load(yaml_file)
            logger.info(f"Configuration loaded from: {config_path}")
            return config
        
        except Exception as e:
            logger.error(f"Error initializing ModelFactory: {e}")
            raise AydieException(e, sys) from e
        
        
    @staticmethod
    def class_for_name(module_name: str, class_name: str):
        """
        Dynamically imports a class from a given module.
        This is how we can use strings from the config file
        to get actual Python classes.

        Args:
            module_name (str): The name of the module
            class_name (str): The name of the class
            
        Returns:
            The imported class reference.
        """
        try:
            module = importlib.import_module(module_name)
            class_ref = getattr(module, class_name)
            logger.info(f"Successfully imported class '{class_name}' from module '{module_name}'.")
            return class_ref
        except Exception as e:
            logger.error(f"Failed to import class '{class_name}' from module '{module_name}': {e}")
            raise AydieException(e, sys) from e
        
        
        
    @staticmethod
    def update_property_of_class(instance_ref, property_data: dict):
        """
        Sets attributes on a class instance based on a dictionary.
        This is used to set parameters for models and grid search.

        Args:
            instance_ref (_type_): The class instance to update.
            property_data (dict): A dictionary of properties to set.
        
        Returns:
            The updated class instace.
        """
        try:
            if not isinstance(property_data, dict):
                raise ValueError("property_data must be a dictionary.")
            for key, value in property_data.items():
                setattr(instance_ref, key, value)
            return instance_ref
        
        except Exception as e:
            raise AydieException(e, sys) from e
        
    
    
    def get_initialised_model_list(self) -> List[InitializedModelDetail]:
        """
        Initializes all models specified in the 'model_selection' section of the config file.

        Returns:
            List[InitializedModelDetail]: A list of initialized model details.
        """
        try:
            logger.info("Starting model initialization from configuration.")
            self.initialised_model_list = []
            for model_serial_number in self.models_initialisation_config.keys():
                model_config = self.models_initialisation_config[model_serial_number]
                logger.info(f"Initializing model with serial number: {model_serial_number}")
                
                model_obj_ref = ModelBuilder.class_for_name(
                    module_name = model_config[MODULE_KEY],
                    class_name = model_config[CLASS_KEY]
                )
                logger.info(f"Model class reference created for {model_config[CLASS_KEY]} from module {model_config[MODULE_KEY]}.")
                
                model = model_obj_ref()
                
                if PARAM_KEY in model_config:
                    model_property_data = dict(model_config[PARAM_KEY])
                    model = ModelBuilder.update_property_of_class(model, model_property_data)
                    logger.info(f"Set parameters for model {model_config[CLASS_KEY]}: {model_property_data}")
                    
                param_grid_search = model_config[SEARCH_PARAM_GRID_KEY]
                model_name = f"{model_config[MODULE_KEY]}.{model_config[CLASS_KEY]}"
                
                initialized_model_detail = InitializedModelDetail(
                    model_serial_number = model_serial_number,
                    model = model,
                    param_grid_search = param_grid_search,
                    model_name = model_name
                )
                self.initialised_model_list.append(initialized_model_detail)
                logger.info(f"Appended initialized model: {model_name} with serial number: {model_serial_number}")
                
            logger.info(f"Total models initialized: {len(self.initialised_model_list)}")
            return self.initialised_model_list
                
        except Exception as e:
            raise AydieException(e, sys) from e
        
        
    def execute_grid_search_operation(self, initialized_model: InitializedModelDetail, X, y) -> GridSearchedBestModel:
        """
        Executes the grid search for a single initialized model

        Args:
            initialized_model (InitializedModelDetail): The model details to run grid search on.
            X (_type_): Input training features
            y (_type_): Target variable

        Returns:
            GridSearchedBestModel: An object containing the best model, parameters, and score.
        """
        
        try:
            logger.info(f"Starting grid search for model serial number: {initialized_model.model_serial_number}")
            grid_search_cv_ref = ModelBuilder.class_for_name(
                module_name = self.grid_search_cv_module,
                class_name = self.grid_search_class_name
            )
            logger.info(f"Imported grid search class '{self.grid_search_class_name}' from module '{self.grid_search_cv_module}'.")
            
            grid_search_cv = grid_search_cv_ref(
                estimator = initialized_model.model,
                param_grid = initialized_model.param_grid_search
            )
            logger.info("Grid search object created successfully.")
            
            grid_search_cv = ModelBuilder.update_property_of_class(grid_search_cv, self.grid_search_property_data)
            logger.info(f"Grid search object updated with parameters: {self.grid_search_property_data}")
            
            # Model fitting
            logger.info("Fitting grid search model on training data.")
            grid_search_cv.fit(X, y)
            
            grid_search_best_model = GridSearchedBestModel(
                model_serial_number = initialized_model.model_serial_number,
                model = initialized_model.model,
                best_model = grid_search_cv.best_estimator_,
                best_parameters = grid_search_cv.best_params_,
                best_score = grid_search_cv.best_score_
            )
            logger.info(f"Grid search completed. Best parameters: {grid_search_cv.best_params_}, Best score: {grid_search_cv.best_score_}")
            logger.info(f"Returning best model for serial number: {initialized_model.model_serial_number}")
            return grid_search_best_model
            
        except Exception as e:
            raise AydieException(e, sys) from e
        
        
    def get_best_model(self, X, y, base_accuracy: float = BASE_ACCURACY) -> BestModel:
        """
        The main public method to run the entire pipeline:
        1. Initialize models.
        2. Run grid search for all models.
        3. Find and return the best model among them.

        Args:
            X : Input features for training.
            y : Target/output feature for training.
            base_accuracy (float, optional):  The minimum score a model must achieve to be considered the "best".

        Returns:
            BestModel: The best model that meets the base accuracy criteria.
        """
        
        try:
            logger.info("Starting the process to select the best model.")
            initialized_model_list = self.get_initialised_model_list()
            logger.info(f"Initialized {len(initialized_model_list)} models from configuration.")
            
            if not initialized_model_list:
                logger.warning("No models were initialized. Please check the model configuration file.")
                raise Exception("No models were initialised. Check your model configuration file, check for syntax or errors.")
            
            self.grid_searched_best_model_list = [
                self.execute_grid_search_operation(initialized_model, X, y)
                for initialized_model in initialized_model_list
            ]
            logger.info("Completed grid search for all initialized models.")
            logger.info("Selecting the best model from grid search results.")
            return ModelBuilder.get_best_model_from_list(self.grid_searched_best_model_list, base_accuracy)
            
        except Exception as e:
            raise AydieException(e, sys) from e
        
    
    
    def get_best_model_from_list(grid_searched_models: List[GridSearchedBestModel], base_accuracy: float = BASE_ACCURACY) -> BestModel:
        """
        Compares all the tuned models and returns the one with the highest score.


        Args:
            grid_searched_models (List[GridSearchedBestModel]): A list of models that have been through grid search.
            base_accuracy (float, optional): The minimum score required. Defaults to BASE_ACCURACY.

        Returns:
            BestModel: The single best model found.
        """
        
        try:
            logger.info("Comparing grid searched models to find the best one.")
            best_model = None
            for model in grid_searched_models:
                if model.best_score >= base_accuracy:
                    if best_model is None or model.best_score > best_model.best_score:
                        best_model = model
                        logger.info(f"New best model found with score: {model.best_score} and parameters: {model.best_parameters}")
                        
            if best_model is None:
                logger.warning(f"No model found with a score above the base accuracy of {base_accuracy}.")
                raise Exception(f"No model found with a base accuracy of at least {base_accuracy}")
            
            logger.info(f"Best model selected with score: {best_model.best_score}")
            return best_model
            
        except Exception as e:
            raise AydieException(e, sys) from e
        
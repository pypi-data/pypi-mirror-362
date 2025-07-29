import numpy as np
import pickle
import json
import uuid
from datetime import datetime
from random import getrandbits
from csa_common_lib.helpers._conversions import convert_ndarray_to_list
from csa_common_lib.helpers._os import is_valid_path, calc_crc64

class PredictionReceipt:
    """Saves and orgnaizes input dimensions, prediction durations, 
    timestamps, input options and more. This is meant to assist in
    the validation process of prediction results. 

    
    Returns
    -------
    PredictionReceipt
        Receipt class to store and persist information that is relavant
        to cross checking prediction requests

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the receipt dictionary.
    """

    def __init__(self, model_type, y, X, theta, options, yhat, prediction_duration=0):
        self.prediction_id = str(uuid.uuid4()) # Unique id for the prediction request
        self.timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Timestamp of the receipt
        self.prediction_duration = round(prediction_duration, 3) # Time to run a prediction (in seconds) 
        self.model_type = str(model_type) # Prediction model that was run
        self.X_dim = X.shape  # Save input dimensions
        self.y_dim = y.shape  # Save input dimensions
        self.theta_dim = theta.shape  # Save input dimensions
        self.options = convert_ndarray_to_list(options.options) # Save input options
        self.yhat = yhat # Save output info
        self.y_checksum = calc_crc64(pickle.dumps(y)) # convert y to bytes and get checksum
        self.X_checksum = calc_crc64(pickle.dumps(X)) # convert X to bytes and get checksum
        self.theta_checksum = calc_crc64(pickle.dumps(theta)) # convert theta to bytes and get checksum
        self.seed = getattr(options, '_seed', "A seed was not set") # The np.random seed cannot be accessed via os calls. Referencing options instead. 

    def display(self, detail:bool=False):
        """Displays basic validation info. Excludes lengthy results objects
        """        
        attributes = dir(self)
        
        # If suer does not request a detailed display(), remove input options and yhat array
        if detail is False:
            remove_attributes = ['options','yhat']
            attributes = [attr for attr in attributes if attr not in remove_attributes]

        # Print out a menu of accessible attributes in the receipt
        for attr in attributes:
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")
    

    def save_receipt(self, path:str='', file_name:str=None):
        """Saves prediction_receipts as .json file 
        """

        # Convert timestamp to filename if not supplied
        if file_name is None:
            file_name = self.timestamp.replace(" ", "_").replace(":", "-")

        # Validate that the user supplied a valid path before saving .json
        try:
            if path != '':
                is_valid_path(path)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")

        # Convert any nd.arrays to lists (to be json serializable)
        for attr in dir(self):
            attr_value = getattr(self, attr)
            if isinstance(attr_value, np.ndarray):
                setattr(self, attr, attr_value.tolist())
        
        
        # Turn receipt object into dictionary so that it can be saved as a json file
        obj_dict = self.__dict__

        # Save to a JSON file
        with open(f'{path}{file_name}.json', 'w') as json_file:
            json.dumps(obj_dict, json_file)
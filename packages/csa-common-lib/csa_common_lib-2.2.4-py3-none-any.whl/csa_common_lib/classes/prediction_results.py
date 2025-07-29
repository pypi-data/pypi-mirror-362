import numpy as np

class PredictionResults:
    """Stores an array of dictionaries containing prediction results
    and filters specific keys (output_details' attributes)
    into their respective arrays.

    Returns
    -------
    PredictionResults
        Flattened array of dictionaries by keys (output_details attributes)

    Raises
    ------
    TypeError
        If items in raw_data are not dictionaries.
    """    
    

    def __init__(self, results):
        if not results:
            raise ValueError("PredictionResults: Input data cannot be empty.")

        self.raw_data = results if isinstance(results, list) else [results]
        self._initialize_attributes()

        # compute weights concentration and add to class
        if hasattr(self, 'weights'):
            self.weights_concentration = [np.std(row) for row in self.weights]

        if hasattr(self,'status') and hasattr(self,'error'):
            self.yhat = None
            print("Warning: Some attributes are missing in the results. Tasks may have failed.")


    def _initialize_attributes(self):
        if not self.raw_data:
            return
        
        if isinstance(self.raw_data, dict):
            first_item = self.raw_data
            self.raw_data = [self.raw_data]
        else:
            first_item = self.raw_data[0]

        if not isinstance(first_item, dict):
            raise TypeError("PredictionResults: Items in raw_data must be dictionaries")
        
        # keys_to_populate = [key for key in first_item if key in allowed_keys]
        allowed_keys = list(self.raw_data[0].keys()) # Pull results keys that we want to capture

        for key in allowed_keys:
            values = []
            for item in self.raw_data:
                if key in item:
                    value = item[key]
                    if isinstance(value, np.ndarray) and value.shape == (1, 1):
                        value = value[0][0]
                    values.append(value)
            setattr(self, key, values)
            

    def attributes(self):
        """Display a list of accessible attributes of the class

        Returns
        -------
        list
            List of accessible attributes of the class.
        """        
        
        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        return attribute_list


    def display(self):
        """Display key-value pairs of all accessible attributes of the class.
        """        
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")


    def __repr__(self):
        """Displays a list of all accessible attributes in the class
        """
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key in self.raw_data[0].keys())
        return f"\nResults:\n--------- \n{attributes}\n--------- "
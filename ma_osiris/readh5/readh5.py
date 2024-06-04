import h5py
import os


def convert_h5_to_data(file_path):
    """
    Convert osiris h5 data to dictionary

    Args:
        file_path (_type_): The path of the h5 file
    """
    data_dict = {}

    def add_to_dict(name, obj):
        # Create an entry in the dictionary for the item, either dataset or group
        item_data = {'attributes': dict(obj.attrs)}
        if isinstance(obj, h5py.Dataset):
            # If it's a dataset, add the data
            item_data['data'] = obj[()]
        data_dict[name] = item_data
    with h5py.File(file_path, 'r') as file:
        file.visititems(add_to_dict)
    
    return data_dict

if __name__ == "__main__":
    file_path = '/Users/donglaima/Research/EER_simulation_mac/simulation_results/test1/MS/FLD/e1/e1-000001.h5'
    file_info = convert_h5_to_data(file_path)
    print(file_info['SIMULATION']['attributes']['DT'][0])
    print(file_info['AXIS/AXIS1']['data'][0])
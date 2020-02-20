import pickle
import numpy as np


class TrainingProgress:
    def __init__(self,
                 data_key_list=None,
                 data_dict=None,
                 meta_dict=None,
                 epoch_dict=None):
        self.data_dict = {} if data_dict is None else data_dict
        self.meta_dict = {} if meta_dict is None else meta_dict
        self.epoch_dict = {} if epoch_dict is None else epoch_dict
        if data_key_list is not None:
            for k in data_key_list:
                self.data_dict[k] = []

    def add_meta(self, new_dict):
        self.meta_dict.update(new_dict)

    def get_meta(self, key):
        try:
            return self.meta_dict[key]
        except KeyError:  # New key
            print('TP Error: Cannot find meta, key=', key)
            return None

    def record_data(self, new_dict, display=False):
        for k, v in new_dict.items():
            try:
                self.data_dict[k].append(v)
            except AttributeError:  # Append fail
                print('TP Error: Cannot Record data, key=', k)
            except KeyError:  # New key
                print('TP Warning: Add New Appendable data, key=', k)
                self.data_dict[k] = [v]
        if display:
            print('TP Record new data: ', new_dict)
        pass

    def record_epoch(self, epoch, prefix, new_dict, display=False):
        key = prefix + str(epoch)
        if key in self.epoch_dict.keys():
            self.epoch_dict[key].update(new_dict)
        else:
            self.epoch_dict[key] = new_dict
        if display:
            print(key, new_dict)

    def get_epoch_data(self, data_key, prefix, ep_start, ep_end, ep_step=1):
        data = []
        for ep in range(ep_start, ep_end, ep_step):
            key = prefix + str(ep)
            try:
                data.append(self.epoch_dict[key][data_key])
            except KeyError:
                print('TP Warning, Invalid epoch=', ep, ' Data Ignored!')
        return data


class ValueMeter:
    def __init__(self):
        self.data_dict = {}
        self.data_count = 0

    def record_data(self, dict, data_num=1):
        for k, v in dict.items():
            try:
                self.data_dict[k].append(v * data_num)
            except KeyError:
                self.data_dict[k] = [v * data_num]
        self.data_count += data_num

    def avg(self):
        result_dict = {}
        for k, v in self.data_dict.items():
            result_dict[k] = float(np.sum(v)) / self.data_count
        return result_dict

    def reset(self):
        self.data_dict = {}
        self.data_count = 0


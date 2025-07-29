#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eas_prediction.request import Request
from eas_prediction.request import Response
from eas_prediction.easyrec_predict_pb2 import PBRequest, PBResponse

class EasyRecRequest(Request):
    """
    Request for tensorflow services whose input data is in format of protobuf,
    privide methods to generate the required protobuf object, and serialze it to string
    """

    def __init__(self, signature_name=None, fg_mode="normal"):
        self.fg_mode = fg_mode
        self.request_data = PBRequest()
        self.signature_name = signature_name

    def __str__(self):
        return self.request_data

    def set_signature_name(self, singature_name):
        """
        Set the signature name of the model
        :param singature_name: signature name of the model
        """
        self.signature_name = singature_name

    def add_feed(self, data, debug_level=0):
        if isinstance(data, PBRequest):       
          self.request_data = data
        else:
          self.request_data.ParseFromString(data)
        self.request_data.debug_level = debug_level

    def add_user_fea_flt(self, k, v):
        self.request_data.user_features[k].float_feature = float(v)

    def add_user_fea_int(self, k, v):
        self.request_data.user_features[k].int_feature = int(v)

    def add_user_fea_str(self, k, v):
        self.request_data.user_features[k].string_feature = str(v)

    def set_faiss_neigh_num(self, neigh_num):
        self.request_data.faiss_neigh_num = neigh_num

    def keep_one_item_ids(self):
        item_id = self.request_data.item_ids[0]
        self.request_data.ClearField('item_ids')
        self.request_data.item_ids.extend([item_id])

    def to_string(self):
        """
        Serialize the request to string for transmission
        :return: the request data in format of string
        """
        return self.request_data.SerializeToString()

    def parse_response(self, response_data):
        """
        Parse the given response data in string format to the related TFResponse object
        :param response_data: the service response data in string format
        :return: the TFResponse object related the request
        """
        self.response = PBResponse()
        self.response.ParseFromString(response_data)
        return self.response


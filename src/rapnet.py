"""Rapnet SDK for Python3"""
import datetime
import requests
import json


class RapNetAPI:
    """API SDK for RapNet"""
    SHAPES = ["round", "pear", ""]
    COLORS = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    CLARITIES = ["IF", "VVS1", "VVS2", "VS1", "VS2",
                 "SI1", "SI2", "SI3", "I1", "I2", "I3"]

    BASE_URL = "https://technet.rapaport.com"
    AUTH_URL = "/HTTP/Authenticate.aspx"
    DLS_URL = "/HTTP/DLS/GetFile.aspx"
    UPLOAD_STRING_URL = "/HTTP/Upload/Upload.aspx?Method=string"
    UPLOAD_FILE_URL = "/HTTP/Upload/Upload.aspx?Method=file"
    PRICE_SHEET_URL = ":449/HTTP/JSON/Prices/GetPriceSheet.aspx"
    PRICE_CHANGES_URL = ":449/HTTP/JSON/Prices/GetPriceChanges.aspx"
    PRICE_SHEET_INFO_URL = ":449/HTTP/JSON/Prices/GetPriceSheetInfo.aspx"
    PRICE_URL = ":449/HTTP/JSON/Prices/GetPrice.aspx"
    ALL_DIAMONDS_URL = "/HTTP/JSON/RetailFeed/GetDiamonds.aspx"
    SINGLE_DIAMOND_URL = "/HTTP/JSON/RetailFeed/GetSingleDiamond.aspx"
    FORM_HEADER = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.timestamp = None

    def _get_token(self):
        """Get token Smartly."""
        if self.token is None or \
           self.timestamp is None or \
           (datetime.datetime.utcnow() - self.timestamp) > \
           datetime.timedelta(minutes=58):
            try:
                params = {
                    'username': self.username,
                    'password': self.password
                }
                response = requests.post(self.BASE_URL + self.AUTH_URL,
                                         data=params,
                                         headers=self.FORM_HEADER)

                if response.status_code == 200:
                    self.token = response.text
                    self.timestamp = datetime.datetime.utcnow()
                    return self.token
                else:
                    print("Can't get Token")
                    raise
            except:
                print("Can't get Token")
                raise
        else:
            return self.token

    def _auth(self, mode="BASIC"):
        if mode == "BASIC":
            return {
                    "username": self.username,
                    "password": self.password
                }
        elif mode == "TOKEN":
            return {'ticket': self._get_token}

    def _get_data(self, url, body={}, mode="BASIC",
                  header='self', raw=False, data={}, extras={}):
        if header == 'self':
            header = self.FORM_HEADER
        if mode == "BASIC":
            json_body, params = {
                "request": {
                    "header": self._auth(),
                    "body": body
                }
            }, {}
        elif mode == "TOKEN":
            json_body, params = {
                "request": {
                    "body": body
                }
            }, self._auth("TOKEN")

        params.update(data)
        response = requests.post(url,
                                 json=json_body,
                                 data=params,
                                 headers=header,
                                 **extras).text
        if raw:
            return response
        data = json.loads(response)["response"]
        if data["header"]["error_code"] == 0:
                return data["body"]
        elif data["header"]["error_code"] == 4001:
            return {}
        else:
            raise RuntimeWarning(
                "{}: {}".format(str(data["header"]["error_code"]),
                                data["header"]["error_message"])
            )

    def get_price_sheet_info(self):
        """Get Price sheet metadata"""
        return self._get_data(self.BASE_URL + self.PRICE_SHEET_INFO_URL)

    def get_price_sheet(self, shape="round"):
        """Get Price is by shape"""
        if shape in self.SHAPES:
            return self._get_data(self.BASE_URL + self.PRICE_SHEET_URL,
                                  body={"shape": shape})
        else:
            raise RuntimeWarning(
                "Invalid Shape Choose from {}.".format(", ".join(self.SHAPES))
            )

    def get_price_changes(self, shape="round"):
        """Get Price Changes is by shape"""
        if shape in self.SHAPES:
            return self._get_data(self.BASE_URL + self.PRICE_CHANGES_URL,
                                  body={"shape": shape})
        else:
            raise RuntimeWarning(
                "Invalid Shape Choose from {}.".format(", ".join(self.SHAPES))
            )

    def get_price(self, params={"shape": "round",
                                "size": 2.10,
                                "color": "E",
                                "clarity": "VS2"}):
        """Return a list of diamond pricing by filtering
        with params [JSON] (if provided else default).

        Keyword arguments:
        params -- filter paramters in json.

        For Further Information Consult:
        https://technet.rapaport.com/Info/Prices/Format_Json.aspx
        """
        search_params = params
        if "shape" not in search_params or \
           search_params["shape"] not in self.SHAPES:
            search_params["shape"] = "round"
        if "color" not in search_params or \
           search_params["color"] not in self.COLORS:
            search_params["color"] = "E"
        if "clarity" not in search_params or \
           search_params["clarity"] not in self.CLARITIES:
            search_params["clarity"] = "VS2"
        if "size" not in search_params:
            search_params["size"] = 2.10

        try:
            return self._get_data(self.BASE_URL + self.PRICE_URL,
                                  body=search_params)
        except:
            raise RuntimeWarning("Can't get data")

    def get_diamonds_list(self, params={"page_number": 1, "page_size": 20}):
        """Return a list of diamonds by filtering
        with params [JSON] (if provided else default).

        Keyword arguments:
        params -- filter paramters in json. An example:
        {
            "search_type": "White",
            "shapes": ["round","Princess","pear"],
            "size_from": 0.2,
            "size_to": 15.3,
            "color_from": "D",
            "color_to": "K",
            "clarity_from": "IF",
            "clarity_to": "VS2",
            "cut_from": "Excellent",
            "cut_to": "Fair",
            "polish_from": "Excellent",
            "polish_to": "Fair",
            "symmetry_from": "Excellent",
            "symmetry_to": "Fair",
            "price_total_from": 100,
            "price_total_to": 150000,
            "labs": ["GIA","IGI"],
            "table_percent_from": "26.0",
            "table_percent_to": "66.0",
            "eye_cleans": ["Yes", "Borderline"],
            "page_number": 1,
            "page_size": 20,
            "sort_by": "price",
            "sort_direction": "Asc"
        }

        For Further Information Consult:
        https://technet.rapaport.com/Info/RapLink/Format_Json.aspx
        """
        search_params = params
        if "page_number" not in search_params:
            search_params["page_number"] = 1
        if "page_size" not in search_params:
            search_params["page_size"] = 1

        try:
            return self._get_data(self.BASE_URL + self.ALL_DIAMONDS_URL,
                                  body=search_params)
        except:
            raise RuntimeWarning("Can't get data")

    def get_diamond(self, id):
        """Return a diamond by id."""
        if isinstance(id, int):
            try:
                return self._get_data(self.BASE_URL + self.SINGLE_DIAMOND_URL,
                                      body={"diamond_id": id})
            except:
                raise RuntimeWarning("Can't get data")
        else:
            raise RuntimeWarning("diamond_id must be a Integer")

    def get_all_diamonds(self, datafile=None):
        "Get all diamonds data from API"
        page1 = self.get_diamonds_list(params={"page_number": 1,
                                               "page_size": 50})
        data = page1['diamonds']
        total = page1["search_results"]["total_diamonds_found"]
        total_pages = (total // 50) - 0 if total % 50 > 0 else 1
        for page in range(2, total_pages+1):
            data.append(
                self.get_diamonds_list(params={"page_number": 1,
                                               "page_size": 50})['diamonds']
            )
        if datafile is None:
            return data
        else:
            with open(datafile, 'w') as d_file:
                json.dump(data, d_file)

    def get_dls(self, datafile=None):
        """Get Download Listing Service Data."""
        data = self._get_data(self.BASE_URL + self.DLS_URL,
                              mode="TOKEN",
                              raw=True)
        if datafile is not None:
            with open(datafile, 'w') as d_file:
                d_file.write(data)
        else:
            return data

    def upload_string(self, datastring):
        """Upload single diamond details in a string.
        For formatting details consult:
        https://technet.rapaport.com/Info/LotUpload/Upload_HTTP.aspx
        """
        return self._get_data(self.BASE_URL + self.UPLOAD_STRING_URL,
                              mode="TOKEN",
                              data={
                                  "UploadCSVString": datastring,
                                  "ReplaceAll": "false"
                              },
                              raw=True)

    def upload_csv(self, uploadfile):
        """Upload diamonds details in a csv file.
        For formatting details consult:
        https://technet.rapaport.com/Info/LotUpload/Upload_HTTP.aspx
        """
        return self._get_data(self.BASE_URL + self.UPLOAD_File_URL,
                              mode="TOKEN",
                              data={
                                  "ReplaceAll": "false"
                              },
                              raw=True,
                              extras={'files':{'file': open(uploadfile,
                                                            'rb')}})

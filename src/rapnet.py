"""Rapnet SDK for Python3"""
import datetime
import requests
import json


class RapNetAPI:
    """API SDK for RapNet"""

    BASE_URL = "https://technet.rapaport.com"
    AUTH_URL = "/HTTP/Authenticate.aspx"
    DATA_URL = "/HTTP/DLS/GetFile.aspx"
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
        self.cache = True
        self.cache_time = datetime.timedelta(days=1)
        self.all_diamonds_data = {}

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

    @staticmethod
    def _return_json(text):
        data = json.loads(text)["response"]
        print(data)
        if data["header"]["error_code"] == 0:
            return data["body"]
        else:
            print("{}: {}".format(str(data["header"]["error_code"]),
                                  data["header"]["error_message"]))
            raise

    def get_all_diamonds(self, params={"page_number": 1, "page_size": 20}):
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

        body = {
            "request": {
                "header": {
                    "username": self.username,
                    "password": self.password
                },
                "body": search_params
            }
        }

        try:
            response = requests.post(self.BASE_URL + self.ALL_DIAMONDS_URL,
                                     json=body,
                                     headers=self.FORM_HEADER,)

            return self._return_json(response.text)
        except:
            print("Can't get data")
            raise

    def get_diamond(self, id):
        """Return a diamond by id."""
        if isinstance(id, int):
            body = {
                "request": {
                    "header": {
                        "username": self.username,
                        "password": self.password
                    },
                    "body": {
                        "diamond_id": id
                    }
                }
            }

            try:
                response = requests.post(self.BASE_URL + self.SINGLE_DIAMOND_URL,
                                         json=body,
                                         headers=self.FORM_HEADER)

                return self._return_json(response.text)
            except:
                print("Can't get data")
                raise
        else:
            print("diamond_id must be a Integer")
            raise

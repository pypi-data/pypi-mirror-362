import os
import logging
import requests
import json
import time
import msgpack
import sys
from ls_cred_storage import LSCredStorage
from laser_mind_client_meta import MessageKeys


class LSAPIClient:

    USER_KEY = 'userToken'
    USER_ID_KEY = 'userId'
    TIMESTAMP_KEY = 'timestamp'
    ACCESS_TOKEN_KEY = 'accessToken'
    ID_TOKEN_KEY = 'IdToken'
    MAX_TOKEN_RETENTION_TIME_SECS = 3500

    SOLVER_REQUEST_HEADERS = {'accept' : 'application/octet-stream',
                              'content-type' : 'application/octet-stream',
                              'accept-encoding' : 'gzip, deflate, br'}

    SOLUTION_REQUEST_HEADERS = {
        'accept' : 'application/msgpack',
        'content-type' : 'application/msgpack',
        'accept-encoding' : 'gzip, deflate, br'
    }

    URL_REQUEST_HEADERS = {
        'accept' : 'application/msgpack',
        'content-type' : 'application/msgpack',
        'accept-encoding' : 'gzip, deflate, br'
    }

    def __init__(self, usertoken = None, printTiming = False, logLevel = logging.INFO, authEnabled = True, logToConsole = True):
        self.LS_API_RUN_URL = os.environ['LS_API_RUN_URL'] if 'LS_API_RUN_URL' in os.environ else 'http://solve.lightsolver.com/api/v2/commands/run'
        self.LS_API_RUN_SECURED_URL = os.environ['LS_API_RUN_SECURED_URL'] if 'LS_API_RUN_SECURED_URL' in os.environ else 'https://solve.lightsolver.com/api/v2/commands/run'
        self.LS_API_GET_PRESIGNED_URL = os.environ['LS_API_GET_PRESIGNED_URL'] if 'LS_API_GET_PRESIGNED_URL' in os.environ else 'https://solve.lightsolver.com/api/v2/getposturl'
        self.LS_AUTH_URL = os.environ['LS_AUTH_URL'] if 'LS_AUTH_URL' in os.environ else 'https://solve.lightsolver.com/authorize-solver-usage'
        self.LS_REQUEST_URL = os.environ['LS_REQUEST_URL'] if 'LS_REQUEST_URL' in os.environ else 'https://solve.lightsolver.com/api/v2/getsolution'

        # Define log format
        log_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
        # Get the root logger
        logger = logging.getLogger()
        logger.setLevel(logLevel)  # Set the logging level
        # Remove all existing handlers to prevent duplicates
        if logger.hasHandlers():
            logger.handlers.clear()
        # Add FileHandler (explicitly)
        file_handler = logging.FileHandler("laser-mind.log")
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)  # Logs will go to the file

        # Add StreamHandler (console logging) if enabled
        if logToConsole:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_formatter)
            logger.addHandler(console_handler)  # Logs will go to stdout

        self.printTiming = printTiming
        self.authEnabled = authEnabled
        if authEnabled:
            if usertoken == None :
                raise ValueError("You must input a usertoken when authREnabled = True")
            self.usertoken = usertoken
            self.credStorage = LSCredStorage()
            token_dic = self.check_and_get_persisted_tokens() #TODO @markin is this duplication with check_is_token_valid() in refresh_tokens_if_needed?

            if token_dic == None:
                self.refresh_tokens_if_needed()
                logging.info('Got new access token')
            logging.info('LSAPIClient created,connection is authenticated and authorized')
        else:
            logging.info('LSAPIClient created, authentication disabled')

    def msgpack_encode(self, x):
        v = msgpack.packb(x)
        return v

    def msgpack_decode(self, x):
        try:
            v = msgpack.unpackb(x)
        except Exception as e:
            return None
        return v

    def refresh_tokens_if_needed(self):
        if self.authEnabled and not self.check_is_token_valid():
            newTokenDic = self.GetTokensFromServer()
            logging.info(f'got tokens for usertoken {self.usertoken}')
            self.credStorage.store_token(self.usertoken, newTokenDic)

    def GetTokensFromServer(self):
        data = {
            'userToken' : f'{self.usertoken}'
        }

        headers = {
            'accept' : 'application/json',
            'content-type' : 'application/json',
            }
        req = requests.post(self.LS_AUTH_URL, headers=headers, data=json.dumps(data))
        req.raise_for_status()
        token = req.json()
        token_dic  = self.create_token_data_for_user(token)
        return token_dic

    def create_token_data_for_user(self, token):
        dic = {
            self.TIMESTAMP_KEY : time.time(),
            self.USER_KEY : self.usertoken,
            self.USER_ID_KEY : token[self.USER_ID_KEY],
            self.ACCESS_TOKEN_KEY : token[self.ACCESS_TOKEN_KEY],
            self.ID_TOKEN_KEY : token[self.ID_TOKEN_KEY]
        }
        return dic

    def check_and_get_persisted_tokens(self):
        storedToken = self.credStorage.get_stored_token(self.usertoken)
        if storedToken != None:
            if self.check_is_token_valid():
                return storedToken
        return None

    def check_is_token_valid(self):
        if self.credStorage.currentTokenDic is not None:
            return time.time() - self.credStorage.currentTokenDic[self.TIMESTAMP_KEY] < self.MAX_TOKEN_RETENTION_TIME_SECS
        return False

    def MakeDataForSolveRequest(self, commandName, param):
        data = {
            'name' : commandName,
            'param' : param,
            'creationTime' : time.time()
        }
        if self.authEnabled:
            data['userToken'] = self.credStorage.currentTokenDic[self.USER_KEY]
            data['userId'] = self.credStorage.currentTokenDic[self.USER_ID_KEY]
            data['accessToken'] = self.credStorage.currentTokenDic[self.ACCESS_TOKEN_KEY]
            data['IdToken'] = self.credStorage.currentTokenDic[self.ID_TOKEN_KEY]

        return self.msgpack_encode(data)

    def MakeDataForUploadRequest(self, toUpload):
        data = {
            'param' : toUpload,
            'creationTime' : time.time()
        }
        if self.authEnabled:
            data['userToken'] = self.credStorage.currentTokenDic[self.USER_KEY]
            data['userId'] = self.credStorage.currentTokenDic[self.USER_ID_KEY]
            data['accessToken'] = self.credStorage.currentTokenDic[self.ACCESS_TOKEN_KEY]
            data['IdToken'] = self.credStorage.currentTokenDic[self.ID_TOKEN_KEY]
        return self.msgpack_encode(data)

    def MakeDataForResultRequest(self, solutionId):
        data = {
            'solId' : solutionId,
            'creationTime' : time.time(),
            'userId' : 0
        }
        if self.authEnabled:
            data['userToken'] = self.credStorage.currentTokenDic[self.USER_KEY]
            data['userId'] = self.credStorage.currentTokenDic[self.USER_ID_KEY]
            data['accessToken'] = self.credStorage.currentTokenDic[self.ACCESS_TOKEN_KEY]
            data['IdToken'] = self.credStorage.currentTokenDic[self.ID_TOKEN_KEY]
        return self.msgpack_encode(data)

    def MakeDataForGetURLRequest(self, inputPath = None):
        data = {
            'creationTime' : time.time()
        }

        if self.authEnabled:
            data['userId'] = self.credStorage.currentTokenDic[self.USER_ID_KEY]
            data['accessToken'] = self.credStorage.currentTokenDic[self.ACCESS_TOKEN_KEY]
            data['IdToken'] = self.credStorage.currentTokenDic[self.ID_TOKEN_KEY]

        if inputPath != None:
            data[MessageKeys.QUBO_INPUT_PATH] = inputPath

        return self.msgpack_encode(data)

    def ValidateResponse(self, response):
        if MessageKeys.ERROR_KEY in response:
            raise Exception(response[MessageKeys.ERROR_KEY])
        return True

    def SendCommandRequest(self, commandName, input, secured = True):
        if self.authEnabled:
            if not self.credStorage.is_cached_user(self.usertoken):
                raise SystemError("usertoken doesn't match stored access token, please reconnect LightSolver service")
            self.refresh_tokens_if_needed()
        if self.printTiming:
            startTime = time.time()
        data = self.MakeDataForSolveRequest(commandName, input)
        headers = self.SOLVER_REQUEST_HEADERS
        req_url = self.LS_API_RUN_SECURED_URL if secured else self.LS_API_RUN_URL
        response = requests.post(url = req_url, headers = headers, data = data)
        response.raise_for_status()
        dicResponse = self.msgpack_decode(response._content)
        self.ValidateResponse(dicResponse)
        if self.printTiming:
            totalTime = time.time() - startTime
        return dicResponse

    def SendResultRequest(self, solutionId, timestamp):
        self.refresh_tokens_if_needed()
        id_str = f'{solutionId}_{timestamp}'
        logging.info(f"getting {id_str}")
        if self.printTiming:
            startTime = time.time()
        data = self.MakeDataForResultRequest(id_str)
        headers = self.SOLUTION_REQUEST_HEADERS
        req_url = self.LS_REQUEST_URL
        response = requests.post(url = req_url, headers = headers, data = data)
        if self.printTiming:
            totalTime = time.time() - startTime
        if response.status_code == 404:
            decoded_str = response._content.decode('utf-8').strip()
            if not decoded_str:
                return None
            if decoded_str != 'Not Found':
                try:
                    dicResponse =  json.loads(decoded_str)
                    if  isinstance(dicResponse, dict) and "error" in dicResponse :
                        logging.info(f"Status: {dicResponse['error']}")
                except json.JSONDecodeError as e:
                    return None
                except Exception as ex:
                    return None
            return None

        response.raise_for_status()
        dicResponse = self.msgpack_decode(response._content)

        if not isinstance(dicResponse, dict):
            raise Exception("response is not a dictionary!")
        if MessageKeys.ERROR_KEY in dicResponse:
            raise Exception(dicResponse[MessageKeys.ERROR_KEY])
        if MessageKeys.WARNING_KEY in dicResponse:
            logging.warning(f"Warning: solver encountered \"{dicResponse[MessageKeys.WARNING_KEY]}\"")
        return dicResponse

    def SendGetURLRequest(self, urlPath = None):
        self.refresh_tokens_if_needed()
        logging.info(f"getting url")
        if self.printTiming:
            startTime = time.time()
        data = self.MakeDataForGetURLRequest(urlPath)
        headers = self.URL_REQUEST_HEADERS
        req_url = self.LS_API_GET_PRESIGNED_URL
        response = requests.post(url = req_url, headers = headers, data = data)
        if self.printTiming:
            totalTime = time.time() - startTime
            print(f"{totalTime=}")
        if response.status_code == 404:
            return None
        response.raise_for_status()

        return self.msgpack_decode(response._content)

    def SendUploadRequest(self, toUpload, url):
        payload = self.MakeDataForUploadRequest(toUpload)
        response = requests.put(url, data=payload)
        response.raise_for_status()

    def upload_command_input(self, data, inputPath = None):
        urlResponse = self.SendGetURLRequest(inputPath)
        self.SendUploadRequest(data, urlResponse['url'])
        return urlResponse['reqId']

from easy_utils_dev.debugger import DEBUGGER
import requests , json , subprocess
from requests.auth import HTTPBasicAuth as BAuth    
from .utils import pingAddress , fixTupleForSql , start_thread
from time import sleep
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from threading import Thread
from easy_utils_dev.Events import EventEmitter
from .EasySsh import CREATESSH
import traceback
import xmltodict
from .FastQueue import FastQueue


class WSNOCLIB : 
    def __init__( self, 
                ip , 
                username , 
                password ,
                debug_level='info', 
                debug_name='wsnoclib' ,
                debug_homepath='./debug/',
                request_max_count=30,
            ): 
        self.logger = DEBUGGER(f'{debug_name}-{ip}',level=debug_level,homePath=debug_homepath)
        self.disabledWarnings = self.disableUrlWarnings()
        self.event = EventEmitter(id=ip)
        self.address = ip
        self.username = username
        self.password = password
        self.baseUrl = self.createBaseUrl()
        self.session = requests.Session()
        self.numberOfRequests=0
        self.request_max_count = request_max_count
        self.onGoingRequests=0
        self.kafka = False
        self.fastQueue = FastQueue(request_max_count)
        self.queue = []
        self.tokenRefreshPeriod = 2700
        self.final_results = []
        self.killed=False
        self.nes=[]
        self.loggedOut = False
        self.alarms_store=[]

    def getLogger(self) : 
        return self.logger

    def supress_logs(self) :
        self.logger.disable_print()
    
    def change_token_refresh_period(self , period=2700) :
        '''
        period is in seconds.
        '''
        self.tokenRefreshPeriod = int(period)

    def createBaseUrl(self) :
        self.baseUrl = f'https://{self.address}'
        return self.baseUrl

    def change_debug_level(self , level) :
        self.logger.warning("This function -change_debug_level- is deprecated and will be removed. please use set_debug_level instead")
        if not level in ['info' , 'error' , 'debug' , 'warn'] :
            raise Exception(f"Not valid debugging level: {level}. Levels {['info' , 'error' , 'debug' , 'warn']}")
        self.logger.set_level(level)
    
    def set_debug_level(self , level) :
        if not level in ['info' , 'error' , 'debug' , 'warn'] :
            raise Exception(f"Not valid debugging level: {level}. Levels {['info' , 'error' , 'debug' , 'warn']}")
        self.logger.set_level(level)

    def disableUrlWarnings(self) :
        disable_warnings(InsecureRequestWarning)
        return True

    def getSession(self) :
        return self.session

    def connect(self,auto_refresh_token=True) :
        self.auto_refresh_token = auto_refresh_token 
        #refresh the session
        self.logger.debug(f"loggedOut flag is {self.loggedOut}")
        if self.loggedOut :
            return
        if not pingAddress(self.address) :
            raise Exception(f'Address {self.address} is not pingable.')
        self.logger.info(f'Connecting to {self.address} using username: {self.username} BAuth={BAuth(self.username, self.password)}')
        self.logger.debug(f'Connecting to {self.address} using username: {self.username}')
        URL = f"https://{self.address}/rest-gateway/rest/api/v1/auth/token"
        self.logger.debug(f'Login URL is {URL}')
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "grant_type": "client_credentials"
        }
        r = requests.post(url = URL , headers=headers , auth=BAuth(self.username, self.password), verify=False, json=data)
        self.logger.debug(f"""
            response_header={r.headers}
            response_encoding={r.encoding}
            response_reason={r.reason}
            body={r.request.body}
            headers={r.request.headers}
            URL={URL}
            content={r.text}
        """)
        self.logger.info(f'Request return status code : {r.status_code}')
        self.logger.debug(f"Login Request response body is {r.text}")
        if r.status_code != 200 :
            self.logger.debug(f'fail message {r.text}')
            raise Exception(f'Failed to authenticate WSNOC. Return status code : {r.status_code}')
        self.access_token = r.json()["access_token"]
        self.refresh_token = r.json()["refresh_token"]
        self.bearer_token = f'Bearer {self.access_token}'
        self.token = r.json()
        self.token.update({'bearer_token' :  self.bearer_token })
        if auto_refresh_token :
            self.autoRefreshThread = start_thread(target=self.runAutoRefreshThread)
        self.logger.debug(f'token => {r.text}')
        return self.token


    def getLatestToken(self) :
        return self.token


    def logout(self,logout=True) :
        self.logger.info(f"Logging out from {self.address} ...")
        body = f"token={self.access_token}&token_type_hint=token"
        self.logger.debug(f"logout body={body}")
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        self.logger.debug(f"logout header={header} address={self.address}")
        URL = f"https://{self.address}/rest-gateway/rest/api/v1/auth/revocation"
        self.logger.debug(f'Logout URL {URL}')
        r = requests.post(
            url = URL ,
            auth=BAuth(self.username, self.password),
            verify=False,
            data=body,
            headers=header
        )
        self.logger.info(f"Logging out from '{self.address}' response.code={r.status_code}")
        self.logger.debug(f"Logout response is {r.text}")
        if r.status_code != 200 :
            self.logger.debug(f'fail message is {r.text}')
            self.logger.error(f"Failed logging out from {self.address}")
        self.numberOfRequests = 0
        if logout :
            self.loggedOut = True
        self.logger.debug("logout function completed. return TRUE exit status")
        try :
            r.close()
        except :
            pass
        return True

    def runAutoRefreshThread(self) : 
        self.logger.info(f'Waiting for auto refresh in {self.tokenRefreshPeriod}sec...')
        sleep(self.tokenRefreshPeriod)
        self.logger.info(f"Waiting period completed. Starting Revoking/Login process ...")
        self.logout(logout=False)
        sleep(10)
        self.logger.info(f"Logout process completed. Starting Reconnecting ...")
        self.connect(self.auto_refresh_token)


    def kafka_connect( self , 
            user , 
            password, 
            auto_refresh=True ,
            severities=[], 
            nodeNames=[] , 
            nodeIps=[] , 
            affectedObjects=[] , 
            alarms=[] , 
            kafka_port=8443, 
            ssh_port=22 , 
            custom_filter_expression=None
        ): 
        '''
        possible serverities ['major','minor', 'critical' , 'warning' , 'cleared' , 'indeterminate']
        possible affectedObjects ["TRAIL","ASONTRAIL","service.Service","PHYSICALCONNECTION","NetworkElement"]
        custom_filter_expression example : AND neName in (nes) OR possibleCause = 'card-missing'
        {
            "alarms": [akjsd,asdmkasdm,asdjiasdi],  
            "severities": [],
            "affectedObjectTypes": [],
        }
 
        '''
        self.logger.info('requesting kafka subscription ...')
        if self.loggedOut or self.killed:
            self.logger.error(f"WSNOC API Authentication process loggedout or killed. exit")
            raise Exception('WSNOC API Authentication process loggedout or killed. exit')
        self.kafka_port = kafka_port
        self.ssh = CREATESSH(
            address=self.address,
            user=user,
            password=password,
            sshPort=ssh_port
        )
        self.sshclient = self.ssh.init_shell()
        self.channel = self.ssh.init_ch()
        if len(severities) == 0 :
            severities = ['major','minor', 'critical' , 'warning' , 'cleared' , 'indeterminate']
        filter = f"severity in {fixTupleForSql(severities)}"
        self.logger.debug(f'severity filter is  "{filter}"')
        # for index, alarm in enumerate(alarms) : 
        #     self.logger.debug(f'adding filter on alarmName={alarm} for index {index}')
        #     if index == 0 :
        #         filter += f" AND ( alarmName like '{alarm}' )"
        #     else :
        #         filter += f" OR ( alarmName like '{alarm}' )"
        if len(alarms) > 0 :
            filter += f" AND ( alarmName in {fixTupleForSql(alarms)} )"
            self.logger.debug(f'filter updated with "{filter}"')
            
        if len(nodeNames) > 0 :
            neArray = self.get_nes()
            for ne in neArray :
                if ne['tid'] in nodeNames :
                    nodeIps.append(ne['ipAddress'])
        if len(nodeIps) > 0 :
            filter += f" AND neId in {fixTupleForSql(nodeIps)}"
            self.logger.debug(f'nodeIpFilter : filter updated with "{filter}"')
        if len(affectedObjects) > 0 :
            filter += f" AND affectedObjectTypes in {fixTupleForSql(affectedObjects)}" 
            self.logger.debug(f'affectedObjectType Filter : filter updated with "{filter}"')
        if custom_filter_expression :
            filter += f" {custom_filter_expression}"
        URL = '/nbi-notification/api/v1/notifications/subscriptions'
        kafkaForm = {
                "categories": [
                    {
                    "name": "NSP-FAULT",
                    "propertyFilter": filter
                    }
                ]
        }
        self.logger.debug(f"Kafka Filter Form : {kafkaForm}")
        response = self.post(
            url=URL,
            return_json=True,
            port=self.kafka_port,
            body=json.dumps(kafkaForm)
            )
        if response :
            self.kafka={}
            self.kafka['subscriptionId'] = response['response']['data']['subscriptionId']
            self.kafka['response'] = response
            self.kafka['topicId'] =response['response']['data']['topicId']
        if auto_refresh :
            start_thread(target=self.renewSubscription)
        self.killed=False
        return response or {}


    def renewSubscription(self) :
        while True :
            try :
                sleep(3000) 
                if self.loggedOut or self.killed:
                    break
                self.logger.info('Renewing subscription ...')
                URL = f"/nbi-notification/api/v1/notifications/subscriptions/{self.kafka.get('subscriptionId')}/renewals"
                self.post(
                    url=URL,
                    return_json=True,
                    port=self.kafka_port,
                )
                self.logger.info('Renewing subscription completed successfully. sleep 50 minutes.')
            except Exception as error :
                self.logger.error(f'failed to renew subscription. {error}')
                self.logger.debug(traceback.format_exc())

    def deleteKafkaSubscription(self , subscriptionId=None) :
        # /nbi-notification/api/v1/notifications/subscriptions/{{subscriptionID}}
        if not subscriptionId :
            subscriptionId=self.kafka.get('subscriptionId')
            
        self.logger.info('Deleting subscription')
        URL = f"/nbi-notification/api/v1/notifications/subscriptions/{subscriptionId}"
        self.delete(
            url=URL,
            return_json=True,
            port=self.kafka_port,
        )
        self.killed=True
        return True
    
    def handle_beautify_alarm(self , alarm ) :
        oalarm = alarm
        alarm = alarm['data']['ietf-restconf:notification']
        if 'create' in str(list(alarm.keys())) :
            alarmData = alarm['nsp-fault:alarm-create']
            oalarm['dataEnh'] = {
                'newAlarm' : True,
                'alarmChange' : False,
                'alarmId' : int(alarmData['objectId'].split(':')[-1]),
                'neId' : alarmData['neId'],
                'neName	' : alarmData['neName'],
                'alarmName' : alarmData['alarmName'],
                'cleared' : False,
                'aknowledged' : False,
                **alarmData , 
            }
        elif 'change' in str(list(alarm.keys())) :
            alarmData = alarm['nsp-fault:alarm-change']
            cleared = False
            aknowledged = False
            if 'severity' in list(alarmData.keys()) :
                if alarmData['severity']['new-value'] == 'cleared' :
                    cleared = True
            if 'acknowledged' in list(alarmData.keys()) :
                    aknowledged = alarmData['acknowledged']['new-value']
            oalarm['dataEnh'] = {
                'newAlarm' : False,
                'alarmChange' : True,
                'alarmId' : int(alarmData['objectId'].split(':')[-1]),
                'cleared' : cleared,
                'aknowledged' : aknowledged,
                **alarmData ,
            }
        return oalarm


    def kafka_listen(self,new_kafka_release=False,beautify=False) :  
        self.logger.info('Listening to Kafka Notifications ...')
        if not self.kafka :
            self.logger.error(f'kafka is not established. exit.')
            return False
        if not new_kafka_release :
            cmd=f"docker exec nspos ./opt/nsp/os/kafka/bin/kafka-console-consumer.sh --bootstrap-server nspos:9193 --topic {self.kafka.get('topicId')} --consumer.config /opt/nsp/os/kafka/config/consumer.properties"
        elif new_kafka_release:
            cmd=f"docker exec nspos-kafka unset JMX_PORT && /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server nspos-kafka:9193 --topic {self.kafka.get('topicId')} --consumer.config /opt/bitnami/kafka/config/consumer.properties"
        self.logger.debug(f'Kafka Listen is using {cmd}')
        self.channel.sendall(cmd+'\n')
        while True :
            sleep(.1)
            if self.killed :
                raise Exception("Kafka is already killed.")
            lines = self.channel.recv(4096).decode().strip().splitlines()
            self.logger.debug(f'Received message in kafka : {lines}')
            for line in lines :
                self.logger.debug(f"parsing line '{line}'")
                if 'eventTime' in str(line):
                    try :
                        if beautify :
                            line = json.loads(line)
                            line = self.handle_beautify_alarm(line)
                            self.alarms_store.append(line)
                            yield line
                        yield line
                    except Exception as error:
                        if beautify :
                            self.logger.error(f'failed to json.loads kafka alarm. maybe incomplete. check debug logs.')
                            self.logger.debug(f'failed to json.loads kafka alarm. alarm={line} error={error} traceback={traceback.format_exc()}' )
                        else :
                            self.logger.error(f'failed to json.loads kafka alarm {line} error={error}')
                        yield line


    def get(self, url , headers={} , port=8443 , return_json=True ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [GET] : {url}')
        headers={ 'Authorization' : self.bearer_token }
        r = requests.get(url , headers=headers , verify=False )
        self.logger.info(f'request [GET] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [GET]: {url} status code: [{r.status_code}]')
        if return_json :
            return r.json()
        return r

    def post(self, url , port=8443 , body={} , headers={} , return_json=False , contentType=f'application/json' ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [POST] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
            }
        if body : 
            _headers['Content-Type'] = contentType
        headers.update(_headers)
        r = requests.post( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [POST] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [POST]: {url} status code: [{r.status_code}]')
            return False
        if return_json :
            return r.json()
        return r
    
    def update(self, url , port=8443 , body={} , headers={} , return_json=False , contentType=f'application/json' ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [UPDATE] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
            }
        if body : 
            _headers['Content-Type'] = contentType
        headers.update(_headers)
        r = requests.update( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [UPDATE] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [UPDATE]: {url} status code: [{r.status_code}]')
            return False
        if return_json :
            return r.json()
        return r
    

    def delete(self, url , port=8443 , body={} , headers={} , return_json=False ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [DELETE] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
            }
        if body : 
            _headers['Content-Type'] = 'application/json'
        headers.update(_headers)
        r = requests.delete( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [DELETE] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [DELETE]: {url} status code: [{r.status_code}]')
            return False
        if return_json :
            return r.json()
        return r

    def session_info(self) :
        self.logger.debug('Getting Version ...')
        response = self.get( url='/oms1350/data/common/sessionInfo')
        return response

    def get_nodes(self) :
        self.logger.debug(f"Requesting Nodes ..")
        response = self.get( url="/oms1350/data/npr/nodes" )
        return response

    def get_nes(self) :
        self.logger.debug(f"Requesting Network Elements ..")
        response = self.get( url="/oms1350/data/npr/nes")
        return response

    def get_version(self) :
        self.logger.debug(f"Getting Version ...")
        response = self.get('/oms1350/data/otn/system/getVersion')
        return response

    def fullSync(self , nodeId, nodeName ) :
        self.logger.debug(f'Trigger Full Sync for node %s' % nodeId)
        url = f'/oms1350/data/npr/nodes/{nodeId}'
        headers={"Content-Type" : "application/json" , "Accept" : "application/json" }
        body= json.dumps({"Tag":"F_POP_neFullSyncro","userLabel": nodeName })
        response=self.post( url=url , body=body , headers=headers ,return_json=False )
        return response.json()

    def getUserRecords(self) :
        self.logger.debug("Trigger GET request for user records ...")
        url = f'/oms1350/data/npr/AdminCommandLogs'
        headers={"Content-Type" : "application/json" , "Accept" : "application/json" }
        response=self.get( url=url , headers=headers ,return_json=False )
        if response :
            return response.json()

    def cliCutThough(self , neName , command) : 
        if len(self.nes) == 0:
            self.nes = self.get_nes()
        emlDomId=None
        emlNeId=None
        for elem in self.nes :
            if elem['guiLabel'] == neName :
                emlDomId= elem['emlDomId']
                emlNeId= elem['emlNeId']
        if not emlDomId or not emlNeId :
            self.logger.error(f'Error: Cannot find network element {neName}')
            return False
        URL = f'/oms1350/eqm/cliRequest/processCLIRequest/{emlDomId}/{emlNeId}'
        payload = f"<CLIRequestCommand><neName>{neName}</neName><ncName>{emlDomId}_SNA</ncName><cliCommandText>{command}</cliCommandText></CLIRequestCommand>"
        response = self.post(URL ,body=payload ,contentType='application/xml')
        if response.status_code in [200,201] :
            parsed_xml = xmltodict.parse(response.text)
            return parsed_xml

    def getBackupJobs(self) :
        URL = '/oms1350/data/plat/jobs'
        return self.get(URL)
    
    def getAllConnections(self) :
        '''
        get trails and services in one array.
        '''
        URL = '/oms1350/data/otn/connections/trails'
        trails = self.get(URL).get('items' , [])
        URL = '/oms1350/data/otn/connections/paths'
        paths = self.get(URL).get('items' , [])
        return trails + paths
    
    def getSystemLicense(self) :
        self.logger.info(f'get license ...')
        return self.get('/systemmonitor/sysadmin/stats/licenseinfo/v2')

    def getUnscheduledNetworkElementsBackup(self) :
        URL = "/oms1350/data/swim/NeScheduledBckpData"
        return self.get(URL).get('items' , [])
    
    def getAlarms(self) :
        URL= "/FaultManagement/rest/api/v2/alarms/details"
        return self.get(URL,port=8544)
    
    def getSessionInfo(self) :
        URL = "/oms1350/data/common/sessionInfo"
        return self.get(URL)

if __name__ == '__main__' :
    # noc = WSNOCLIB('10.20.30.55' , 'admin' , 'Nokia@2024') 
    # noc.connect(auto_refresh_token=True)
# #     records= noc.getUserRecords()
# #     open( './w.json' , 'w').write(json.dumps(records))
# #     noc.logout()

#     # ========================================================== kafka
#     # noc = WSNOCLIB('151.98.30.91' , 'admin' , 'Nokia1.!') 
#     # noc.connect(auto_refresh_token=False)
#     # response = noc.cliCutThough( 'LRVMP_AAN6001-AD' , 'show xc *')
#     # print(response)
#     # test = noc.kafka_connect(
#     #     user='root',
#     #     password='Nokia@2023' ,
#     #     # nodeIps=['10.198.34.3'] ,
#     #     severities=['minor' , 'critical' , 'major' , 'warning'] ,
#     #     alarms=['Card missing' , 'Loss of Signal'] ,
#     #     nodeNames=["RVMP_AUH2920-1"]
#     # )
#     alarms = noc.kafka_listen()
#     # # this will keep listening for alarms , since kafka_listen is yielding not returning ...
#     for alarm in alarms: 
#         print(alarm)

#     # noc.logout()
    pass

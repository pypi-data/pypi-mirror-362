from agora_redis_client import redis as Redis
from agora_logging import logger
from agora_config import config
from .twin_property_observer import TwinPropertyObserver
from enum import Enum

class RedisPattern(Enum):
    DESIRED = "desired"
    REPORTED = "reported" 

class TwinPropertySingleton: 
    _instance = None

    def __init__(self) -> None:
        super().__init__()
        self.pubsub = Redis.pubsub()
        self.__sleep_time = 0.01
        self.observer_callbacks = {}    
        self.__twin_property_running = 0
 
            
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance     
    
    def _initialize_redis_sub(self):
        try:
            if not Redis.is_connected():
                Redis.connect()
            self.pubsub = Redis.pubsub()
            
        except Exception as error:
            logger.exception(error, "Exception occured while Redis subscription...")
            raise error
            

    def observe(self, app_callback: callable, tp_group_id: str, property_name :str = None) -> None:    
        """
        Create Observable and add to list and start the subscription to the pattern
        """    
        if self.pubsub is None: self._initialize_redis_sub()
        if tp_group_id is None: raise ValueError("tp_group_id cannot be None")
        if not callable(app_callback): raise TypeError("app_callback is not callable method")
        if tp_group_id not in self.observer_callbacks:
            observer = TwinPropertyObserver(tp_group_id,property_name)
            observer.attach(app_callback)
            self.__add_observer(observer,None)    
        else:
            callbacks = self.observer_callbacks[tp_group_id]
            if property_name not in callbacks:
                observer = TwinPropertyObserver(tp_group_id,property_name)
                observer.attach(app_callback)
                self.__add_observer(observer,callbacks)
            else:
                logger.warn(f"Duplicate request for subscription to same group{tp_group_id} and property {property_name}")

    def stop_observe(self, tp_group_id: str, property_name :str = None) -> None:        
        
        if tp_group_id is None: raise ValueError("tp_group_id cannot be None")
        if property_name is None: property_name = "*"
        if tp_group_id in self.observer_callbacks and property_name in self.observer_callbacks[tp_group_id]:
            self.__remove_observer(tp_group_id,property_name)                
        else:
            logger.info(f"No Observer found for the group {tp_group_id}, property{property_name}")
                
    def __add_observer(self, observer: TwinPropertyObserver, callbacks:dict=None):
        """
        Add Observable to dictionary and start subscription
        """
        if callbacks is None: 
            callbacks = {}
        callbacks[observer.property_name] = observer
        self.observer_callbacks[observer.tp_id] = callbacks
        self.__subscribe_patterns(observer)
      
    def __remove_observer(self, tp_group_id:str,property_name:str = None):
        """
        Remove Observable from dictionary and stop subscription
        """        
        observer = self.observer_callbacks[tp_group_id][property_name]
        self.__unsubscribe_patterns(observer)        
        del self.observer_callbacks[tp_group_id][property_name]
        
        
    def __subscribe_patterns(self, observer:TwinPropertyObserver):
        """
        Subscribe to pattern in Redis
        """
        try:          
            if self.pubsub is None:  
                logger.warn("No Redis subscription initialized")   
            self.pubsub.psubscribe(**{"__key*__:"+ observer.pattern : observer.subscription_callback})
            if not self.__twin_property_running :
                self.pubsub.run_in_thread(sleep_time=float(self.__sleep_time))
                self.__twin_property_running = 1
            logger.info("Running : {0} redis event subscriber ...".format(observer.pattern))
        except Exception as error:
            logger.exception(error, "Error while suscribing to pattern {0} ".format(observer.pattern))

    def __unsubscribe_patterns(self, observer:TwinPropertyObserver):
        """
        Unsubscribe pattern in Redis
        """
        try:  
            if self.pubsub is None:  
                logger.warn("No Redis subscription initialized")           
            self.pubsub.punsubscribe("__key*__:"+ observer.pattern ) 
            logger.info(" {0} twin property unsubscribe ...".format(observer.pattern))
        except Exception as error:
            logger.exception(error, "Error while unsubscriber to pattern {0} ".format(observer.pattern))
    
    @staticmethod
    def set_reported_property( prop_name:str, prop_value:any, tp_group_id):
        """
        Set reported property in Redis key 'set twin_properties/{tp_group_id}/reported/{propname} {propvalue}'
        """
        try:
            if tp_group_id is None : raise AttributeError("Error 'tp_group_id' cannot be null")
            
            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error

            if prop_value is None:
                raise ValueError("Property Value is not set")

            key = f'twin_properties/{tp_group_id}/{RedisPattern.REPORTED.value}/{prop_name}'
            
            if type(prop_value) ==bool:
                if prop_value:
                     prop_value = "1"
                else:
                    prop_value = "0"
            
            Redis.set(key, prop_value)
            

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the set reported property')
            
    @staticmethod        
    def get_desired_property(prop_name:str, tp_group_id:str):
        """
        Get desired property in Redis key 'get twin_properties/{tp_group_id}/desired/{propname}'
        """
        try:
            if tp_group_id is None : raise AttributeError("Error 'tp_group_id' cannot be null")
            
            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error            

            key = f'twin_properties/{tp_group_id}/{RedisPattern.DESIRED.value}/{prop_name}'

            if Redis.exists(key) <= 0:
                logger.info("Property Name - {} does not exists".format(key))

            return Redis.get(key)

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the get desired property')

    @staticmethod        
    def get_reported_property(prop_name:str, tp_group_id:str):
        """
        Get reported property in Redis key 'get twin_properties/{tp_group_id}/reported/{propname}'
        """
        try:
            if tp_group_id is None : raise AttributeError("Error 'tp_group_id' cannot be null")

            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error

            key = f'twin_properties/{tp_group_id}/{RedisPattern.REPORTED.value}/{prop_name}'

            if Redis.exists(key) <= 0:
                logger.info("Property Name - {} does not exists".format(key))

            return Redis.get(key)

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the get reported property')


@staticmethod
def is_valid_prop_name(prop_name:str):
    if prop_name is None:
        return (False, ValueError("Property Name is not set"))
    return (True, None)       

@staticmethod
def is_valid_prop_value(prop_value:str):
    if prop_value is None:
        return (False, ValueError("Property value is not set"))
    return (True, None)       


Twin = TwinPropertySingleton()
import datetime

from typing import Optional
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.constants import CONNECTION_TYPE_ATHENA, CONNECTION_TYPE_IAM, \
    CONNECTION_TYPE_SPARK_GLUE, CONNECTION_TYPE_GENERAL_SPARK, CONNECTION_TYPE_SPARK_EMR_SERVERLESS, METADATA_CONTENT, \
    DATAZONE_ENDPOINT_URL, DATAZONE_DOMAIN_REGION, DOMAIN_ID, PROJECT_ID
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.exceptions import ConnectionNotSupportedException, \
    ConnectionNotFoundException
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.gateways.datazone_gateway import DataZoneGateway
from sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.constants import CONNECTION_TYPE_REDSHIFT, \
    CONNECTION_TYPE_SPARK_EMR_EC2, SAGEMAKER_DEFAULT_CONNECTION_DISPLAYNAME, SAGEMAKER_DEFAULT_CONNECTION_NAME

EMR_EC2_ARN_KEY_WORD = "cluster"
EMR_SERVERLESS_ARN_KEY_WORD = "applications"


class SageMakerToolkitUtils(object):
    _connection_type_mapping = {
        CONNECTION_TYPE_GENERAL_SPARK : [],
        CONNECTION_TYPE_REDSHIFT: [],
        CONNECTION_TYPE_ATHENA: []
    }
    _datazone_gateway = DataZoneGateway()
    _connection_name_to_connection_id_mapping = {}
    _connection_id_to_connection_details_mapping = {}
    _connection_id_last_cached_time = {}
    _connection_list_last_cached_time = None
    _glue_connection_names = []
    _cache_time_minutes = 5

    @classmethod
    def get_connection_type_mapping(cls):
        if (not cls._connection_list_last_cached_time or (cls._connection_list_last_cached_time
                and datetime.datetime.now() - cls._connection_list_last_cached_time > datetime.timedelta(minutes=cls._cache_time_minutes))):
            try:
                cls._cache_connection_list_from_datazone()
            except:
                pass
        return cls._connection_type_mapping

    @classmethod
    def get_connection_detail(cls, sagemaker_connection_name: str, with_secret: Optional[bool] = False) -> dict:
        connection_detail = cls._get_connection_detail_with_connection_name(
            sagemaker_connection_name=sagemaker_connection_name, with_secret=with_secret)
        return connection_detail

    @classmethod
    def is_connection_valid(cls, sagemaker_connection_name) -> bool:
        try:
            cls.get_connection_detail(sagemaker_connection_name=sagemaker_connection_name)
            return True
        except:
            return False

    @classmethod
    def get_connection_detail_from_id(cls, connection_id: str, with_secret: Optional[bool] = False) -> dict:
        return cls._get_connection_detail_with_connection_id(connection_id, with_secret=with_secret)

    @classmethod
    def get_connection_type(cls, sagemake_connection_name) -> str:
        if sagemake_connection_name == SAGEMAKER_DEFAULT_CONNECTION_DISPLAYNAME:
            sagemake_connection_name = SAGEMAKER_DEFAULT_CONNECTION_NAME
        connection_detail = cls.get_connection_detail(sagemaker_connection_name=sagemake_connection_name)
        connection_type = connection_detail["type"]
        if ((connection_type == CONNECTION_TYPE_ATHENA
             or connection_type == CONNECTION_TYPE_REDSHIFT)
                or connection_type == CONNECTION_TYPE_IAM):
            return connection_type
        elif connection_type == CONNECTION_TYPE_GENERAL_SPARK:
            if connection_detail["props"] and "sparkGlueProperties" in connection_detail["props"]:
                return CONNECTION_TYPE_SPARK_GLUE
            if connection_detail["props"] and "sparkEmrProperties" in connection_detail["props"]:
                if connection_detail["props"]["sparkEmrProperties"]["computeArn"] and EMR_EC2_ARN_KEY_WORD in \
                        connection_detail["props"]["sparkEmrProperties"]["computeArn"]:
                    return CONNECTION_TYPE_SPARK_EMR_EC2
                elif connection_detail["props"]["sparkEmrProperties"]["computeArn"] and EMR_SERVERLESS_ARN_KEY_WORD in \
                        connection_detail["props"]["sparkEmrProperties"]["computeArn"]:
                    return CONNECTION_TYPE_SPARK_EMR_SERVERLESS
                else:
                    raise RuntimeError(f"Unable to determine the EMR type of connection {sagemake_connection_name}")
        raise ConnectionNotSupportedException(f"{sagemake_connection_name} type {connection_type} is not supported")

    @classmethod
    def get_connection_id_from_connection_name(cls, sagemake_connection_name: str) -> str:
        if sagemake_connection_name == SAGEMAKER_DEFAULT_CONNECTION_DISPLAYNAME:
            sagemake_connection_name = SAGEMAKER_DEFAULT_CONNECTION_NAME
        connection_detail = cls._get_connection_detail_with_connection_name(sagemake_connection_name, False)
        return connection_detail["connectionId"]

    @classmethod
    def has_key_chain_in_connection_detail(cls, connection, key_chain):
        """
        checks if a nested dictionary contains a chain of keys.
        This function can be used to check if a connection detail contains a chain of keys in its response
        example: SageMakerToolkitUtils.has_key_chain_in_connection_detail(athena_connection_details, ["props", "athenaProperties", "workgroupName"]) -> true
        example: SageMakerToolkitUtils.has_key_chain_in_connection_detail(athena_connection_details, ["props", "redshiftProperties", "workgroupName"]) -> false
        """
        current_dict = connection
        for key in key_chain:
            if not isinstance(current_dict, dict):
                return False
            if key not in current_dict:
                return False
            current_dict = current_dict[key]
        return True

    @classmethod
    def get_glue_connection_names(cls) -> list:
        return cls._glue_connection_names

    @classmethod
    def _cache_connection_list_from_datazone(cls):
        cls._initialize_datazone_gateway_if_not_exist()
        connection_list = cls._datazone_gateway.list_connections()
        cls._glue_connection_names = []
        for connection in connection_list:
            connection_type = connection["type"]
            typeList = cls._connection_type_mapping.get(connection_type, [])
            typeList.append(connection["name"])
            cls._connection_type_mapping[connection_type] = typeList

            cls._connection_name_to_connection_id_mapping[connection["name"]] = connection["connectionId"]
            if (cls._is_connection_ready(connection)
                    and "physicalEndpoints" in connection.keys() and connection["physicalEndpoints"]):
                for physicalEndpoint in connection["physicalEndpoints"]:
                    if ("glueConnectionName" in physicalEndpoint.keys()
                            and physicalEndpoint["glueConnectionName"] not in cls._glue_connection_names):
                        cls._glue_connection_names.append(physicalEndpoint["glueConnectionName"])
        cls._connection_list_last_cached_time = datetime.datetime.now()
        return

    @classmethod
    def _get_connection_detail_with_connection_id(cls, connection_id: str, with_secret: Optional[bool] = False):
        cls._initialize_datazone_gateway_if_not_exist()
        if (not with_secret and connection_id in cls._connection_id_to_connection_details_mapping and
                datetime.datetime.now() - cls._connection_id_last_cached_time[connection_id] <= datetime.timedelta(minutes=cls._cache_time_minutes)):
            return cls._connection_id_to_connection_details_mapping[connection_id]
        else:
            connection_detail = cls._datazone_gateway.get_connection(connection_id, with_secret=with_secret)
            cls._connection_id_to_connection_details_mapping[connection_id] = connection_detail
            cls._connection_id_last_cached_time[connection_id] = datetime.datetime.now()
            return connection_detail

    @classmethod
    def _get_connection_detail_with_connection_name(cls, sagemaker_connection_name: str,
                                                    with_secret: Optional[bool] = False) -> dict:
        if (sagemaker_connection_name in cls._connection_name_to_connection_id_mapping
                and datetime.datetime.now() - cls._connection_list_last_cached_time
                <= datetime.timedelta(minutes=cls._cache_time_minutes)):

            connection_id = cls._connection_name_to_connection_id_mapping[sagemaker_connection_name]
            try:
                connection_detail = cls._get_connection_detail_with_connection_id(connection_id,
                                                                                  with_secret=with_secret)
            except Exception:
                raise ConnectionNotFoundException(f"Could not get connection: {sagemaker_connection_name} from DataZone")
        else:
            cls._cache_connection_list_from_datazone()
            if sagemaker_connection_name not in cls._connection_name_to_connection_id_mapping:
                raise ConnectionNotFoundException(
                    f"Connection {sagemaker_connection_name} does not exist")
            connection_id = cls._connection_name_to_connection_id_mapping[sagemaker_connection_name]
            connection_detail = cls._get_connection_detail_with_connection_id(connection_id, with_secret=with_secret)
        return connection_detail

    @classmethod
    def _initialize_datazone_gateway_if_not_exist(cls):
        if cls._datazone_gateway.datazone_client is None:
            if METADATA_CONTENT:
                cls._datazone_gateway.initialize_default_clients()
            else:
                cls._datazone_gateway.initialize_clients(profile="default",
                                                         region=DATAZONE_DOMAIN_REGION,
                                                         endpoint_url=DATAZONE_ENDPOINT_URL,
                                                         domain_identifier=DOMAIN_ID,
                                                         project_identifier=PROJECT_ID)

    @classmethod
    def get_account_id_from_connection(cls, connection_name: str) -> str:
        """Get AWS account ID from connection details."""
        connection_details = cls.get_connection_detail(connection_name)
        return connection_details["physicalEndpoints"][0]["awsLocation"]["awsAccountId"]

    @classmethod
    def _is_connection_ready(cls, connection):
        if ("props" in connection.keys() and connection["props"]
                and "glueProperties" in connection["props"].keys() and connection["props"]["glueProperties"]
                and "status" in connection["props"]["glueProperties"].keys()
                and connection["props"]["glueProperties"]["status"] == "READY"):
            return True
        else:
            return False

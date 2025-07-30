from logger_local.LoggerComponentEnum import LoggerComponentEnum

PYTHON_SDK_REMOTE_COMPONENT_ID = 184
PYTHON_SDK_REMOTE_COMPONENT_NAME = 'python_sdk_remote'

OBJECT_TO_INSERT_CODE = {
    'component_id': PYTHON_SDK_REMOTE_COMPONENT_ID,
    'component_name': PYTHON_SDK_REMOTE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'sahar.g@circ.zone'
}

OBJECT_TO_INSERT_TEST = {
    'component_id': PYTHON_SDK_REMOTE_COMPONENT_ID,
    'component_name': PYTHON_SDK_REMOTE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'sahar.g@circ.zone'
}

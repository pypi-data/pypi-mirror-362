import uuid

def generate_unique_id():
    """
    生成一个不重复的唯一ID
    :return: 返回字符串形式的唯一ID
    """
    return str(uuid.uuid4())
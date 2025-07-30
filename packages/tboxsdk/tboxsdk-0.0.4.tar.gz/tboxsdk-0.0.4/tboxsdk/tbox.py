from typing import List

from .core.httpclient import HttpClientConfig, HttpClient
from .core.exception import TboxClientConfigException
from .model.message import MessageParser
from .model.file import File


class TboxClient(object):
    """
    Tbox client
    """

    """
    tbox client config
    """
    http_client_config: HttpClientConfig = None
    """
    http client
    """
    httpClient: HttpClient = None

    def __init__(self, http_client_config: HttpClientConfig = None, authorization: str = None):
        """
        :param http_client_config:
        :param authorization:
        """
        self.http_client_config = http_client_config if http_client_config is not None else HttpClientConfig()
        # 这里加个简化写法的代码, 方便使用者初始化客户端
        if authorization is not None:
            self.http_client_config.authorization = authorization
        self.httpClient = HttpClient(self.http_client_config)
        return

    def chat(self,
             appId: str,
             query: str,
             userId: str,
             conversationId: str = None,
             requestId: str = None,
             inputs: dict = None,
             clientProperties: dict = None,
             files: List[File] = None,
             withMeta: bool = False,
             messageParser: MessageParser = None
             ):
        """
        tbox client chat
        用于调用 tbox 的 chat 类型应用
        返回格式是统一的流式响应格式
        FIXME: 这里需要以后有文档地址以后，把文档地址贴到这里
        """
        data = {
            "appId": appId,
            "query": query,
        }
        if conversationId is not None:
            data["conversationId"] = conversationId
        if requestId is not None:
            data["requestId"] = requestId
        if inputs is not None:
            data["inputs"] = inputs
        if userId is not None:
            data["userId"] = userId
        if clientProperties is not None:
            data["clientProperties"] = clientProperties
        if files is not None:
            data["files"] = files
        response_iter = self.httpClient.post_stream('/api/chat', data=data, timeout=110)
        return self._stream(response_iter, messageParser=messageParser, withMeta=withMeta)

    def chat_sync(self,
                  appId: str,
                  query: str,
                  userId: str,
                  conversationId: str = None,
                  requestId: str = None,
                  inputs: dict = None,
                  clientProperties: dict = None,
                  files: List[File] = None,
                  ):
        """
        tbox client chat
        同步接口，将chat 接口封装成同步接口
        返回格式：
        {
            '多返回lane' : {
                "type": "返回数据类型",
                "data": "" or {}, # 这里是聚合后的数据结果，比如流式响应文字会拼接成一个文字
                "header": {}, # 响应头，参考流式响应结果的header内容
                "messages": [] # 该 lane 下所有的 chunk 类型的报文，保存在这里
            }
        }
        """
        messageParser = MessageParser()

        events = self.chat(appId, query, userId, conversationId=conversationId, requestId=requestId, inputs=inputs,
                           clientProperties=clientProperties, withMeta=False, messageParser=messageParser, files=files)
        for event in events:
            # do nothing
            pass

        return messageParser.answers_holder

    def completion(self,
                   appId: str,
                   userId: str,
                   conversationId: str = None,
                   requestId: str = None,
                   inputs: dict = None,
                   clientProperties: dict = None,
                   files: List[File] = None,
                   withMeta: bool = False,
                   messageParser: MessageParser = None
                   ):
        data = {
            "appId": appId,
        }
        if conversationId is not None:
            data["conversationId"] = conversationId
        if requestId is not None:
            data["requestId"] = requestId
        if inputs is not None:
            data["inputs"] = inputs
        if userId is not None:
            data["userId"] = userId
        if clientProperties is not None:
            data["clientProperties"] = clientProperties
        if files is not None:
            data["files"] = files
        response_iter = self.httpClient.post_stream('/api/completion', data=data, timeout=110)
        return self._stream(response_iter, messageParser=messageParser, withMeta=withMeta)

    def completion_sync(self,
                        appId: str,
                        userId: str,
                        conversationId: str = None,
                        requestId: str = None,
                        inputs: dict = None,
                        clientProperties: dict = None,
                        files: List[File] = None,
                        ):
        """
        tbox client completion
        同步接口，将completion 接口封装成同步接口
        返回格式：
        {
            '多返回lane' : {
                "type": "返回数据类型",
                "data": "" or {}, # 这里是聚合后的数据结果，比如流式响应文字会拼接成一个文字
                "header": {}, # 响应头，参考流式响应结果的header内容
                "messages": [] # 该 lane 下所有的 chunk 类型的报文，保存在这里
            }
        }
        """
        messageParser = MessageParser()
        events = self.completion(appId, userId, conversationId=conversationId, requestId=requestId, inputs=inputs,
                                 clientProperties=clientProperties, withMeta=False, messageParser=messageParser, files=files)
        for event in events:
            # do nothing
            pass
        return messageParser.answers_holder

    def _stream(self, response_iter, messageParser: MessageParser = None, withMeta=False):
        """
        stream
        :param response_iter: http response iter
        :param messageParser: message parser
        """
        if messageParser is not None:
            parser = messageParser
        else:
            parser = MessageParser()
        for event in response_iter:
            # 解析响应内容的list，如果其中有一个是 error，则抛出异常
            if event.event == 'error':
                raise TboxClientConfigException(event.data)
            # 判断下这段内容是否需要解析
            if parser.need_parse(event):
                data = parser.parse(event)
                if data.get("type") == 'meta':
                    if withMeta:
                        yield data
                else:
                    yield data

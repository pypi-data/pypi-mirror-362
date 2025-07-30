import json
import logging

from tboxsdk.core.httpclient import HttpResponseEvent
from tboxsdk.core.exception import TboxServerException

logger = logging.getLogger("tbox.client")

class MessageParser(object):
    """
    message parser
    用来解析 http sse 响应报文
    """

    """
    用来持有 answers 的众多结果。
    用来保存多返回的内容是什么结构、类型
    answers ==> {
        "lane_key" :{ // 用来持有 响应的 lane,默认default，在工作流中可以查看有哪些响应key 
            "type" : "text", // 用来持有 响应类型： text、images、object等等
            "data": {}, // 用来持有 各种类型的响应值的最终聚合数据，比如text类型的流式响应，会被归集为一个字符串
            "header" : {}, // 用来持有每个lane的响应头
            "messages" : [] // 用来持有所有的chunk 类型的报文，保存在这里
        }
    
    }
    """
    answers_holder: dict = {}

    def need_parse(self, response_event: HttpResponseEvent) -> bool:
        """
        need parse
        :param response_event: http response event
        """
        if response_event.event in ("message", "error"):
            return True
        else:
            return False

    def parse(self, response_event: HttpResponseEvent) -> dict:
        if response_event.event == "error":
            self.parse_error(response_event)
        """
        parse
        :param response_event: http response event
        """
        if response_event.event == "message":
            data = json.loads(response_event.data)
            # 这里会有：header/chunk/meta/revoke/error/charge/end/unknown/followup
            if data.get("type") == "meta":
                return self.parse_meta_message(data)
            elif data.get("type") == "header":
                return self.parse_header_message(data)
            elif data.get("type") == "chunk":
                return self.parse_chunk_message(data)
            elif data.get("type") == "revoke":
                return self.parse_revoke_message(data)
            elif data.get("type") == "error":
                return self.parse_error_message(data)
            elif data.get("type") == "charge":
                return self.parse_charge_message(data)
            elif data.get("type") == "end":
                return self.parse_end_message(data)
            elif data.get("type") == "unknown":
                return self.parse_unknown_message(data)
            elif data.get("type") == "followup":
                return self.parse_followup_message(data)
            else:
                return data

        return json.loads(response_event.data)

    def parse_chunk_message(self, data: dict) -> dict:
        """
        parse message
        :param response_event: http response event
        """
        lane = data.get("lane", "default")
        mediaType = self.answers_holder.get(lane, {}).get("type", 'text');
        data['payload'] = json.loads(data.get("payload", "{}"))
        if mediaType == "text":
            self.answers_holder[lane]["data"] += data.get("payload", {}).get("text", "")
        self.answers_holder[lane]["messages"].append(data)
        return data

    def parse_meta_message(self, data: dict) -> dict:
        """
        parse meta
        :param response_event: http response event
        """
        return data

    def parse_header_message(self, data: dict) -> dict:
        """
        parse message
        :param data: http response event's data
        """
        if data.get("lane") is None:
            data["lane"] = "default"
        # 拆解playload
        payload = json.loads(data.get("payload", "{}"))
        data["payload"] = payload
        media_type = payload.get("mediaType")

        # 将内容写入到 answer holder 中
        if self.answers_holder.get(data["lane"]) is None:
            self.answers_holder[data["lane"]] = {
                "type": media_type,
                "header": data,
                "data": "",
                "messages": [],
            }
        else:
            self.answers_holder[data["lane"]]["header"] = data
            self.answers_holder[data["lane"]]["type"] = media_type
        return data

    def parse_revoke_message(self, data: dict) -> dict:
        return data

    def parse_error_message(self, data: dict) -> dict:
        return data

    def parse_charge_message(self, data: dict) -> dict:
        return data

    def parse_end_message(self, data: dict) -> dict:
        return data

    def parse_unknown_message(self, data: dict) -> dict:
        return data

    def parse_followup_message(self, data: dict) -> dict:
        return data

    def parse_error(self, response_event: HttpResponseEvent) -> None:
        error_context = json.loads(response_event.data)
        message = error_context.get("description", "unknown error")
        exception = TboxServerException(message)
        exception.error_context = error_context
        raise exception

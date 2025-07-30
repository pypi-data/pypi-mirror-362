import asyncio
import json
import logging

import numpy as np
import requests

from xiaozhi_sdk.utils.mcp_data import mcp_initialize_payload, mcp_tool_conf, mcp_tools_payload
from xiaozhi_sdk.utils.mcp_tool import _get_random_music_info

logger = logging.getLogger("xiaozhi_sdk")


class McpTool(object):

    def __init__(self):
        self.session_id = ""
        self.explain_url = ""
        self.explain_token = ""
        self.websocket = None
        self.tool_func = {}
        self.is_playing = False

    def get_mcp_json(self, payload: dict):
        return json.dumps({"session_id": self.session_id, "type": "mcp", "payload": payload})

    def _build_response(self, request_id: str, content: str, is_error: bool = False):
        return self.get_mcp_json(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": content}],
                    "isError": is_error,
                },
            }
        )

    async def analyze_image(self, img_byte: bytes, question: str = "这张图片里有什么？"):
        headers = {"Authorization": f"Bearer {self.explain_token}"}
        files = {"file": ("camera.jpg", img_byte, "image/jpeg")}
        payload = {"question": question}
        try:
            response = requests.post(self.explain_url, files=files, data=payload, headers=headers, timeout=5)
            res_json = response.json()
        except Exception as e:
            return "网络异常", True
        if res_json.get("error"):
            return res_json, True
        return res_json, False

    async def play_custom_music(self, tool_func, arguments):
        pcm_array, is_error = await tool_func(arguments)
        while True:
            if not self.is_playing:
                break
            await asyncio.sleep(0.1)
        pcm_array = await self.audio_opus.change_sample_rate(np.array(pcm_array))
        self.output_audio_queue.extend(pcm_array)

    async def mcp_tool_call(self, mcp_json: dict):
        tool_name = mcp_json["params"]["name"]
        tool_func = self.tool_func[tool_name]
        arguments = mcp_json["params"]["arguments"]
        try:
            if tool_name == "async_play_custom_music":

                # v1 返回 url
                music_info = await _get_random_music_info(arguments["id_list"])
                if not music_info.get("url"):
                    tool_res, is_error = {"message": "播放失败"}, True
                else:
                    tool_res, is_error = {"message": "正在为你播放: {}".format(arguments["music_name"])}, False
                    data = {
                        "type": "music", "state": "start",
                        "url": music_info["url"],
                        "text": arguments["music_name"],
                        "source": "sdk.mcp_music_tool"
                    }
                    await self.message_handler_callback(data)

                # v2 音频放到输出
                # asyncio.create_task(self.play_custom_music(tool_func, arguments))

            elif tool_name.startswith("async_"):
                tool_res, is_error = await tool_func(arguments)
            else:
                tool_res, is_error = tool_func(arguments)
        except Exception as e:
            logger.error("[MCP] tool_func error: %s", e)
            return self._build_response(mcp_json["id"], "工具调用失败", True)

        if tool_name == "take_photo":
            tool_res, is_error = await self.analyze_image(tool_res, mcp_json["params"]["arguments"]["question"])

        content = json.dumps(tool_res, ensure_ascii=False)
        return self._build_response(mcp_json["id"], content, is_error)

    async def mcp(self, data: dict):
        payload = data["payload"]
        method = payload["method"]

        if method == "initialize":
            self.explain_url = payload["params"]["capabilities"]["vision"]["url"]
            self.explain_token = payload["params"]["capabilities"]["vision"]["token"]

            mcp_initialize_payload["id"] = payload["id"]
            await self.websocket.send(self.get_mcp_json(mcp_initialize_payload))

        elif method == "notifications/initialized":
            # print("\nMCP 工具初始化")
            pass

        elif method == "notifications/cancelled":
            logger.error("[MCP] 工具加载失败")

        elif method == "tools/list":
            mcp_tools_payload["id"] = payload["id"]
            tool_list = []
            for name, func in self.tool_func.items():
                if func:
                    tool_list.append(name)
                    target_name = name.removeprefix("async_")
                    mcp_tool_conf[target_name]["name"] = name
                    mcp_tools_payload["result"]["tools"].append(mcp_tool_conf[target_name])
            await self.websocket.send(self.get_mcp_json(mcp_tools_payload))
            logger.debug("[MCP] 加载成功，当前可用工具列表为：%s", tool_list)

        elif method == "tools/call":
            tool_name = payload["params"]["name"]
            if not self.tool_func.get(tool_name):
                logger.warning("[MCP] Tool not found: %s", tool_name)
                return

            mcp_res = await self.mcp_tool_call(payload)
            await self.websocket.send(mcp_res)
            logger.debug("[MCP] Tool %s called", tool_name)
        else:
            logger.warning("[MCP] unknown method %s: %s", method, payload)

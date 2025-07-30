from typing import Any, Dict, List

mcp_initialize_payload: Dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "", "version": "0.0.1"},
    },
}

mcp_tool_conf: Dict[str, Dict[str, Any]] = {
    "search_custom_music": {
        "description": "Search music and get music IDs. Use this tool when the user asks to search or play music. This tool returns a list of music with their IDs, which are required for playing music. Args:\n  `music_name`: The name of the music to search\n  `author_name`: The name of the music author (optional)",
        "inputSchema": {
            "type": "object",
            "properties": {"music_name": {"type": "string"}, "author_name": {"type": "string"}},
            "required": ["music_name"],
        },
    },
    "play_custom_music": {
        "description": "Play music using music IDs. IMPORTANT: You must call `search_custom_music` first to get the music IDs before using this tool. Use this tool after getting music IDs from search results. Args:\n  `id_list`: The id list of the music to play (obtained from search_custom_music results). The list must contain more than 2 music IDs, and the system will randomly select one to play.\n  `music_name`: The name of the music (obtained from search_custom_music results)",
        "inputSchema": {
            "type": "object",
            "properties": {"music_name": {"type": "string"}, "id_list": {"type": "array", "items": {"type": "string"}, "minItems": 3}},
            "required": ["music_name", "id_list"],
        },
    },
    "get_device_status": {
        "description": "Provides the real-time information of the device, including the current status of the audio speaker, screen, battery, network, etc.\nUse this tool for: \n1. Answering questions about current condition (e.g. what is the current volume of the audio speaker?)\n2. As the first step to control the device (e.g. turn up / down the volume of the audio speaker, etc.)",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "set_volume": {
        "description": "Set the volume of the audio speaker. If the current volume is unknown, you must call `get_device_status` tool first and then call this tool.",
        "inputSchema": {
            "type": "object",
            "properties": {"volume": {"type": "integer", "minimum": 0, "maximum": 100}},
            "required": ["volume"],
        },
    },
    "set_brightness": {
        "description": "Set the brightness of the screen.",
        "inputSchema": {
            "type": "object",
            "properties": {"brightness": {"type": "integer", "minimum": 0, "maximum": 100}},
            "required": ["brightness"],
        },
    },
    "set_theme": {
        "description": "Set the theme of the screen. The theme can be `light` or `dark`.",
        "inputSchema": {"type": "object", "properties": {"theme": {"type": "string"}}, "required": ["theme"]},
    },
    "take_photo": {
        "description": "Take a photo and explain it. Use this tool after the user asks you to see something.\nArgs:\n  `question`: The question that you want to ask about the photo.\nReturn:\n  A JSON object that provides the photo information.",
        "inputSchema": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"],
        },
    },
    "open_tab": {
        "description": "Open a web page in the browser. 小智后台：https://xiaozhi.me",
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    },
}

mcp_tools_payload: Dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 2,
    "result": {"tools": []},
}

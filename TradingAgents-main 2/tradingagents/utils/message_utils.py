"""
メッセージ型の安全な処理を行うためのユーティリティ関数群

このモジュールはLangChainのメッセージ型に対する型安全なアクセスを提供します。
Union型のメッセージで安全に属性にアクセスするための型ガード関数群を含みます。
"""

from typing import TypeGuard, Optional, Any, List, Union
from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    FunctionMessage,
    ChatMessage,
)


def has_tool_calls(message: BaseMessage) -> TypeGuard[AIMessage]:
    """
    メッセージがtool_calls属性を持つかどうかを判定する型ガード関数
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: tool_calls属性を持つ場合True、そうでなければFalse
        型ガードによって、TrueならmessageはAIMessage型として扱われる
    """
    return isinstance(message, AIMessage) and hasattr(message, 'tool_calls')


def has_content(message: BaseMessage) -> bool:
    """
    メッセージがcontent属性を持つかどうかを判定
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: content属性を持つ場合True、そうでなければFalse
    """
    return hasattr(message, 'content') and message.content is not None


def is_ai_message(message: BaseMessage) -> TypeGuard[AIMessage]:
    """
    メッセージがAIMessageかどうかを判定する型ガード関数
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: AIMessageの場合True、そうでなければFalse
    """
    return isinstance(message, AIMessage)


def is_human_message(message: BaseMessage) -> TypeGuard[HumanMessage]:
    """
    メッセージがHumanMessageかどうかを判定する型ガード関数
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: HumanMessageの場合True、そうでなければFalse
    """
    return isinstance(message, HumanMessage)


def is_system_message(message: BaseMessage) -> TypeGuard[SystemMessage]:
    """
    メッセージがSystemMessageかどうかを判定する型ガード関数
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: SystemMessageの場合True、そうでなければFalse
    """
    return isinstance(message, SystemMessage)


def is_tool_message(message: BaseMessage) -> TypeGuard[ToolMessage]:
    """
    メッセージがToolMessageかどうかを判定する型ガード関数
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: ToolMessageの場合True、そうでなければFalse
    """
    return isinstance(message, ToolMessage)


def get_tool_calls_safely(message: BaseMessage) -> Optional[List[Any]]:
    """
    メッセージから安全にtool_callsを取得
    
    Args:
        message: tool_callsを取得するBaseMessageオブジェクト
        
    Returns:
        Optional[List[Any]]: tool_callsのリスト、存在しない場合はNone
    """
    if has_tool_calls(message):
        return message.tool_calls
    return None


def get_content_safely(message: BaseMessage) -> Optional[str]:
    """
    メッセージから安全にcontentを取得
    
    Args:
        message: contentを取得するBaseMessageオブジェクト
        
    Returns:
        Optional[str]: contentの文字列、存在しない場合はNone
    """
    if has_content(message):
        return str(message.content)
    return None


def get_message_type(message: BaseMessage) -> str:
    """
    メッセージの型名を取得
    
    Args:
        message: 型名を取得するBaseMessageオブジェクト
        
    Returns:
        str: メッセージの型名
    """
    return message.__class__.__name__


def has_tool_calls_and_not_empty(message: BaseMessage) -> bool:
    """
    メッセージがtool_calls属性を持ち、かつ空でないかを判定
    
    Args:
        message: 判定対象のBaseMessageオブジェクト
        
    Returns:
        bool: tool_callsが存在し空でない場合True、そうでなければFalse
    """
    if has_tool_calls(message):
        tool_calls = message.tool_calls
        return tool_calls is not None and len(tool_calls) > 0
    return False


def safe_tool_calls_check(message: BaseMessage) -> bool:
    """
    tool_callsの存在と内容を安全にチェック（conditional_logic用）
    
    この関数は既存のif last_message.tool_calls:パターンの置き換えに使用されます。
    
    Args:
        message: チェック対象のBaseMessageオブジェクト
        
    Returns:
        bool: tool_callsが存在し、真値評価でTrueになる場合True
    """
    tool_calls = get_tool_calls_safely(message)
    return bool(tool_calls)
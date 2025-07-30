import requests
import pandas as pd
import socket
import logging
import json
import time
from typing import List, Dict, Any, Optional

# 配置日志格式和级别
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义项目工具类
class Dispider:
    """
    Dispider 爬虫客户端工具。

    该工具专为在爬虫容器内部运行的脚本设计，封装了与 Dispider 后端服务交互的
    核心爬虫工作流，包括获取任务、提交结果、报告状态等。

    使用示例:
        >>> # 在爬虫脚本中
        >>> from dispider import Dispider
        >>>
        >>> # 初始化客户端，worker_id 会自动使用容器 hostname
        >>> client = Dispider(
        ...     base_url="http://dispider-backend:8000",
        ...     project_id=1,
        ...     username="crawler_user",
        ...     password="crawler_password"
        ... )
        >>>
        >>> # 获取一个待处理的任务
        >>> task = client.get_next_task()
        >>> if task:
        ...     try:
        ...         # ... 执行爬虫逻辑 ...
        ...         result = {"data": "some_scraped_data"}
        ...         client.submit_task_result(task['id'], result)
        ...     except Exception as e:
        ...         client.report_task_failure(task['id'], str(e))
    """

    def __init__(self, base_url: str, project_id: int, username: str, password: str, worker_id: Optional[str] = None):
        """
        初始化 Dispider 爬虫客户端。

        在实例化时，会自动登录后端服务以获取认证 token，并为后续所有 API 请求做好准备。

        Args:
            base_url (str): FastAPI 服务的根 URL (例如 "http://dispider-backend:8000")。
            project_id (int): 当前爬虫所属项目的 ID。
            username (str): 用于认证的用户名。
            password (str): 用于认证的密码。
            worker_id (Optional[str], optional): 当前爬虫的唯一标识符。
                如果未提供，将自动使用当前主机的 hostname。 Defaults to None.
        """
        self.base_url = base_url.rstrip('/')
        self.project_id = project_id
        
        # 如果未提供 worker_id，则自动获取主机名作为唯一标识
        self.worker_id = worker_id or socket.gethostname()
        
        self._session = requests.Session()
        self.task_id = None
        logging.info(f"Dispider 客户端正在为项目 {self.project_id} 初始化，Worker ID: {self.worker_id}")
        self._login(username, password)
        logging.info("客户端初始化并登录成功。")

    def _login(self, username, password):
        """
        内部登录方法，获取并为会话设置 access token。
        """
        login_url = f"{self.base_url}/auth/token"
        try:
            # 这里的 headers 需要设置为 'application/x-www-form-urlencoded'
            # requests 会在 data 参数不为 dict 时自动处理，但显式声明更清晰
            response = self._session.post(login_url, data={"username": username, "password": password})
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("登录响应中未找到 access_token。")
            self._session.headers.update({"Authorization": f"Bearer {access_token}"})
            logging.info(f"用户 '{username}' 登录成功。")
        except requests.exceptions.HTTPError as e:
            logging.error(f"登录失败: {e.response.status_code} {e.response.text}")
            raise ConnectionError(f"登录认证失败，请检查用户名和密码: {e.response.text}") from e
        except requests.exceptions.RequestException as e:
            logging.error(f"连接到 {login_url} 时发生网络错误: {e}")
            raise ConnectionError(f"连接到后端服务时发生网络错误: {e}") from e

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        统一的请求发送方法，封装了 URL 构建、认证和错误处理。
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self._session.request(method, url, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:  # No Content
                return None
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_message = f"API 请求失败 ({method} {url}): {e.response.status_code} {e.response.text}"
            logging.error(error_message)
            raise RuntimeError(error_message) from e
        except requests.exceptions.RequestException as e:
            error_message = f"请求 {url} 时发生网络错误: {e}"
            logging.error(error_message)
            raise ConnectionError(error_message) from e

    # --- 1 & 2. 表初始化 ---
    def initialize_tasks_table(self, columns: List[str]) -> Dict[str, Any]:
        """
        为当前项目初始化或重建任务表。
        这是一个准备阶段的操作，通常在批量下发任务前执行一次。

        Args:
            columns (List[str]): 任务表的列名列表。

        Returns:
            Dict[str, Any]: API 返回的成功消息。
        """
        logging.info(f"正在为项目 {self.project_id} 初始化任务表，列: {columns}")
        endpoint = f'/projects/{self.project_id}/tasks/table'
        return self._request('POST', endpoint, json={"columns": columns})

    def initialize_results_table(self, columns: List[str]) -> Dict[str, Any]:
        """
        为当前项目初始化或重建结果表。
        这是一个准备阶段的操作，在提交任何结果前需要执行。

        Args:
            columns (List[str]): 结果表的列名列表。

        Returns:
            Dict[str, Any]: API 返回的成功消息。
        """
        logging.info(f"正在为项目 {self.project_id} 初始化结果表，列: {columns}")
        endpoint = f'/projects/{self.project_id}/results/table'
        return self._request('POST', endpoint, json={"columns": columns})

    # --- 3. 新增任务 ---
    def add_tasks(self, tasks_df: pd.DataFrame) -> Dict[str, Any]:
        """
        通过 Pandas DataFrame 批量添加任务到任务表。

        Args:
            tasks_df (pd.DataFrame): 包含任务数据的 DataFrame，其列名应与任务表匹配。

        Returns:
            Dict[str, Any]: API 返回的批量插入结果，包含成功插入的记录数。
        """
        if not isinstance(tasks_df, pd.DataFrame) or tasks_df.empty:
            raise ValueError("tasks_df 必须是一个非空的 Pandas DataFrame。")
        logging.info(f"正在为项目 {self.project_id} 从 DataFrame 批量添加 {len(tasks_df)} 个任务...")
        tasks_data = tasks_df.to_dict(orient='list')
        endpoint = f'/projects/{self.project_id}/tasks'
        return self._request('POST', endpoint, json=tasks_data)

    # --- 4. 提交结果 ---
    def submit_task_result(self, result_data: Dict[str, Any], note_list: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        为已完成的任务提交结果。

        Args:
            result_data (Dict[str, Any]): 包含结果数据的字典，其键应与结果表列名匹配。
            note_list (Optional[List[str]], optional): 结果的注释列表。如果提供，将被添加到结果数据中。Defaults to None.

        Returns:
            Dict[str, Any]: API 返回的成功消息。
        
        Raises:
            ValueError: 如果提供了 note_list 但其长度与列式结果数据不匹配。
        """
        if note_list:
            # 如果是列式数据 (即字典的值是列表)，则校验 note_list 的长度以确保数据一致性
            if result_data:
                first_val = next(iter(result_data.values()), None)
                if isinstance(first_val, list):
                    if len(first_val) != len(note_list):
                        raise ValueError(
                            f"数据不一致: note_list 的长度 ({len(note_list)}) "
                            f"必须与结果数据中的列长度 ({len(first_val)}) 相同。"
                        )
            
            # 将 note_list 以 'note' 为键，添加到要提交的数据字典中
            result_data['note'] = note_list

        logging.info(f"正在为项目 {self.project_id} 的任务 {self.task_id} 提交结果。")
        endpoint = f'/projects/{self.project_id}/tasks/{self.task_id}/result'
        return self._request('POST', endpoint, json=result_data)

    # --- 5. 获取任务 ---
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        原子化地获取一个待处理的任务。
        这是爬虫工作循环的核心方法。

        Returns:
            Optional[Dict[str, Any]]: 包含任务数据的字典，如果当前没有可用任务，则返回 None。
        """
        logging.debug(f"Worker '{self.worker_id}' 正在为项目 {self.project_id} 请求下一个任务...")
        endpoint = f'/projects/{self.project_id}/tasks/next?worker_id={self.worker_id}'
        task = self._request('GET', endpoint)
        self.task_id = task.get('id')
        if task:
            logging.info(f"获取到新任务 {task.get('id')}。")
        else:
            logging.info("当前没有待处理的任务。")
        return task

    # --- 6. 报告容器状态 ---
    def report_needs_manual_intervention(self, message: str) -> Dict[str, Any]:
        """
        向系统报告当前容器需要人工干预。
        当爬虫遇到无法自动恢复的严重错误（如 IP 被封、配置错误等）时调用此方法。

        Args:
            message (str): 描述需要人工干预原因的消息。

        Returns:
            Dict[str, Any]: API 返回的成功消息。
        """
        logging.warning(f"Worker '{self.worker_id}' 报告需要人工干预: {message}")
        endpoint = f'/projects/{self.project_id}/containers/{self.worker_id}/status'
        payload = {"status": "needs_manual_intervention", "message": message}
        return self._request('POST', endpoint, json=payload)

    # --- 7. 报告任务失败 ---
    def report_task_failure(self, error_message: Optional[str] = None) -> Dict[str, Any]:
        """
        报告一个任务执行失败。
        系统后台会根据项目的重试策略来处理这个失败的任务。

        Args:
            error_message (Optional[str], optional): 描述失败原因的错误信息。 Defaults to None.

        Returns:
            Dict[str, Any]: API 返回的成功消息。
        """
        logging.error(f"正在为项目 {self.project_id} 报告任务 {self.task_id} 失败。错误: {error_message}")
        endpoint = f'/projects/{self.project_id}/tasks/{self.task_id}/fail'
        payload = {"error": error_message} if error_message else {}
        return self._request('POST', endpoint, json=payload)

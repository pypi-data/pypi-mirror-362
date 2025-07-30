# db.py
import os
import logging
import pymysql
import uuid
import hashlib
from dbutils.pooled_db import PooledDB
from .utils import (
    get_host_info,
    get_project_parent_dir,
    create_system_uuid_file,
    create_host_uuid_file,
    read_file_content,
    set_file_hidden,
    parse_project_number_from_readme,
    generate_identifier_code
)
from .exceptions import DatabaseConnectionException

# 配置日志
logger = logging.getLogger("ProjectSecurityLogger")

# 连接池全局变量
db_pool = None
pool_initialized = False

# 允许的最大主机数量
from .constants import MAX_ALLOWED_HOSTS


def initialize_db_pool():
    """初始化数据库连接池"""
    global db_pool, pool_initialized

    if pool_initialized:
        return db_pool

    try:
        # 从环境变量获取数据库配置
        db_config = {
            'host': os.getenv('DB_HOST', 'mysql5.sqlpub.com'),
            'user': os.getenv('DB_USER', 'funnel'),
            'password': os.getenv('DB_PASSWORD', 'BX4FwWuqDrciPg8H'),
            'database': os.getenv('DB_NAME', 'do_not_use'),
            'port': int(os.getenv('DB_PORT', '3310')),
            'connect_timeout': 5,
        }

        # SSL配置
        ssl_config = {}
        if os.getenv('DB_SSL', 'false').lower() == 'true':
            ssl_ca = os.getenv('DB_SSL_CA', '')
            ssl_cert = os.getenv('DB_SSL_CERT', '')
            ssl_key = os.getenv('DB_SSL_KEY', '')

            if ssl_ca and ssl_cert and ssl_key:
                ssl_config = {
                    'ssl': {
                        'ca': ssl_ca,
                        'cert': ssl_cert,
                        'key': ssl_key,
                        'check_hostname': False
                    }
                }
            else:
                logger.warning("DB_SSL is true but SSL files not provided. Using default SSL context")
                ssl_config = {'ssl': True}

        # 创建pymysql连接池
        db_pool = PooledDB(
            creator=pymysql,
            maxconnections=10,  # 增加连接池大小
            blocking=True,
            setsession=[],
            ping=1,  # 每次使用时ping服务器检查连接
            **db_config,
            **ssl_config
        )

        pool_initialized = True
        return db_pool

    except Exception as e:
        raise DatabaseConnectionException("Failed to initialize database pool") from e


def get_db_connection():
    """获取数据库连接"""
    global db_pool

    if not pool_initialized:
        initialize_db_pool()

    try:
        conn = db_pool.connection()
        return conn
    except Exception as e:
        logger.error(f"Failed to get database connection: {e}", exc_info=True)
        raise DatabaseConnectionException("Failed to get database connection") from e


def check_project_security(host_id, project_uuid):
    """
    增强的安全策略：
    1. 检查项目是否已启动
    2. 如果项目未启动或当前主机是最早的两台设备之一，允许运行
    3. 否则阻止执行
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 第一步：获取项目启动的最早两台主机
            early_hosts_query = """
            SELECT host_id, MIN(first_launch_time) as first_time
            FROM project_launch_logs
            WHERE project_uuid = %s
            GROUP BY host_id
            ORDER BY first_time ASC
            LIMIT %s
            """
            cursor.execute(early_hosts_query, (project_uuid, MAX_ALLOWED_HOSTS))
            early_hosts = cursor.fetchall()
            early_host_ids = [host[0] for host in early_hosts] if early_hosts else []

            # 如果项目未启动或当前主机是最早的之一，允许运行
            if not early_hosts or host_id in early_host_ids:
                return True

            # 当前主机不是最早的两台，阻止运行
            return False

    except Exception as e:
        logger.error(f"Security check database error: {e}", exc_info=True)
        # 安全检测失败时默认允许执行
        return True
    finally:
        if conn:
            conn.close()


def register_activation(host_id, system_uuid_content, project_number_id):
    """注册或更新项目激活关系"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查项目编号是否已被使用
            check_existing_query = """
            SELECT host_id, system_uuid_content 
            FROM project_activation 
            WHERE project_number_id = %s
            """
            cursor.execute(check_existing_query, (project_number_id,))
            existing_record = cursor.fetchone()

            if existing_record:
                existing_host, existing_system_uuid = existing_record
                # 项目编号已被使用，且不是当前主机+项目组合
                if existing_host != host_id or existing_system_uuid != system_uuid_content:
                    return False  # 项目编号已被其他项目使用

            # 检查是否已有相同主机+项目的记录
            check_activation_query = """
            SELECT project_number_id 
            FROM project_activation 
            WHERE host_id = %s 
              AND system_uuid_content = %s
            """
            cursor.execute(check_activation_query, (host_id, system_uuid_content))
            activation_record = cursor.fetchone()

            if activation_record:
                # 更新现有记录
                update_query = """
                UPDATE project_activation 
                SET project_number_id = %s, updated_at = NOW() 
                WHERE host_id = %s 
                  AND system_uuid_content = %s
                """
                cursor.execute(update_query, (project_number_id, host_id, system_uuid_content))
            else:
                # 创建新记录
                insert_query = """
                INSERT INTO project_activation (
                    host_id, 
                    system_uuid_content, 
                    project_number_id
                ) VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (host_id, system_uuid_content, project_number_id))

            conn.commit()
            return True

    except Exception as e:
        logger.error(f"激活注册失败: {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()


def log_launch_to_db(host_id, project_uuid, project_path, uuid_file_path,
                     system_uuid_path, system_uuid_content,
                     host_uuid_path, host_uuid_content):
    """记录启动日志到数据库，优先更新相同主机ID和系统标识内容的记录"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 第一步：检查是否存在相同主机ID和系统标识内容的记录
            check_query = """
            SELECT id, first_launch_time, is_activated, identifier_code, project_number_id
            FROM project_launch_logs
            WHERE host_id = %s
              AND system_uuid_content = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(check_query, (host_id, system_uuid_content))
            existing_record = cursor.fetchone()

            # 如果找到匹配记录，更新现有记录
            if existing_record:
                record_id, first_launch_time, old_is_activated, identifier_code, project_number_id = existing_record
                # 保留原始激活状态
                is_activated = old_is_activated

                # 即使没有项目编号，只要标识文件匹配且之前已激活，保持激活状态
                project_number, new_identifier_code, new_project_number_id = parse_and_register_project_number(
                    project_path)

                # 仅当解析到有效项目编号时才更新激活状态
                if new_project_number_id is not None:
                    # 验证项目编号激活关系
                    activation_ok = register_activation(
                        host_id,
                        system_uuid_content,
                        new_project_number_id
                    )

                    if activation_ok:
                        is_activated = 1
                        identifier_code = new_identifier_code
                        project_number_id = new_project_number_id
                    else:
                        is_activated = 0  # 项目编号已被使用

                update_query = """
                UPDATE project_launch_logs
                SET
                    project_uuid = %s,
                    project_path = %s,
                    uuid_file_path = %s,
                    launch_time = NOW(),
                    hostname = %s,
                    username = %s,
                    mac_address = %s,
                    cpu_id = %s,
                    python_version = %s,
                    os_info = %s,
                    system_uuid_file_path = %s,
                    host_uuid_file_path = %s,
                    host_uuid_content = %s,
                    is_activated = %s,
                    identifier_code = %s,
                    project_number_id = %s
                WHERE id = %s
                """
                host_info = get_host_info()
                cursor.execute(update_query, (
                    project_uuid,
                    project_path,
                    uuid_file_path,
                    host_info["hostname"],
                    host_info["username"],
                    host_info["mac_address"],
                    host_info["cpu_id"],
                    host_info["python_version"],
                    host_info["os_info"],
                    system_uuid_path,
                    host_uuid_path,
                    host_uuid_content,
                    is_activated,
                    identifier_code or "N/A",
                    project_number_id,
                    record_id
                ))
                conn.commit()
                return True, is_activated, identifier_code, project_number_id  # 返回新状态

            # 第二步：如果没有匹配记录，检查是否存在相同主机ID和项目路径的记录
            check_path_query = """
            SELECT id, first_launch_time, is_activated, identifier_code, project_number_id
            FROM project_launch_logs
            WHERE host_id = %s
              AND project_path = %s
            LIMIT 1
            """
            cursor.execute(check_path_query, (host_id, project_path))
            existing_path_record = cursor.fetchone()

            # 更新现有记录（基于项目路径）
            if existing_path_record:
                record_id, first_launch_time, old_is_activated, identifier_code, project_number_id = existing_path_record
                # 保留原始激活状态
                is_activated = old_is_activated

                project_number, new_identifier_code, new_project_number_id = parse_and_register_project_number(
                    project_path)

                # 仅当解析到有效项目编号时才更新激活状态
                if new_project_number_id is not None:
                    # 验证项目编号激活关系
                    activation_ok = register_activation(
                        host_id,
                        system_uuid_content,
                        new_project_number_id
                    )

                    if activation_ok:
                        is_activated = 1
                        identifier_code = new_identifier_code
                        project_number_id = new_project_number_id
                    else:
                        is_activated = 0  # 项目编号已被使用

                update_query = """
                UPDATE project_launch_logs
                SET
                    project_uuid = %s,
                    uuid_file_path = %s,
                    launch_time = NOW(),
                    hostname = %s,
                    username = %s,
                    mac_address = %s,
                    cpu_id = %s,
                    python_version = %s,
                    os_info = %s,
                    system_uuid_file_path = %s,
                    system_uuid_content = %s,
                    host_uuid_file_path = %s,
                    host_uuid_content = %s,
                    is_activated = %s,
                    identifier_code = %s,
                    project_number_id = %s
                WHERE id = %s
                """
                host_info = get_host_info()
                cursor.execute(update_query, (
                    project_uuid,
                    uuid_file_path,
                    host_info["hostname"],
                    host_info["username"],
                    host_info["mac_address"],
                    host_info["cpu_id"],
                    host_info["python_version"],
                    host_info["os_info"],
                    system_uuid_path,
                    system_uuid_content,
                    host_uuid_path,
                    host_uuid_content,
                    is_activated,
                    identifier_code or "N/A",
                    project_number_id,
                    record_id
                ))
                conn.commit()
                return True, is_activated, identifier_code, project_number_id

            # 第三步：如果都没有找到，插入新记录
            # 获取主机信息
            host_info = get_host_info()

            # 尝试解析README.md中的项目编号
            project_number, identifier_code, project_number_id = parse_and_register_project_number(project_path)
            is_activated = 0  # 默认未激活

            # 如果项目编号有效，尝试注册激活
            if project_number_id is not None:
                activation_ok = register_activation(
                    host_id,
                    system_uuid_content,
                    project_number_id
                )
                is_activated = 1 if activation_ok else 0
                if not activation_ok:
                    identifier_code = "N/A"  # 项目编号无效
            else:
                identifier_code = "N/A"  # 项目编号无效

            insert_query = """
            INSERT INTO project_launch_logs (
                host_id,
                project_uuid,
                project_path,
                uuid_file_path,
                first_launch_time,
                hostname,
                username,
                mac_address,
                cpu_id,
                python_version,
                os_info,
                identifier_code,
                is_activated,
                system_uuid_file_path,
                system_uuid_content,
                host_uuid_file_path,
                host_uuid_content,
                project_number_id
            ) VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                host_id,
                project_uuid,
                project_path,
                uuid_file_path,
                host_info["hostname"],
                host_info["username"],
                host_info["mac_address"],
                host_info["cpu_id"],
                host_info["python_version"],
                host_info["os_info"],
                identifier_code if identifier_code else "N/A",
                is_activated,
                system_uuid_path,
                system_uuid_content,
                host_uuid_path,
                host_uuid_content,
                project_number_id
            )

            cursor.execute(insert_query, values)
            conn.commit()
            return True, is_activated, identifier_code, project_number_id

    except Exception as e:
        logger.error(f"日志记录数据库错误: {e}", exc_info=True)
        return False, 0, None, None
    finally:
        if conn:
            conn.close()


def parse_and_register_project_number(project_path):
    """解析并验证项目编号"""
    conn = None
    try:
        # 尝试从README.md解析项目编号
        project_number, project_name = parse_project_number_from_readme(project_path)
        if not project_number:
            return None, None, None

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查项目编号是否已存在
            check_query = """
            SELECT id FROM project_numbers WHERE project_number = %s
            """
            cursor.execute(check_query, (project_number,))
            result = cursor.fetchone()

            if result:
                project_number_id = result[0]
                # 生成标识符代码
                identifier_code = generate_identifier_code(project_number, project_path)
                return project_number, identifier_code, project_number_id
            else:
                # 项目编号在数据库中不存在
                return project_number, None, None

    except Exception as e:
        logger.error(f"Error validating project number: {e}", exc_info=True)
        return None, None, None
    finally:
        if conn:
            conn.close()


def validate_identifiers(host_id, project_uuid, current_project_path, system_uuid_path, host_uuid_path):
    """验证系统标识和主机标识是否匹配数据库记录"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT system_uuid_file_path, system_uuid_content, host_uuid_content
                FROM project_launch_logs
                WHERE project_uuid = %s
                  AND host_id = %s
                LIMIT 1
                """
            cursor.execute(query, (project_uuid, host_id))
            result = cursor.fetchone()

            if not result:
                return False

            stored_system_path, stored_system_content, stored_host_content = result

            # 处理相对路径：转换为当前项目下的绝对路径
            if not os.path.isabs(stored_system_path):
                actual_system_path = os.path.join(current_project_path, stored_system_path)
            else:
                actual_system_path = stored_system_path

            # 读取本地文件内容
            current_system_content = read_file_content(actual_system_path)
            current_host_content = read_file_content(host_uuid_path)

            # 验证内容是否匹配
            system_match = stored_system_content == current_system_content
            host_match = stored_host_content == current_host_content

            return system_match and host_match

    except Exception as e:
        logger.error(f"Identifier validation error: {e}")
        return False
    finally:
        if conn:
            conn.close()


def check_activation_status(project_uuid):
    """检查项目是否已激活"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT is_activated
            FROM project_launch_logs
            WHERE project_uuid = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(query, (project_uuid,))
            result = cursor.fetchone()
            return result[0] if result else False
    except Exception as e:
        logger.error(f"Error checking activation status: {e}")
        return False
    finally:
        if conn:
            conn.close()


def has_host_changed(host_id, project_uuid):
    """
    检查主机特征是否有变化：
    1. 项目首次运行：默认为有变化
    2. 数据库中不存在相同主机ID：有变化
    3. 存在相同主机ID但特征不同：有变化
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查该项目是否有历史记录
            query = """
            SELECT host_id, MIN(first_launch_time) as first_time
            FROM project_launch_logs
            WHERE project_uuid = %s
            GROUP BY host_id
            """
            cursor.execute(query, (project_uuid,))
            results = cursor.fetchall()

            # 项目第一次运行
            if not results:
                return True

            # 检查当前主机是否在历史记录中
            host_found = False
            for result in results:
                stored_host_id, first_time = result
                if stored_host_id == host_id:
                    host_found = True
                    break

            # 主机特征已变化
            if not host_found:
                return True

            return False  # 主机特征未变化

    except Exception as e:
        logger.error(f"Host change check database error: {e}")
        return True
    finally:
        if conn:
            conn.close()
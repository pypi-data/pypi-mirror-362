from typing import Optional, Union

from pydantic import BaseModel, Field
from ..model.enums import UserStatus, UserGender
from ..lib import time as time_lib


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # mongodb主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class AuthUser(BaseData):
    """
    用户鉴权模型
    """
    # 用户id
    id: Optional[int] = None
    # 用户编号
    user_id: Optional[str] = None
    # 用户账号
    account: Optional[str] = None
    # 用户昵称
    nickname: Optional[str] = None
    # 头像
    avatar: Optional[str] = None
    # 用户性别:[1=男,2=女,3=保密]
    gender: Optional[int] = 3
    # 手机号码
    mobile: Optional[str] = None
    # 手机状态:[0=未绑定,1=已绑定未验证,2=已验证]
    mobile_status: Optional[int] = 0
    # 电子邮箱
    email: Optional[str] = None
    # 邮箱状态:[0=未绑定,1=已绑定未验证,2=已验证]
    email_status: Optional[int] = 0
    # 是否禁用: [0=否, 1=是]
    is_disable: Optional[int] = 0
    # 是否删除: [0=否, 1=是]
    is_delete: Optional[int] = 0
    # 创建时间
    create_time: Optional[int] = 0
    # 更新时间
    update_time: Optional[int] = 0
    # 删除时间
    delete_time: Optional[int] = 0
    # 团队主键,团队编号
    team_id: Optional[str] = None
    # 是否团队管理员,[1=是,0=否]
    is_team_admin: Optional[int] = 0
    # 最后一次登录token
    token: Optional[str] = None
    # 团队名称
    team_name: Optional[str] = None
    # 团队简称
    team_nick_name: Optional[str] = None
    # 团队头像
    team_avatar: Optional[str] = None
    # 团队最大成员数
    max_member_count: Optional[int] = None
    # 团队当前成员数
    current_member_count: Optional[int] = None
    # 团队最大SKU数
    max_sku_count: Optional[int] = None
    # 团队当前SKU数
    current_sku_count: Optional[int] = None
    # 批量导入SKU数量限制
    batch_size_limit: Optional[int] = None
    # 团队状态:[1=正常,0=禁用]
    team_status: Optional[int] = 1

    def to_log(self):
        return f'{self.nickname}({self.account})'


class AuthApp(BaseData):
    # 唯一id，一个团队可以有多个token
    token: Optional[str] = None
    # 团队状态:[1=正常,0=禁用]
    team_status: Optional[int] = 1
    # 团队主键,团队编号
    team_id: Optional[str] = None
    # 团队名称
    team_name: Optional[str] = None
    # 团队简称
    team_nick_name: Optional[str] = None
    # 创建时间
    create_time: Optional[int] = 0
    # 更新时间
    update_time: Optional[int] = 0
    # 删除时间
    delete_time: Optional[int] = 0
    # 是否禁用: [0=否, 1=是]
    is_disable: Optional[int] = 0
    # 是否删除: [0=否, 1=是]
    is_delete: Optional[int] = 0


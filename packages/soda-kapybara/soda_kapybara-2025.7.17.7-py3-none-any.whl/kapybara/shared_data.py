from pydantic import BaseModel
import threading

shared_data = threading.local()

class HealthDocumentData(BaseModel):
    """
    档案数据
    """

    sbp: str  # 收缩压
    dbp: str  # 舒张压
    height: str  # 身高
    weight: str  # 体重
    waistline: str  # 腰围
    eat_amount: str  # 主食量
    exercise_count: int  # 运动次数
    exercise_duration: int  # 运动时间
    daily_smoke_amount: int  # 日吸烟量
    daily_drink_amount: int = 0  # 日饮酒量
    salt: str  # 摄盐情况
    diease_history: str  # 疾病史


class FollowUpData(BaseModel):
    """
    随访数据
    """

    sbp: str  # 收缩压
    dbp: str  # 舒张压
    FBG: str  # 空腹血糖
    heart_rate: str  # 心率
    PBG: str  # 餐后血糖
    glycosylated_hemoglobin: str  # 糖化血红蛋白
    weight: str  # 体重
    height: str  # 身高


class HealthCheckData(BaseModel):
    """
    体检数据
    """

    FBG: str  # 空腹血糖
    glycosylated_hemoglobin: str  # 糖化血红蛋白
    waistline: str  # 腰围

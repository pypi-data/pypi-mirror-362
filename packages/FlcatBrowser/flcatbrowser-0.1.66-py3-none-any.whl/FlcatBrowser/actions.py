import random
import time
from enum import Enum
from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.common import Keys
from .utils import clipboard as cb
from typing import List
import loguru
import random
class ActionsConfig:
    def __init__(self, action_speed_ratio = 1, get_need_wait = None):
        self.action_speed_ratio = action_speed_ratio
        self.get_need_wait = get_need_wait

default_config = ActionsConfig()

import random
import loguru  # 假设你正在使用loguru，如果没有，可以替换为print或标准logging

def get_random_offset(element, min_x_offset=None, max_x_offset=None, min_y_offset=None, max_y_offset=None):
    """
    返回元素相对于自身左上角的随机偏移量。
    对于尺寸足够大的元素（默认>=40px），随机点将优先选择在中心的50%区域内，以提高点击稳定性。

    参数:
        element: 目标元素，需要包含位置信息。
        min_x_offset (int, optional): x轴最小偏移量。如果提供，将覆盖默认逻辑。
        max_x_offset (int, optional): x轴最大偏移量。如果提供，将覆盖默认逻辑。
        min_y_offset (int, optional): y轴最小偏移量。如果提供，将覆盖默认逻辑。
        max_y_offset (int, optional): y轴最大偏移量。如果提供，将覆盖默认逻辑。

    返回:
        tuple: 格式为(x_offset, y_offset)的随机偏移量元组。
    
    异常:
        ValueError: 如果元素没有位置信息或尺寸过小无法计算偏移。
    """
    # 检查元素是否有位置信息
    if not hasattr(element, 'states') or not element.states.has_rect:
        raise ValueError("元素没有位置信息，无法计算偏移量")

    left_top, right_top, right_bottom, left_bottom = element.states.has_rect
    # 计算元素的宽度和高度
    width = right_top[0] - left_top[0]
    height = left_bottom[1] - left_top[1]

    # 定义常量，方便调整
    MIN_SIZE_FOR_CENTER_BIAS = 15  # 元素尺寸大于此值时，启用中心50%偏好
    SAFE_PADDING = 5               # 距离边缘的最小安全距离

    # --- X轴偏移量计算 ---
    
    # 1. 根据元素宽度确定默认的偏移范围
    if width >= MIN_SIZE_FOR_CENTER_BIAS:
        # 尺寸足够大，默认范围为中心50%
        default_min_x = width * 0.25
        default_max_x = width * 0.75
    else:
        # 尺寸较小，使用安全边距作为默认范围
        default_min_x = SAFE_PADDING
        default_max_x = width - SAFE_PADDING

    # 2. 应用用户指定的偏移量（如果提供）
    final_min_x = min_x_offset if min_x_offset is not None else default_min_x
    final_max_x = max_x_offset if max_x_offset is not None else default_max_x

    # 3. 校准最终范围，确保其在安全边界内
    final_min_x = max(SAFE_PADDING, final_min_x)
    final_max_x = min(width - SAFE_PADDING, final_max_x)

    # 4. 处理边界情况：如果最小偏移大于最大偏移（可能因元素过小或用户输入不当）
    if final_min_x > final_max_x:
        # 将偏移量固定在元素中心，避免random.randint报错
        final_min_x = final_max_x = width / 2
        
    # --- Y轴偏移量计算 (逻辑同X轴) ---

    # 1. 根据元素高度确定默认的偏移范围
    if height >= MIN_SIZE_FOR_CENTER_BIAS:
        default_min_y = height * 0.25
        default_max_y = height * 0.75
    else:
        default_min_y = SAFE_PADDING
        default_max_y = height - SAFE_PADDING

    # 2. 应用用户指定的偏移量
    final_min_y = min_y_offset if min_y_offset is not None else default_min_y
    final_max_y = max_y_offset if max_y_offset is not None else default_max_y

    # 3. 校准最终范围
    final_min_y = max(SAFE_PADDING, final_min_y)
    final_max_y = min(height - SAFE_PADDING, final_max_y)

    # 4. 处理边界情况
    if final_min_y > final_max_y:
        final_min_y = final_max_y = height / 2

    # --- 生成随机偏移量 ---
    loguru.logger.info(
        f"元素名称: {element}, 尺寸: ({width}, {height}), "
        f"X偏移范围: ({int(final_min_x)}, {int(final_max_x)}), "
        f"Y偏移范围: ({int(final_min_y)}, {int(final_max_y)})"
    )
    
    # 确保范围是有效的整数
    if int(final_min_x) > int(final_max_x) or int(final_min_y) > int(final_max_y):
        raise ValueError(f"无法为尺寸为({width}, {height})的元素生成有效的偏移范围。")
        
    x_offset = random.randint(int(final_min_x), int(final_max_x))
    y_offset = random.randint(int(final_min_y), int(final_max_y))
    
    return x_offset, y_offset

# 最后的bool表示是否应用action_speed_ratio
class SleepTime(Enum):
    MOUSE_RELEASE = (0.1, 0.2, False)
    KEY_RELEASE = (0.05, 0.1, False)
    KEY_INTERVAL = (0.03, 0.05, False)
    KEY_DOWN = (0.05, 0.1, False)
    HUMAN_THINK = (0.2, 2, True)
    WAIT_PAGE = (1, 1.5, True)
    NONE_OPERATION = (1, 5, True)
    DELETE_TEXT = (5, 10, True)

def sleep(sleep_time: SleepTime, config: ActionsConfig):
    if sleep_time.value[2]:
        time.sleep(random.uniform(sleep_time.value[0], sleep_time.value[1]) * config.action_speed_ratio)
    else:
        time.sleep(random.uniform(sleep_time.value[0], sleep_time.value[1]))

def move_to(tab: MixTab, ele_or_loc, timeout=3, offset_x: float = 0, offset_y: float = 0, min_x_offset=None, max_x_offset=None, min_y_offset=None, max_y_offset=None, config: ActionsConfig = default_config):
    if config.get_need_wait and config.get_need_wait():
        while config.get_need_wait and config.get_need_wait():
            time.sleep(0.1)
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    if isinstance(ele_or_loc, (tuple, list)):
        return act.move_to(ele_or_loc, offset_x=offset_x, offset_y=offset_y)
    elif offset_x == 0 and offset_y == 0:
        # 如果没有指定偏移量，则获取随机偏移量
        offset_x, offset_y = get_random_offset(tab.ele(ele_or_loc, timeout=timeout),  min_x_offset=min_x_offset, max_x_offset=max_x_offset, min_y_offset=min_y_offset, max_y_offset=max_y_offset)
    
    # 打印窗口信息
    loguru.logger.info(f'[窗口信息] rect.viewport_size: {tab.rect.viewport_size}')
    
    return act.move_to(ele_or_loc, offset_x=offset_x, offset_y=offset_y)

def click(tab: MixTab, ele_or_loc, more_real=True, act_click=False, timeout=3, offset_x: float = 0, offset_y: float = 0, min_x_offset=None, max_x_offset=None, min_y_offset=None, max_y_offset=None, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    if more_real:
        sleep(SleepTime.HUMAN_THINK, config=config)
        if act_click:
            act.click(ele_or_loc, timeout=timeout)
        else:
            move_to(tab, ele_or_loc, offset_x=offset_x, offset_y=offset_y, min_x_offset=min_x_offset, max_x_offset=max_x_offset, min_y_offset=min_y_offset, max_y_offset=max_y_offset, config=config).hold()
            sleep(SleepTime.MOUSE_RELEASE, config=config)
            act.release()
    else:
        raise NotImplementedError("为避免意外不支持非模拟人类方式")
        # tab.ele(ele_or_loc, timeout=timeout).click()
        
    sleep(SleepTime.WAIT_PAGE, config=config)
    
def hold(tab: MixTab, ele_or_loc, more_real=True, act_click=False, timeout=3, offset_x: float = 0, offset_y: float = 0, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    if more_real:
        sleep(SleepTime.HUMAN_THINK, config=config)
    else:
        raise NotImplementedError("为避免意外不支持非模拟人类方式")
    if act_click:
        act.hold(ele_or_loc)
    else:
        move_to(tab, ele_or_loc, offset_x=offset_x, offset_y=offset_y, config=config).hold()
        
    sleep(SleepTime.WAIT_PAGE, config=config)
    
def release(tab: MixTab, config: ActionsConfig = default_config):
    act = tab.actions
    act.release()
    sleep(SleepTime.WAIT_PAGE, config=config)

def type_message_to_shift_and_enter(message: str):
    tem_messages = message.split('\n')
    messages = []
    shift_and_enter = (Keys.SHIFT, Keys.ENTER)
    for message in tem_messages:
        messages.append(message)
        messages.append(shift_and_enter)
    return messages

def _get_ele_text(tab: MixTab, ele_or_loc, timeout=3):
    text = tab.ele(ele_or_loc, timeout=timeout).text
    if not text:
        text = tab.ele(ele_or_loc, timeout=timeout).value
    return text

def type(tab: MixTab, ele_or_loc, message: str, more_real=True, timeout=3, config=default_config, assist_ele=None):
    act = tab.actions
    sleep(SleepTime.HUMAN_THINK, config=config)
    if not message:
        return
    
    if ele_or_loc and not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    if more_real:
        if ele_or_loc:
            click(tab, ele_or_loc, timeout=timeout, config=config, more_real=more_real)
        _paste(tab, message, config=config)
        if not assist_ele:
            assist_ele = ele_or_loc
        if assist_ele and not isinstance(assist_ele, (tuple, list)):
            text = _get_ele_text(tab, assist_ele, timeout=timeout)
            if len(text) == 0:
                _paste(tab, message, config=config)
                text = _get_ele_text(tab, assist_ele, timeout=timeout)
                if len(text) == 0:
                    raise ValueError(f"输入框内容不一致，输入内容：{message}，实际内容：{text}")
    else:
        raise NotImplementedError("为避免意外不支持非模拟人类输入方式")
        # # 避免末尾回车触发发送
        # if not ele_or_loc:
        #     act.type(message.rstrip())
        # else:
        #     tab.ele(ele_or_loc, timeout=timeout).input(message.rstrip())
                
        
    sleep(SleepTime.WAIT_PAGE, config=config)

def _paste(tab: MixTab, message, config=default_config):
    act = tab.actions
    for i in range(3):
        try:
            tab.actions.key_down(Keys.CTRL)
            sleep(SleepTime.KEY_INTERVAL, config=config)
            tab.actions.key_down('a')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up('a')
            sleep(SleepTime.KEY_INTERVAL, config=config)
            tab.actions.key_up(Keys.CTRL)
            data = cb.save_clipboard()
            # 避免末尾回车触发发送
            cb.set_clipboard_universal(message.rstrip(), 'text')
            tab.actions.key_down(Keys.CTRL)
            sleep(SleepTime.KEY_INTERVAL, config=config)
            tab.actions.key_down('v')
            sleep(SleepTime.KEY_RELEASE, config=config)
            tab.actions.key_up('v')
            sleep(SleepTime.KEY_INTERVAL, config=config)
            tab.actions.key_up(Keys.CTRL)
            cb.restore_clipboard(data)
            break
        except Exception as e:
            loguru.logger.exception(e)
            
    
def type_and_send(tab: MixTab, ele_or_loc, messages: List[str], more_real=True, timeout=3, config=default_config, assist_ele=None):
    act = tab.actions
    sleep(SleepTime.HUMAN_THINK, config=config)
    first=False
    # 没有指定元素，则直接模拟键盘输入，不点击元素
    if ele_or_loc and not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    if more_real:
        if ele_or_loc:
            click(tab, ele_or_loc, timeout=timeout, config=config, more_real=more_real)
    else:
        raise NotImplementedError("为避免意外不支持非模拟人类方式")
    for message in messages:
        if not message:
            continue
        if more_real:
            if not first:
                first=True
            _paste(tab, message, config=config)
        else:
            raise NotImplementedError("为避免意外不支持非模拟人类输入方式")
            # # 避免末尾回车触发发送
            # if not ele_or_loc:
            #     act.type(message.rstrip())
            # else:
            #     tab.ele(ele_or_loc, timeout=timeout).input(message.rstrip())

        sleep(SleepTime.WAIT_PAGE, config=config)
        if not assist_ele:
            assist_ele = ele_or_loc
        if assist_ele and not isinstance(assist_ele, (tuple, list)):
            text = _get_ele_text(tab, assist_ele, timeout=timeout)
            if len(text) == 0:
                _paste(tab, message, config=config)
                text = _get_ele_text(tab, assist_ele, timeout=timeout)
                if len(text) == 0:
                    raise ValueError(f"输入框内容不一致，输入内容：{message}，实际内容：{text}")
        send_key(tab, Keys.ENTER, config=config)

def send_key(tab: MixTab, key: Keys, config: ActionsConfig = default_config):
    act = tab.actions
    act.key_down(key)
    sleep(SleepTime.KEY_RELEASE, config=config)
    act.key_up(key)
    sleep(SleepTime.WAIT_PAGE, config=config)

def scroll(tab: MixTab, ele_or_loc, delta_y, delta_x, timeout=3, config: ActionsConfig = default_config):
    if not isinstance(ele_or_loc, (tuple, list)):
        ele_or_loc = tab.ele(ele_or_loc, timeout=timeout)
    act = tab.actions
    move_to(tab,ele_or_loc, config=config)
    act.scroll(delta_y, delta_x)

def simulated_human(tab: MixTab, config: ActionsConfig = default_config):
    try:
        act = tab.actions
        # 1. 随机移动鼠标
        width, height = tab.rect.size
        x = random.randint(0, width)
        y = random.randint(0, height)
        act.move_to((x, y))
        
        # 模拟人类在移动完鼠标后略作停顿
        sleep(SleepTime.HUMAN_THINK, config=config)

        # 2. 随机决定是否进行滚轮滚动
        if random.random() < 0.6:  # 60% 的概率进行滚动操作
            # 滚动距离可以是向上或向下
            # delta_y 向下滚动为正，向上滚动为负
            delta_y = random.randint(-300, 300)  
            # 如果需要横向滚动，可设置 delta_x
            delta_x = 0  

            act.scroll(delta_y=delta_y, delta_x=delta_x)

            # 停顿一小段时间，模拟卷动后的停顿或浏览
            sleep(SleepTime.HUMAN_THINK, config=config)

        # 3. 随机等待，模拟人与人差异
        sleep(SleepTime.NONE_OPERATION, config=config)
    except Exception:
        pass

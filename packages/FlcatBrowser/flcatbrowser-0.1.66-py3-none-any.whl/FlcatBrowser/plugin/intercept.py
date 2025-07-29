import base64
from DrissionPage import Chromium
from DrissionPage._base.driver import Driver
from DrissionPage._pages.mix_tab import MixTab
import loguru

class Intercept:
    def get_intercept_patterns(self):
        return [
                    # {
                    #     'urlPattern': '*://www.genspark.ai/api/copilot/ask*',  # 精确拦截目标请求
                    #     'resourceType': 'XHR',  # XHR 请求（AJAX 请求）
                    #     'interceptionStage': 'Request'
                    # },
                    # {
                    #     'urlPattern': '*',  # 精确拦截目标请求
                    #     'interceptionStage': 'Request'
                    # },
                    {
                        'urlPattern': '*://www.genspark.ai/_nuxt/*',  # 拦截目标 JS 文件
                        'resourceType': 'Script',
                        'interceptionStage': 'HeadersReceived',  # 在接收到响应头后拦截
                    }
                ]

    def __init__(self,tab: MixTab, chromium: Chromium):
        self.tab=tab
        self.chromium = chromium

        self._target_id = self.tab.tab_id
        self.address=self.chromium.address
        self._driver = Driver(self._target_id, "page", self.address)
        self._driver.run("Network.enable")
        self._driver.run("Network.setRequestInterception",
                patterns = self.get_intercept_patterns()
            )

        self._driver.set_callback("Network.requestIntercepted", self.route)
        self.current_user_agent = None  # 当前使用的 User-Agent
        self.user_agent_timestamp = 0  # 当前 User-Agent 的时间戳

    def route(self, **kwargs):
        try:
            # 判断是否已经拿到响应头
            if 'responseHeaders' in kwargs:
                # 这是 HeadersReceived 阶段
                self.handle_headers_received(**kwargs)
            else:
                # 否则就是 Request 阶段
                self.handle_request(**kwargs)
        finally:
            self._driver.run('Network.continueInterceptedRequest', interceptionId=kwargs['interceptionId'])


    def handle_headers_received(self, **kwargs):
        resource_type = kwargs['resourceType']
        if resource_type == 'Script':
            self.recaptcure_utils_intercepted(**kwargs)

    def handle_request(self, **kwargs):
        url = kwargs['request']['url']
        resource_type = kwargs['resourceType']
        # 如果 URL 匹配排除规则，直接放行
        # cf 5秒盾牌
        # if "cdn-cgi/challenge-platform" in url:
        #     self._driver.run('Network.continueInterceptedRequest', interceptionId=kwargs['interceptionId'])
        #     return
        
        # if resource_type == 'XHR' and resource_type != 'Script':
        #     self.ask_request_intercepted(**kwargs)
                # elif 'www.genspark.ai/api/copilot/ask' in url:
        #     self.ask_request_intercepted(**kwargs)

    def ask_request_intercepted(self, **kwargs):
        url = kwargs['request']['url']
        # print(f"拦截到请求：{url}")
        headers = kwargs['request']['headers']

        # 随机设置 User-Agent
        headers['User-Agent'] = self._get_random_user_agent()
        # print(f"拦截到请求：{url}，使用 User-Agent: {headers['User-Agent']}")
        # post_data_entries = kwargs['request']['postDataEntries']

        # modified_entries = []
        # modified_data = None
        # for entry in post_data_entries:
        #     # Base64 解码
        #     decoded_data = base64.b64decode(entry.get('bytes')).decode('utf-8')
            
        #     # 尝试解析 JSON 数据
        #     try:
        #         json_data = json.loads(decoded_data)
        #         loguru.logger.debug(f"解码后的数据：{json_data}")

        #         # 修改内容
        #         json_data['messages'][0]['content'] = '为什么太阳是圆的'
        #         json_data['user_s_input'] = '为什么太阳是圆的'

        #         # JSON 转字符串并重新 Base64 编码
        #         modified_data = json.dumps(json_data)
        #         encoded_data = base64.b64encode(modified_data.encode('utf-8')).decode('utf-8')
        #     except json.JSONDecodeError:
        #         # 如果解析失败，保留原数据
        #         encoded_data = entry.get('bytes')

        #     modified_entries.append({'bytes': encoded_data})

        # 发送修改后的请求
        self._driver.run('Network.continueInterceptedRequest', 
            interceptionId=kwargs['interceptionId'],
            # headers=headers
            # postDataEntries=modified_entries,
            # postData=modified_data
        )

    def recaptcure_utils_intercepted(self,**kwargs):
        interception_id = kwargs['interceptionId']
        # 只在请求的响应头被接收后才能获取响应体
        body = self._driver.run("Network.getResponseBodyForInterception",
                                interceptionId=interception_id)
        try:
            if kwargs.get('responseHeaders') and body['base64Encoded']:
                content = base64.b64decode(body['body']).decode('utf-8')
                find_content = 'async function i(s){await o.callHook("app:error",s),o.payload.error=o.payload.error||xg(s)}r.config.errorHandler=i;try{await DY(o,ywe)}catch(s){i(s)}try{await o.hooks.callHook("app:created",r),await o.hooks.callHook("app:beforeMount",r),r.mount(TY),await o.hooks.callHook("app:mounted",r),await Pt()}catch(s){i(s)}return r.config.errorHandler===i&&(r.config.errorHandler=void 0),r},e=WA().catch(t=>{throw console.error("Error while mounting app:",t),t})'
                if content.find(find_content) != -1:
                    loguru.logger.debug("recaptcure_utils初始化成功")
                    content = content.replace(find_content, f"{find_content};window.I=JS;")
                # 构造完整的 HTTP 响应
                    http_response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/javascript; charset=UTF-8\r\n"
                        f"Content-Length: {len(content.encode('utf-8'))}\r\n"
                        "Connection: keep-alive\r\n"
                        "\r\n"
                        f"{content}"
                    )
                    
                    # Base64 编码完整的 HTTP 响应
                    res = base64.b64encode(http_response.encode('utf-8')).decode('utf-8')

                    self._driver.run("Network.continueInterceptedRequest",
                                    interceptionId=interception_id,
                                    rawResponse=res)
                else:
                    self._driver.run("Network.continueInterceptedRequest",
                                    interceptionId=interception_id,
                                    )  # 确保这里是你想要的内容
        except Exception as e:
            pass

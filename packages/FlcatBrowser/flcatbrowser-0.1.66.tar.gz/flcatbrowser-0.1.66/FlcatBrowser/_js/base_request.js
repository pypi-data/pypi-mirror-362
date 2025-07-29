// let arguments= []
// arguments[0] = "cf_test"
// arguments[1] = 1
// arguments[2] = {
// }

let request_name = arguments[0]
let id = arguments[1]
let args = arguments[2]

let utils = {
  // 'g_recaptcha_token' = await utils.getRecaptchaToken("xxx")
  getRecaptchaToken: window.I ? window.I.getRecaptchaToken : null
}

function processEventStreamDataToJsonArray(data){
    try {
        // 将原始字符串按行分割
        const lines = data.split("\n").filter(line => line.trim() !== "");
        
        // 将每一行 JSON 解析为对象
        const jsonArray = lines.map(line => JSON.parse(line));
        return jsonArray
      } catch (error) {
        console.error("解析失败:", error.stack);
      }
}

async function processEventStream(response) {
    let reader;
    try {
      // 如果 HTTP 状态码非 2xx，则主动抛错
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }
  
      // 检查响应 body 是否存在（部分环境下可能为空）
      if (!response.body) {
        throw new Error('ReadableStream not supported or response body is empty.');
      }
  
      // 2. 从 response 里获取可读流 (ReadableStream)
      reader = response.body.getReader();
    } catch (error) {
      console.error('网络请求或响应初始化出现错误:', error);
      // 可以根据业务需求决定是否在此 return 或做其他处理
      return;
    }
  
    // 用于将二进制数据解码成字符串
    const decoder = new TextDecoder('utf-8');
    let buffer = ''; // 缓存前一次循环遗留的未处理文本
    let fullText = ''
  
    try {
      while (true) {
        // 3. 逐块读取
        const { done, value } = await reader.read();
        if (done) {
        // No more data. Stream finished.
          break;
        }
  
        // 4. 解码本次接收的二进制数据
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
  
        // 5. 解析 SSE 格式数据（或其他需要的逻辑）
        const lines = buffer.split('\n');
        // 最后一行可能是不完整的数据，暂存到 buffer，等待下次拼接
        buffer = lines.pop() || '';
  
        for (let line of lines) {
          if (line.startsWith('data:')) {
            const data = line.slice(5).trim();
            fullText += data + '\n'
            // console.log('Received data:', data);
            // 若确定返回的是 JSON，可用 JSON.parse
            // try {
            //   const parsedData = JSON.parse(data);
            //   console.log('Parsed data:', parsedData);
            // } catch (parseErr) {
            //   console.error('JSON parse error:', parseErr);
            // }
          }
        }
      }
    } catch (error) {
      console.error('流读取或解析过程中出现错误:', error);
      // 在此根据业务需求决定如何处理
    } finally {
      // 如果需要，在此处进行必要的善后处理，例如关闭 reader
      if (reader) {
        try {
          await reader.cancel();
        } catch (cancelErr) {
          console.error('Reader.cancel() 失败:', cancelErr);
        }
      }
    }

    return fullText
}

let my_request = {
    cf_test: async function (){
        return await fetch(`https://cf_test.flcat-test.top/`, {
          method: 'GET'
        });
    },
    ...custom_request
}

async function run(){
    try {
        const res = await my_request[request_name](args);

        // 检查响应是否成功 (200-299)
        if (!res.ok) {
            console.log(JSON.stringify({
                type: 'request',
                id: id,
                data: {
                    code: res.status,
                    message: res.statusText,
                    data: await res.text()
                }
            }));
            return
        }
        let data;
        const contentType = res.headers?.get('Content-Type');
        if (contentType?.includes('text/event-stream')) {
            data = processEventStreamDataToJsonArray(await processEventStream(res))
        } else {
            // 解析响应体（处理 JSON 解析失败或为空的情况）
            try {
                data = await res.json();
            } catch (error) {
                data = null; // 如果解析失败，将数据设置为 null
            }
        }
        console.log(JSON.stringify({
            type: 'request',
            id: id,
            data: {
                code: res.status,
                message: res.statusText,
                data: data
            }
        }));
    } catch (err) {
        // 捕获网络错误
        console.log(JSON.stringify({
            type: 'request',
            id: id,
            data: {
                code: undefined,
                message: err.stack,
                data: undefined
            }
        }));
    }
}
run()
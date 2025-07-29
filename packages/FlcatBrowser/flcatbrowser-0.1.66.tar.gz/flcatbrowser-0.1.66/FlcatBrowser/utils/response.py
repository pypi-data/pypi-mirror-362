def print_response_detail(response):
    # 打印详细信息
    print("状态码:", response.status_code)
    print("响应头部信息:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\n响应内容:")
    print(response.text)

    print("\nJSON解析后的内容:")
    try:
        print(response.json())
    except ValueError:
        print("响应内容不是JSON格式。")
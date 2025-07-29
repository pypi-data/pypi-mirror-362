import random
import time
import requests
import json
import tiktoken
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

# 配置参数
API_URL = "http://gpus.dev.cyberspike.top:8000/v1/chat/completions"
MODEL_NAME = "al-1s-20250421/"
TEST_ROUNDS = 1000  # 测试轮次
MAX_WORKERS = 20  # 并发线程数

# 创建编码器（根据实际情况调整模型名称）
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")


def generate_complex_prompt():
    """生成复杂的网络安全相关prompt"""
    return str(random.choice(open('topic.dataset.txt', 'r', encoding='utf-8').readlines())).strip()


def count_tokens(text):
    """计算文本的token数量"""
    return len(enc.encode(text))


def test_api_call():
    """单次API调用测试"""
    prompt = generate_complex_prompt()
    start_time = time.time()

    try:
        response = requests.post(
            API_URL,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "messages": [{
                    "content": prompt,
                    "role": "user",
                    "name": "user"
                }],
                "model": MODEL_NAME
            }),
            timeout=360
        )

        if response.status_code == 200:
            result = response.json()
            output_text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            token_count = count_tokens(output_text)
            return {
                'success': True,
                'time': time.time() - start_time,
                'token_count': token_count
            }
        else:
            return {'success': False, 'error': f"HTTP {response.status_code}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    total_time = time.time()
    total_tokens = 0
    success_count = 0
    failed_count = 0

    print(f"开始测试，共{TEST_ROUNDS}轮，最大并发{MAX_WORKERS}...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(test_api_call) for _ in range(TEST_ROUNDS)]

        for future in tqdm(futures, desc="Processing API calls", unit="call"):
            result = future.result()
            if result['success']:
                total_tokens += result['token_count']
                success_count += 1
            else:
                failed_count += 1
    total_time = round(time.time() - total_time, 2)
    # 计算指标
    if success_count > 0:
        avg_time_per_call = total_time / success_count
        tokens_per_second = total_tokens / total_time
        rpm = (success_count / total_time) * 60

        print("\n--- 测试结果 ---")
        print(f"成功请求: {success_count}/{TEST_ROUNDS}")
        print(f"失败请求: {failed_count}")
        print(f"平均响应时间: {avg_time_per_call:.2f}秒/次")
        print(f"总生成token数: {total_tokens}")
        print(f"平均token速度: {tokens_per_second:.2f} tokens/秒")
        print(f"吞吐量: {rpm:.2f} 次/分钟")
    else:
        print("所有请求均失败，请检查API服务状态")


if __name__ == "__main__":
    main()

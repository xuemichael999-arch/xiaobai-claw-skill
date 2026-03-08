#!/usr/bin/env python3
import sys
import requests
import json

import os
API_KEY = os.getenv("FUSION_API_KEY")
API_URL = "https://open.feedcoopapi.com/search_api/web_search"

def main():
    import argparse
    if not API_KEY:
        print("请先配置火山引擎融合搜索API密钥：")
        print("export FUSION_API_KEY=\"你的火山引擎融合搜索API密钥\"")
        print("密钥获取方式：开通火山引擎融合信息搜索服务后在控制台获取")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="火山引擎融合信息搜索工具")
    parser.add_argument("query", help="查询问题", nargs="+")
    parser.add_argument("--site", help="指定搜索站点", default="")
    parser.add_argument("--industry", help="指定行业分类", default="")
    args = parser.parse_args()
    
    query = " ".join(args.query)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "query": query,
        "SearchType": "web",
        "Count": 15,
        "TimeRange": "OneMonth",
        "Site": args.site,
        "Industry": args.industry
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        print("="*50)
        print("搜索结果:")
        print("="*50)
        
        # 兼容返回结构
        if isinstance(result, dict):
            if "answer" in result:
                print(result["answer"])
            elif "data" in result and "answer" in result["data"]:
                print(result["data"]["answer"])
            elif "result" in result:
                print(result["result"])
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(response.text[:2000])
            
        print("\n")
            
    except Exception as e:
        print(f"调用API出错: {str(e)}")
        # 打印响应详情方便调试
        if 'response' in locals():
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text[:1000]}")

if __name__ == "__main__":
    main()
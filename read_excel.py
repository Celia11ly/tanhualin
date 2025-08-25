#!/usr/bin/env python3
import pandas as pd
import json
import os

def read_excel_to_json(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return json.dumps({"error": f"文件不存在: {file_path}"})
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 转换为JSON
        result = df.to_json(orient='records', force_ascii=False)
        return result
    except Exception as e:
        return json.dumps({"error": f"读取文件时出错: {str(e)}"})

if __name__ == "__main__":
    # 读取当前目录下的功能项.xlsx文件
    file_path = os.path.join(os.path.dirname(__file__), "功能项.xlsx")
    json_result = read_excel_to_json(file_path)
    
    # 将结果写入output.json文件
    output_path = os.path.join(os.path.dirname(__file__), "output.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json_result)
    
    print(f"Excel文件内容已转换为JSON并保存到: {output_path}")
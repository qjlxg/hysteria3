import yaml
import requests
import os

def filter_nodes_by_keyword(yaml_url, keyword):
    try:
        response = requests.get(yaml_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"请求 {yaml_url} 失败：{e}")
        return []
    
    try:
        data = yaml.safe_load(response.content)
    except yaml.YAMLError as e:
        print(f"YAML 解析失败：{e}")
        return []
    
    if not isinstance(data, dict) or 'proxies' not in data:
        print(f"文件 {yaml_url} 缺少 'proxies' 字段")
        return []
    
    filtered_nodes = []
    for node in data['proxies']:
        node_name = node.get('name', '')
        if keyword in node_name:
            filtered_nodes.append(node)
    return filtered_nodes

def deduplicate_nodes_by_name(nodes):
    seen_names = set()
    unique_nodes = []
    for node in nodes:
        name = node.get('name', '')
        if name and name not in seen_names:
            seen_names.add(name)
            unique_nodes.append(node)
    return unique_nodes

def main():
    yaml_urls = [
        'https://raw.githubusercontent.com/qjlxg/aggregator/main/data/clash.yaml',
      
    ]
    keyword = '美'
    
    all_filtered_nodes = []
    for yaml_url in yaml_urls:
        filtered_nodes = filter_nodes_by_keyword(yaml_url, keyword)
        all_filtered_nodes.extend(filtered_nodes)
    
    unique_nodes = deduplicate_nodes_by_name(all_filtered_nodes)
    
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'aggregated_proxies.yaml')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'proxies': unique_nodes}, f, allow_unicode=True)
    
    print(f"已过滤并去重 {len(unique_nodes)} 个节点，保存到 {output_file}")

if __name__ == '__main__':
    main()

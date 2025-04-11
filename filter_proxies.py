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
 'https://sub.521177.xyz/Jay',
 'https://emm-7zy.pages.dev/CSDN',
 'https://sub.vip.sd/JPa6vvFgygVtNP2sGJ2r/download/YuanZhang',
 'https://dy11.baipiaoyes.com/api/v1/client/subscribe?token=51afccb0e19f977d2d6c73f0b71a53b1',
 'https://202503212313501.chibaba.ggff.net/api/v1/client/subscribe?token=eee1b58c52d8e656bc6b729a182cf49b',
 'https://xfm.xz61.cn/api/v1/feima/subscribe?token=5bc043e4ec85e6648b1286e913a95387',
 'https://sub.eyujichang.com/api/v1/client/subscribe?token=0c7b2b8bb2e443bd5e86bc3efd66ddbd',
 'https://sub.666676666.xyz/api/v1/client/subscribe?token=ce8487fbcd54181a091015a03d5bd5f4',
 'http://j2s.buzz/v3/subscr?id=2119a8ea90154a2abf12f5eb0425daf7',
 'https://www.yuki-sub.top/api/v1/client/subscribe?token=95cd2c27fe4e94ee01b3495d7bf2a784',
 'https://msub.fengchiyx.xyz/api/v1/client/subscribe?token=34ff9012ec68f9c521fc559a83146eba',
 'https://link02.qytsub02.pro/api/v1/client/subscribe?token=98966ee683b1723b461b61c5f47b09f7',
 'https://www.ckckssl.top/api/v1/client/subscribe?token=cdc96d354d96b6e6e2670c7611611bdf',
 'http://jdss.hilaotie.me/',
 'https://0s1tn4.dness.top/api/v1/client/subscribe?token=806af1bab2cc27eb02c2cf9ec1e9f7b9',
 'https://4b8kse.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://4iwg7p.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://4j99dr.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://676b5c.whisperingbreeze.cc/api/v1/client/subscribe?token=e253a809d0c1ad3153feb4eb6907e745',
 'https://6yb3xq.dness.top/api/v1/client/subscribe?token=806af1bab2cc27eb02c2cf9ec1e9f7b9',
 'https://9lkyfh.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://anft4s.cluobotu.xyz/api/v1/client/subscribe?token=8dd1ac6ebbad08764e2514382043ed1b',
 'https://mojie.co/api/v1/client/subscribe?token=21e29de55733e92dbb0b0af9f048b294',
 'https://mojie.me/api/v1/client/subscribe?token=f9e62e795205eb264f8d34ae2281bade',
 'https://mojie.app/api/v1/client/subscribe?token=ce77d629eb0bcea28739ffefa5620218',
 'https://mojie.app/api/v1/client/subscribe?token=6dbf0b92279e3ca9448b883496d8870f',
 'https://onlysub.mjurl.com/api/v1/client/subscribe?token=6dbf0b92279e3ca9448b883496d8870f',
 'https://onlysub.mjurl.com/api/v1/client/subscribe?token=24691c7db62c4214d6e96ff128da0b6f',
 'https://api-hx.02000.net/api/v1/client/subscribe?token=9f44dff9e7a82425fc71e78c9d79fbb1',
 'https://mojie.best/api/v1/client/subscribe?token=7b6ed1c61010e0e4098bf598f9deab9b',
 'https://mojie.app/api/v1/client/subscribe?token=8caa9a9a102ef5c213f8c7e922870a22',
 'https://sub.bxy.org.uk/api/v1/client/subscribe?token=e57e0cae5405ee66d3eb9059a4e7e13a&',
 'https://xship.top/v1/subscribe?starlink=sH-dNCXpq8RiI_PeL6Mr4lMT',
 'https://ts.xship.top/v1/subscribe?starlink=mSIusSz2Ku3YUWxB85cQa',
 'https://xship.top/v1/subscribe?starlink=V3bDL91w89Uh5n65tXawOrHt',
 'https://xship.top/v1/subscribe?starlink=drpkx0fKv4I9AF4j2i2MH2Op',
 'https://xship.top/v1/subscribe?starlink=dqxLsBV3LitAt8Jwux5IRn7m',
 'https://xship.top/v1/subscribe?starlink=Jglkr9T9iNYDipZzxH8nRJhA',
 'https://xship.top/v1/subscribe?starlink=qaKSC44T83EOPpgCSR030vSH',
 'https://xship.top/v1/subscribe?starlink=_RP5WBvhkvkfK72mu4gwgQtv',
 'https://xship.top/v1/subscribe?starlink=smart@vx9RERFgw2WzURK1cQcRYW5K',
 'https://no8-svip.urlapi-dodo.me/s?t=782b4eaaf96ec21c06a481b59beed550#远程订阅组2',
 'https://159.75.130.241/easynet/api/v1/client/subscribe?token=5c77bd133efdcceb5220ffba7d9cc544#远程订阅组 1',
 'https://naiyun0315.xn--8stx8olrwkucjq3b.com/api/v1/client/subscribe?token=8925e615388c763d9cae2206026da702#奈云',
 'https://img.afftruda.com/api/v1/client/subscribe?token=088e57bd9c9f42d01407263cb3ed4d5e#速子云',
 'https://taibai0201.xn--8stx8olrwkucjq3b.com/api/v1/client/subscribe?token=21ac84a01cda936ab265d55efe1c6088#250328',
 'https://cf-workers-sub-9s8.pages.dev/CSDN',
 'https://kawaiifreevpn.pages.dev/90d7db9b-972b-4073-8738-12cf42124260?sub',
 'https://no8-svip.urlapi-dodo.me/s?t=782b4eaaf96ec21c06a481b59beed550',
 'https://xn--z4qtd301ghvk08p.us.kg/',
 'http://216.185.57.210/',
 'http://85.31.235.82:2096/sub/CAA%20Family',
 'https://client-sub.aisu.life/s/f60650781874fde8c396cf156f077bfa',
 'https://client-sub.aisu.life/s/cc94df77c534e0c22541736852db4ca8',
 'https://yaml.51tracking.com',
 'https://diswe.yyuh.me/',
 'https://vless.mhmmddnl.my.id/vless?type=ws&bug=104.22.5.240',
 'https://156.238.251.235/',
 'https://muisgq.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://chromego-sub.netlify.app/sub/merged_proxies_new.yaml',
 'https://fn1.595780.xyz/api/v1/client/subscribe?token=283ba0a08745237e6e1507150261fbac',
 'https://kf2d8j.longonesub.xyz/api/v1/client/subscribe?token=751c31198bdd867e505edac3fb45d01d',
 'https://doone0701.xn--wqr30o34q.xn--io0a7i/api/v1/client/subscribe?token=751c31198bdd867e505edac3fb45d01d',
 'https://xn--cp3a08l.com/api/v1/client/subscribe?token=cfef906df0fcc536603d9d04696a3dfb&flag=meta',
 'https://fz9qin.cluobotu.xyz/api/v1/client/subscribe?token=8dd1ac6ebbad08764e2514382043ed1b',
 'https://vbqrlo.longonesub.xyz/api/v1/client/subscribe?token=751c31198bdd867e505edac3fb45d01d',
 'https://cyberguard.cfd/api/v1/client/subscribe?token=6cbebedaf0f060f5cfef3f432349d840',
 'https://vpn.28.al/s/4920d17bc5f6cda30a465d597cbd1d21',
 'https://speedx2net.postshup.ir:2096/sub/S3VyZFZwbl8zMEdiLDE3NDE0MDkyNzcO4PFMVZoWk',
 'https://img.afftruda.com/api/v1/client/subscribe?token=088e57bd9c9f42d01407263cb3ed4d5e',
 'https://istanbulsydneyhotel.com/blogs/site/sni.php?security=reality',
 'https://naiyun0315.xn--8stx8olrwkucjq3b.com/api/v1/client/subscribe?token=8925e615388c763d9cae2206026da702',
 'https://p2ce09.longonesub.xyz/api/v1/client/subscribe?token=751c31198bdd867e505edac3fb45d01d',
 'https://raw.githubusercontent.com/qjlxg/aggregator/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/aggregator/refs/heads/main/data/clash.yaml',
 'https://raw.githubusercontent.com/qjlxg/YBSubCrawler/refs/heads/main/sub/share/available',
 'https://raw.githubusercontent.com/qjlxg/hysteria3/refs/heads/main/jdss.txt',
 'https://raw.githubusercontent.com/qjlxg/hysteria3/refs/heads/main/minging.txt',
 'https://raw.githubusercontent.com/qjlxg/hysteria3/refs/heads/main/valid_content.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_allv2board/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_dingyue_Center/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_dns68/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_freeVPNjd/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_hack_proxy/refs/heads/main/data/v2ray.txt',
 'https://raw.githubusercontent.com/qjlxg/Mo_jichang_list/refs/heads/main/data/v2ray.txt',
 'https://sqhgq8.babaivip.top/api/v1/client/subscribe?token=0631b0e70e123fd5c1bb9ff2bff2cda6',
 'https://subapi01.qytsublink.com/api/v1/client/subscribe?token=98966ee683b1723b461b61c5f47b09f7',
 'https://taibai0201.xn--8stx8olrwkucjq3b.com/api/v1/client/subscribe?token=21ac84a01cda936ab265d55efe1c608',
 'https://taibai0201.xn--8stx8olrwkucjq3b.com/api/v1/client/subscribe?token=4919dfdeb531db90d8bcb99bd2bc5950',
 'https://tar.l0rd.ir/',
 'https://uthz8n.dness.top/api/v1/client/subscribe?token=806af1bab2cc27eb02c2cf9ec1e9f7b9',
 'https://www.yhc1314dy.link/api/v1/client/subscribe?token=5a6f8390a6e52c6116cbc53212d082c0',
 'https://yx5je8.fluobotu.xyz/api/v1/client/subscribe?token=8dd1ac6ebbad08764e2514382043ed1b',
      
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

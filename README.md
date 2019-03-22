# Fake-Rss
解析rss，使用transmissionrpc发送任务

    fake-rss
    │  server.py
    │  client.py
    │  config.yaml
    │  README.md
    │  
    ├─logs
    │      cache.yaml
    │      
    └─module
            config.py
            item.py
            log.py
            operate.py
            task.py
            trans_api.py
            util.py
            

## 使用方法
### Requirements
    feedparser
    transmissionrpc
    requests
    ruamel.yaml
    python-dateutil
    
### 编辑config.yaml配置文件

    connect:
      headers:                        # 解析种子文件地址时需要加入headers防反爬，格式任意
        User-Agent: ......
        Accept: ......
      transmission:                   # transmission的配置，不需要的参数务必注释掉
        host: localhost
        port: 9091
        user: xxxx
        password: xxxx
        
    schedule:
      path: ./Downloads/Transmission  # 文件默认保存路径
      interval: 3600                  # 请求rss的间隔，单位秒s
      active:                         # 激活的任务
      - Jojo
      - Index
      
    tasks:                            # 除rss外，其余参数均可省略
      Jojo:                           # 示例1
        path: ./Downloads/Transmission/Jojo                 # 保存路径
        rss: https://share.dmhy.org/topics/rss/rss.xml      # rss地址，params参数随rss站点而定
        params:
          keyword: jojo
          team_id: xx
        filter:
          after_time: 2019.1.1        # 该时间之后的条目才会被添加
          keyword: 黄金之风 极影
      Index:                          # 示例2
                                      # url不规范的rss直接复制具体的url，不要使用params
        rss：http://www.kisssub.org/rss-index.xml

### 运行

启动服务

    python server.py

发送指令（可用命令: (start), reload, quit, exit, help）

    python client.py
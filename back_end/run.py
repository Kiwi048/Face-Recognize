from app import create_app

# 通过工厂函数创建 app 实例
app = create_app()

if __name__ == '__main__':
    # 运行 app
    # host='0.0.0.0' 允许网络中其他设备访问，方便前端调试
    # debug=True 会在代码变动后自动重启服务
    app.run(host='0.0.0.0', port=5000, debug=True)

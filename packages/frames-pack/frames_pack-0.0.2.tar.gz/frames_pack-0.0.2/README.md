## FramesPack

![](data/65ce63c95fbf245fbffd97419d48af2e.mp4)


```
make install
make clitest
python3 main.py

# 可以指定所用的 frames pack 文件
#   FALLBACK_FRAMES_PACK_PATH=build/frames_pack2.bin python3 main.py
```

然后打开 localhost:8000

如果你要启动新的前端（frontend/viewer），在运行 python3 main.py 的基础上，
cd frontend/viewer
npm run dev

http://192.168.31.241:3000/#framespack=http://192.168.31.241:3000/frames_pack.bin

(可以在容器内测试：`make test_in_dev_container`，运行测试有可能卡主，原因不明)

---
tags: [工具, 抖音, 视频]
date: 2026-06-07
---
继续 douyin-MP4 项目 


测试:
		 set VIDEO_NAME=你的视频标题 && node node_modules/@remotion/cli/remotion-cli.js studio

		    cmd
    set VIDEO_NAME=你的视频标题
    node node_modules/@remotion/cli/remotion-cli.js render Video --out=output/你的视频标题.mp4


    两行必须同一个 cmd 窗口里跑。VIDEO_NAME 跟 YAML 里的 title 字段一致就行。

    完整流程汇总：


    ① 写 YAML                   tests/XXX.yaml
    ② WSL 生成素材               python3 scripts/generate-all.py tests/XXX.yaml
    ③ Windows cmd 渲染           set VIDEO_NAME=XXX  →  npm run build ...

## 相关笔记

- [[MOC-工具运维]]

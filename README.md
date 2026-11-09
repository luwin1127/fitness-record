# 健身记录（Fitness Record）

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Flutter](https://img.shields.io/badge/Flutter-3.x-blue)
![Platform](https://img.shields.io/badge/platform-Android-green)
![Version](https://img.shields.io/badge/version-4.9.15-brightgreen)

轻量级、完全离线的健身训练记录 App

</div>

---

## 🙏 来源与致谢

本项目基于 **[AixKevin](https://github.com/AixKevin)** 的开源作品
**[XWorkout](https://github.com/AixKevin/XWorkout)**（MIT 协议）修改而来。

- 训练计划管理、每组重量与次数记录、日历视图、历史记录、数据统计、数据导出等
  核心功能，以及数据库结构、界面设计，均来自原作者。
- 本仓库只做了品牌化调整：应用名称、应用包名、关于页署名。
- MIT 协议与 `LICENSE` 中的原始版权声明完整保留。

感谢原作者的辛苦付出，没有 XWorkout 就没有这个项目。

| 角色 | 信息 |
|------|------|
| 原作者 | AixKevin — https://github.com/AixKevin |
| 原项目 | XWorkout — https://github.com/AixKevin/XWorkout |
| 本项目维护者 | LeiLie |
| 本项目仓库 | https://github.com/luwin1127/fitness-record |
| 应用包名 | `com.fitness` |

---

## 📱 关于「健身记录」

一款为健身爱好者设计的轻量级训练记录应用，采用 Cupertino 设计语言，界面简洁。
支持完全离线使用，训练数据全部存储在本地 SQLite 数据库中，不上传、不联网。

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🏋️ **训练计划管理** | 创建个性化训练计划，灵活配置训练项目 |
| 📝 **详细训练记录** | 记录每组次数、重量，追踪训练进度 |
| 📅 **日历视图** | 直观的日历展示，一目了然查看训练历史 |
| 📊 **训练统计** | 查看训练频率、动作统计，了解训练趋势 |
| 🔒 **完全离线** | 本地 SQLite 数据库存储，无需网络 |
| 🎨 **Apple 风格** | Cupertino 设计语言，简洁现代的界面 |
| ⚙️ **高度可定制** | 重量单位、日期格式、训练类型均可自定义 |

## 🔧 相较于原版的改动

- 应用名称由 `XWorkout` 改为 `健身记录`
- 应用包名由 `io.github.aixkevin.xworkout` 改为 `com.fitness`
- 关于页移除原作者 GitHub 链接与贡献者展示，改为本维护者署名
- 新增 GitHub Actions 自动构建流程
- 补充 `scripts/prepare_android.py`，用于生成被上游忽略的 `android/` 工程

> 功能逻辑、数据库结构、页面与交互均未改动。

## 🛠️ 技术栈

| 技术 | 说明 |
|------|------|
| Flutter 3.x / Dart 3.x | 跨平台 UI 框架 |
| Riverpod | 状态管理 |
| Drift (SQLite) | 本地数据库 ORM |
| go_router | 声明式路由 |
| Cupertino | Apple 风格组件 |

## 🚀 构建

### 方式一：GitHub Actions（推荐，本机零依赖）

推送到 `main` 分支会自动触发构建；也可以在
[Actions](https://github.com/luwin1127/fitness-record/actions/workflows/build-apk.yml)
页面手动点击 **Run workflow**。

构建完成后，APK 会自动发布到
[Releases](https://github.com/luwin1127/fitness-record/releases) 页面：

- `fitness-arm64-v8a.apk` — 64 位 ARM（绝大多数安卓手机，含荣耀 300 Pro）
- `fitness-armeabi-v7a.apk` — 32 位 ARM
- `fitness-x86_64.apk` — x86_64 模拟器

### 方式二：本地构建

需要 Flutter 3.38.4+ / Dart 3.10.3+、JDK 17、Android SDK。

> 注意：上游 `.gitignore` 忽略了 `android/` 目录，本仓库同样不包含。
> 本地构建前先运行生成脚本，它会创建 `android/` 并写入包名与应用名。

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs
python3 scripts/prepare_android.py
flutter build apk --release --split-per-abi
```

产物位于 `build/app/outputs/flutter-apk/`。

## 📲 安装

1. 在 [Releases](https://github.com/luwin1127/fitness-record/releases) 下载 `fitness-arm64-v8a.apk`；
2. 传到手机（浏览器直接下载 / 数据线 / 微信文件传输）；
3. 点击安装，若提示「未知来源」，在系统设置中允许一次即可。

> 首次安装是全新应用，不会继承原版 XWorkout 的数据。如需迁移，请先在原版
> 「数据管理」中导出备份，再在新版中恢复。
>
> 本仓库 Release 中的 APK 使用 Flutter 模板的 debug 签名，仅用于个人安装，
> 不适合上架应用商店。不同批次构建的签名可能不同，覆盖安装失败时请先卸载旧版。

## 📁 项目结构

```
lib/
├── core/                    # 核心功能
│   ├── database/            # 数据库层 (Drift)
│   ├── router/              # 路由配置 (go_router)
│   └── theme/               # 主题系统
├── features/                # 功能模块
│   ├── today/               # 今日训练
│   ├── training/            # 训练计划管理
│   ├── workout/             # 训练执行
│   ├── history/             # 历史记录
│   ├── statistics/          # 训练统计
│   ├── settings/            # 应用设置
│   └── more/                # 更多设置
├── shared/                  # 共享组件
└── main.dart                # 应用入口
```

## 📋 数据模型

| 表名 | 说明 |
|------|------|
| WorkoutTypes | 训练类型 |
| Exercises | 训练动作 |
| WorkoutSessions | 训练记录 |
| WorkoutSets | 训练组数 |
| WorkoutPlans | 训练计划 |
| PlanDays | 计划中的天数 |
| DayExercises | 每日训练动作 |
| DailyRecords | 每日记录 |
| ExerciseRecords | 动作记录 |
| AppSettings | 应用设置 |

## 📝 更新日志

版本历史沿用上游记录，详见
[XWorkout 更新日志](https://github.com/AixKevin/XWorkout)。

近期版本摘要：

### v4.9.15
- 训练历史中显示备注内容
- 训练历史编辑增强（可编辑重量、次数、单位，增删训练组）

### v4.9.14
- 重量单位不自动转换，保留原始数值
- 所有重量数值向下取整为整数

### v4.9.12
- 训练中添加「片」重量单位
- 训练历史详情页增加编辑功能
- 动作管理显示最近记录与最佳表现

### v4.9.11
- 新增重量单位「片」选项
- 设置中支持主题模式切换

### v4.9.10
- 修改应用包名

## 📄 许可证

[MIT License](LICENSE)

原始版权声明：`Copyright (c) 2024 XWorkout`

根据 MIT 协议，任何人均可自由使用、修改、分发本软件，但须保留上述版权声明与许可声明。

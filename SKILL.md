---
name: token-optimization
description: 指导 AI 大模型、LLM Agent 与 Prompt 工程减少 Token 消耗，提供无损压缩、高效 Prompt 设计、Context 上下文管理、代码精简生成与结构化输出优化方案。
---

# Skill: AI Token Optimization Guide (Token 极致优化指南)

本 Skill 旨在为 AI 大模型（LLM）、AI Agent 代理及开发者提供一套全面、实用的 Token 消耗优化规范。通过本指南，可以使 AI 在保持推理质量、代码准确性与功能完整性的同时，显著降低 **Input Token** 与 **Output Token** 的开销（通常可减少 **30% - 70%** 的 Token 占用）。

---

## 📖 核心原则 (Core Principles)

1. **信息无损压缩 (Information Density Maximization)**：剔除冗余的表达与修饰词，提高单位 Token 的语义密度。
2. **增量更新 (Incremental Diffs vs Full Dump)**：在代码修改与文档更新时，优先使用局部 Diff/Patch，而非全量重写。
3. **按需上下文 (Context-on-Demand)**：采用精确定位与搜索（Search & Read），避免将非必要大文件直接传入上下文。
4. **结构化极简输出 (Compact Structured Output)**：采用极简 JSON/YAML/Markdown 格式，减少空白字符与重复键名。
5. **系统提示词剪枝 (System Prompt Pruning)**：精简 Persona 定义，合并同类规则，去除冗长示例。

---

## 💡 一、 Prompt 设计与指令优化 (Prompt Engineering Optimization)

### 1.1 消除客套与套话
- **避免**：“你好！我是你的 AI 助手，今天很高兴为你服务。关于你提出的问题，下面是我为你准备的详细解答...”
- **推荐**：直接输出答案或代码，开门见山。

### 1.2 指令合并与符号化
使用缩写、符号与结构化列表替代长篇大论：
```markdown
# 优化前 (耗费 ~80 tokens)
请你扮演一个 Python 专家。你在编写 Python 代码时，需要注意编写规范，不要包含任何多余的解释文字，只需要给出代码本身即可。如果需要测试，请附带单元测试。

# 优化后 (耗费 ~25 tokens)
Role: Senior Python Dev.
Rules:
1. Output code ONLY (no markdown chit-chat).
2. Include unit tests.
```

### 1.3 Few-Shot 示例极简化
只提供最小覆盖边界情况的 Shot 示例，避免冗长上下文：
```markdown
# Compact Few-Shot Pattern
Input: "hello world" -> Output: "HELLO WORLD"
Input: "foo bar" -> Output: "FOO BAR"
```

---

## 📂 二、 Context 上下文管理优化 (Context Window Optimization)

### 2.1 Git Diff 代替全量覆盖
在编辑代码时，使用 Git Merge/Diff 规范或 Search/Replace 替换全量文件输出：

```diff
<<<<<<< SEARCH
def add(a, b):
    return a + b
=======
def add(a: float, b: float) -> float:
    """Add two numbers with typing."""
    return a + b
>>>>>>> REPLACE
```

### 2.2 摘要化长对话历史 (Semantic Truncation & Summarization)
当对话历史超过临界点时，将早期对话压缩为单条摘要：
- **历史对话 (原 2000 tokens)** $\rightarrow$ **摘要 (100 tokens)**：“用户之前要求构建一个 FastAPI 静态服务器，已完成 `server.py` 与静态路由，当前目标是添加 Token 统计接口。”

### 2.3 局部代码检索与精准读取
避免一次性读取整个大型 codebase，优先通过 `grep` 或 `list_files` 找出目标文件，读取特定行区间。

---

## 💻 三、 代码生成 Token 优化 (Code Generation Efficiency)

### 3.1 去除重复样板与繁琐注释
- 避免对显而易见的代码逐行添加多余注释。
- 使用通用工具函数或内置库减少重复逻辑。

```python
# 优化前：过度注释与冗长样板
# 这是一个用于计算列表中所有偶数平方和的函数
def sum_of_even_squares(numbers):
    # 初始化总和变量为0
    total_sum = 0
    # 遍历数字列表中的每一个元素
    for number in numbers:
        # 判断当前数字是否为偶数
        if number % 2 == 0:
            # 计算平方
            square = number ** 2
            # 累加到总和
            total_sum += square
    # 返回最终结果
    return total_sum

# 优化后：精简无损代码
def sum_of_even_squares(numbers: list[int]) -> int:
    return sum(n ** 2 for n in numbers if n % 2 == 0)
```

### 3.2 单次生成可运行补丁 (Executable Snippets)
无需重新生成整个 500 行的模块，仅生成修改的具体函数或类。

---

## 📊 四、 结构化输出优化 (Compact Structured Output)

### 4.1 紧凑 JSON (Compact JSON without Pretty Print)
在工具调用或 API 响应中，禁用多余的换行与缩进空格：

```json
/* 优化前 (Pretty Print: 120 bytes, 40 tokens) */
{
  "status": "success",
  "data": {
    "user_id": 1001,
    "role": "admin"
  }
}

/* 优化后 (Minified JSON: 48 bytes, 16 tokens) */
{"status":"success","data":{"user_id":1001,"role":"admin"}}
```

### 4.2 表格与 YAML 替换冗长文本
使用紧凑 Markdown 表格传达多维数据：

| Param | Type | Default | Description |
|---|---|---|---|
| `token_limit` | int | 4096 | Max tokens per call |
| `compact` | bool | True | Strip whitespace |

---

## 🚀 五、 Token 优化效果对比与检查清单 (Checklist & ROI)

| 优化维度 | 传统做法 | Token 优化做法 | 平均 Token 节省率 |
|---|---|---|---|
| **代码修改** | 全量重写完整文件 | Git Diff / Search-Replace | **60% - 85%** |
| **Prompt 指令** | 礼貌套话 + 冗长描述 | 符号化角色定义 + 短指令 | **40% - 60%** |
| **上下文传递** | 复制完整文件库 | 精确检索 + 局部切片 | **50% - 80%** |
| **JSON 数据** | 缩进格式化 JSON | 压缩紧凑型 JSON | **30% - 50%** |

### 🛠️ 快速检查清单 (Quick Checklist for AI & Developers)
- [ ] 是否消除了系统提示词中的无意义客套话？
- [ ] 代码修改是否使用了 Diff/Patch 格式而非全量文件输出？
- [ ] 是否避免了对显而易见代码的过度注释？
- [ ] 上下文输入是否只包含与当前任务直接相关的行或片段？
- [ ] JSON/数据响应是否采用了 Minified 压缩格式？

---

## 📦 Package Spec
- `.md` file includes standard YAML frontmatter with `name` and `description`.
- `SKILL.md` included inside `.zip` and `.skill` skill packages for seamless integration.

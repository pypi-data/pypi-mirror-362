""" core 需要修改"""
import re
import os
import time
from contextlib import contextmanager
import importlib.resources
from typing import Dict, Any
import yaml
from llmada.core import BianXieAdapter
from querypipz import BuilderFactory,BuilderType,Director

from .log import Log
logger = Log.logger
logger_path = 'logs/querypipz.log'

""" config.yaml
query_persist_dir: /Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes
WORK_CANVAS_PATH:
- /工程系统级设计/能力级别/人体训练设计/人体训练设计.canvas
ModelCards:
- gpt-4.1
- cus-gemini-2.5-flash-preview-04-17-nothinking
- cus-gemini-2.5-flash-preview-04-17-thinking
Custom:
- config_info
- chat_with_long_memory_v2
- long_memory_v2_retriver
- chat_with_Agent_notes
- Custom_Agent_Latest
- Experts_V1
"""



LLM_INFO = {
"query_persist_dir": "/Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes",
"WORK_CANVAS_PATH": [
"/工程系统级设计/能力级别/人体训练设计/人体训练设计.canvas"
],
"ModelCards": [
    "gpt-4.1",
    "cus-gemini-2.5-flash-preview-04-17-nothinking",
    "cus-gemini-2.5-flash-preview-04-17-thinking",
    "cus-gemini-2.5-flash-preview-05-20-nothinking",
],
"Custom": [
            "config_info",
            "logger_info",
            "chat_with_long_memory_v2",
            "chat_with_long_memory_v3",
            "long_memory_v2_retriver",
            "chat_with_Agent_notes",
            "Custom_Agent_Latest",
            "Experts_V1",
            "ReactAgent_API_Expert",
            "small_chat",
            "small_chat_fass",
            "document_expert",

        ]
}



def load_config():
    """ load config """
    with importlib.resources.open_text('clientz', 'config.yaml') as f:
        return yaml.safe_load(f)

def format_node_for_chat(node_data: Dict[str, Any]) -> str:
    """
    解析节点数据，生成适合聊天窗口显示的格式化字符串。

    Args:
        node_data: 包含节点信息的字典结构。

    Returns:
        一个格式化的字符串，包含分数和节点文本内容。
        如果结构异常，返回错误提示。
    """
    node = node_data.get('node')
    score = node_data.get('score')

    if not node:
        return "Error: Could not find 'node' information."

    text_content = node.get('text')
    if not text_content:
        return "Error: 'text' content not found in node."

    # 移除 text 开头的 "topic:  content: \n\n\n" 或类似的元数据前缀
    # 根据你提供的样本，可能是固定的前缀，或者需要更灵活的处理
    # 这里简单移除已知的开头
    prefix_to_remove = "topic:  content: \n\n\n"
    if text_content.startswith(prefix_to_remove):
        text_content = text_content[len(prefix_to_remove):].strip()
    else:
        text_content = text_content.strip() # 或者只移除首尾空白

    # 构建输出字符串
    output = ""
    if score is not None:
        # 格式化分数，例如保留两位小数
        output += f"**Relevant Information (Score: {score:.2f})**:\n\n"
    else:
        output += "**Relevant Information:**\n\n"

    # 直接添加处理后的文本内容
    # 假设聊天窗口支持 Markdown，会渲染 #, ##, **, -, []() 等
    output += text_content

    # 你可以进一步处理 links，例如将它们提取出来单独列在末尾
    # link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    # links_found = link_pattern.findall(text_content)
    # if links_found:
    #     output += "\n\n---\n*Links mentioned:*\n"
    #     for link_text, link_url in links_found:
    #         output += f"- [{link_text}]({link_url})\n" # 或其他格式

    return output

def extract_last_user_input(dialogue_text):
    """
    从多轮对话文本中提取最后一个 user 的输入内容。

    Args:
        dialogue_text: 包含多轮对话的字符串。

    Returns:
        最后一个 user 的输入内容字符串，如果未找到则返回 None。
    """
    # 修正后的正则表达式
    # (?s) 标志：使 . 匹配换行符
    # .* 匹配任意字符，直到最后一个 user:
    # user:\s* 匹配 "user:" 后面的零个或多个空白字符
    # (.*?) 非贪婪匹配任意字符，直到下一个 user: 或字符串末尾
    # (?=user:|$) 正向先行断言：断言后面是 "user:" 或者字符串末尾
    pattern = r"(?s).*user:\s*(.*?)(?=user:|$)"

    match = re.search(pattern, dialogue_text)

    if match:
        # group(1) 捕获的是最后一个 user: 到下一个 user: 或字符串末尾的内容
        return match.group(1).strip()
    else:
        return None




@contextmanager
def check_time(title:str,logger):
    """ try catch"""
    time1 = time.time()
    yield
    time2 = time.time()
    logger.debug(f"{title}: {time2-time1}")

    

def extra_docs(inputs:str)->dict:
    """ docs """
    pattern1 = r'<context>(.*?)<\/context>'
    pattern2 = r'<source id="(\d+)">(.*?)<\/source>'

    match = re.search(pattern1, inputs,re.DOTALL)

    if match:
        sources = match.group(1).strip()
        matches = re.findall(pattern2, sources)

    result = {int(id): content for id, content in matches}
    return result


class ChatBox():
    """ chatbox """
    def __init__(self) -> None:
        self.bx = BianXieAdapter()
        # self.dicts = load_config()
        self.dicts = LLM_INFO
        self.query_persist_dir = self.dicts.get('query_persist_dir')
        self.model_pool = self.dicts.get("ModelCards")
        self.file_path = 'clientz/config.yaml'
        self._last_modified_time = None
        self._update_last_modified_time()
        self.init_lazy_parameter()
        self.query = None
        self.ReactAgent_API_Expert_engine = None
        self.user = None

        self.work_state = True
        self.chat_cache = ""

    def _update_last_modified_time(self):
        """更新存储的最后修改时间"""
        try:
            self._last_modified_time = os.path.getmtime(self.file_path)
        except FileNotFoundError:
            self._last_modified_time = None # 文件不存在时设为None

    def check_and_trigger(self):
        """检查文件是否变化，如果变化则触发动作"""
        try:
            current_modified_time = os.path.getmtime(self.file_path)
            if current_modified_time != self._last_modified_time:
                print(f"文件 '{self.file_path}' 已发生变化。")
                self._trigger_action()
                self._last_modified_time = current_modified_time # 更新存储的时间
            else:
                print(f"文件 '{self.file_path}' 未发生变化。")
        except FileNotFoundError:
            print(f"文件 '{self.file_path}' 不存在。")
            self._last_modified_time = None # 文件不存在时重置状态
        except Exception as e:
            print(f"检查文件时发生错误: {e}")

    def _trigger_action(self):
        """当文件发生变化时触发的动作"""
        # 可以修改
        # 这里可以放置你想要执行的具体动作，例如：
        # - 读取文件内容
        # - 处理文件数据
        # - 调用其他函数
        print("触发预定动作...")
        # 示例：读取文件内容并打印
        try:
            self.dicts = load_config()

        except FileNotFoundError:
            print(f"触发动作时文件 '{self.file_path}' 不存在。")
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

    def init_lazy_parameter(self):
        """ 一个懒加载的初始化头部 """
        self.chat_with_agent_notes_object = None

    def product(self,prompt_with_history: str, model: str) -> str:
        """ x """

        prompt_no_history = extract_last_user_input(prompt_with_history)
        logger.debug(f"# prompt_no_history : {prompt_no_history}")
        logger.debug(f"# prompt_with_history : {prompt_with_history}")
        prompt_with_history, model

        return 'product 还没有拓展'

    async def astream_product(self,prompt_with_history: str, model: str) -> Any:
        """
        # 只需要修改这里
        """
        # self.check_and_trigger()
        prompt_no_history = extract_last_user_input(prompt_with_history)

        logger.debug(f"# prompt_no_history : {prompt_no_history}")
        logger.debug(f"# prompt_with_history : {prompt_with_history}")
        ## __init__ ##
        if model in self.model_pool:
            print(model[4:],'model[4:]')
            self.bx.model_pool.append('gemini-2.5-flash-preview-05-20-nothinking')
            self.bx.set_model(model[4:])
            # with open('/Users/zhaoxuefeng/WorkBench/temp_input.txt','w') as f:
            #     f.write(prompt_no_history)

            result = ""
            for word in self.bx.product_stream(prompt_with_history):
                yield word
            #     result += word
            
            # with open('/Users/zhaoxuefeng/WorkBench/temp_output.txt','w') as f:
            #     f.write(result)


        elif model == "config_info":
            logger.info(f"running {model}")
            yield f"query_dir: {self.query_persist_dir}, dicts {str(self.dicts)}"

            if self.chat_with_agent_notes_object:
                yield self.chat_with_agent_notes_object.tool_calls()

        elif model == "logger_info":
            logger.info(f"running {model}")
            with open(logger_path,'r') as f:
                text = f.read()
            yield text[-10000:]

        elif model == 'document_expert':
            doc_init_system_prompt = """
你是一个专业工程师, 用户现在想做一个python的项目,可能是package(提供一些简单能力的第三方包),SDK(提供一些操作软件或者特定格式的能力),或者是工程项目(将各种能力资源整合起来, 构建项目级别的应用). 
请根据以下工作流程和用户交流,并最终产出PRD和LLD文档, 在与用户交流时, 参考一些默认配置或则用户习惯,用户可以主动介入来把控聊天节奏

请准寻以下工作流程:
## 工作流程:
	与用户讨论交流, 理解用户的需求.
	询问用户是否有补充内容
	if 用户有补充内容:
		与用户交流
	基于达成的共识,展示一个假设实现以后的使用场景或者教程,提供案例并与用户交流确认
	if 用户有补充内容:
		与用户交流
	形成正式的PRD和LLD文档

## 用户默认设置
	要了解这件事的前因后果和想法来源
	要了解这件事的核心或用户最在意的点
	一个问题一个问题进行
	面向开发者, 面向用户个人
	明确核心案例(用例),
	明确主要职责, 上游和下游的基本情况, 如何对接
	使用uv 管理项目, 使用uv add 进行安装

## 文档格式要求

### PRD标准格式
务实风格, 承担拉齐各个部分角色的认知
#### 输出格式
使用以下格式输出
<prd></prd>
### LLD标准格式
要包含项目名, 版本号, UML设计, 示例, 测试代码等固定内容
其他的可以酌情增删
#### 输出格式
使用以下格式输出
<lld></lld>
#### UML设计
	包含设计模式
	使用mermaid 语法实现(对于中文要使用双引号, 避免使用复杂的语法,来降低出错概率)

#### 示例内容
	最好包含最初始的用例

#### 测试代码
	以pytest为基础进行测试代码的编写

#### mock数据
	对于交互性或者数据重视型的项目, 优先使用mock数据, 保证其Server CLI 设计模式等代码跑通和正确, 完成度高于质量

### CR标准格式
	暂无

### DCN标准格式
	暂无

## 其他

### 关于文档版本号与更新
	1 初始版本为V1.0
	2 后续PRD的每次小补丁 (更新V1.1)
	3 重大更新或者项目完全重构(更新V2.0)
### 关于项目名(包名)规范
	1 纯英文, 不能包含大写字母.要满足pypi 格式要求
	2 可以使用 '_' 来分割项目
	3 优先使用用户提供的名称
### 关于项目模版
	项目会使用统一的模版, 提供一些标准的函数和工具以及编程范式,准寻这些范式
		1核心的对外提供函数尽可能放到core.py 文件中, 并提供详尽文档
		2要使用模版提供的log.py 和server.py文件, 与其他包保持一致性
#### 关于核心core.py 的API文档与注释
	对于本包对外提供能力的核心文件和核心函数, 为其中的方法编写合适的api注释(遵守pylint 4.0.0 格式),要求可以让人只读取api文档和函数头就可以明确知道其功能和使用方法
	将核心逻辑放到core.py 中有以下好处:
		1 对外提供的能力明确
		2 减少优质文档的维护量, 只需要在core.py 的文件范围内, 编写详细的代码注释和实例
		3 方便后续RAG的制作和大模型对于该包的理解

"""



            prompt = doc_init_system_prompt + "\n"+prompt_with_history
            time1 = time.time()
            for word in self.bx.product_stream(prompt):
                logger.debug(f"first_tokens_time: {time.time()-time1}")
                yield word


        elif model == 'small_chat': # 存放以后再开发
            def work(article:str = '没有新文章'):
                prompt = f"""
            请遵循以下逻辑设定:
                if 之前的聊天记录有信息密度很高,类似文章的内容 并且用户也是在提问相关内容:
                    根据文章中的信息回答用户的问题,要求做到低信息的交流, 要拟真的去交流, 给用户留下气口和合适的内容体量
                    if 用户忽略但是你认为有必要提醒用户的信息:
                        你可以主动告知用户
                else:
                    进行高频短字数的交流
                    
                if 用户要求总结一下之前的交流:
                    将之前的聊天内容中的有效聊天,总结成一个对大模型友好的, 成体系的文章 使用以下格式输出
                    ```summery
                    
                    ```

            # 当前文章:

            {article}

            # 用户提问:
                """
                return prompt

            system_prompt = work(self.chat_cache)
            prompt = system_prompt + "\n"+prompt_with_history
            logger.info(f'{prompt_with_history},prompt_with_history--->')
            logger.info(f'{prompt_no_history},prompt_no_history--->')

            time1 = time.time()
            for word in self.bx.product_stream(prompt):
                logger.debug(f"first_tokens_time: {time.time()-time1}")
                yield word

        elif model == "ReactAgent_API_ExpertV2":
            from toolsz.dev import AutoAPIMD
            from llama_index.core.query_engine import CustomQueryEngine
            from llama_index.llms.openai import OpenAI
            from llama_index.core import PromptTemplate
            from llama_index.core.tools import QueryEngineTool, ToolMetadata
            from llama_index.core import Settings
            from llama_index.core.agent.workflow import ReActAgent
            from llama_index.core.workflow import Context
            from llama_index.core.agent.workflow import ToolCallResult, AgentStream

            import querypipz
            qa_prompt = PromptTemplate(
                "API文档信息如下.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information and not prior knowledge, "
                "answer the query.\n"
                "Query: {query_str}\n"
                "Answer: "
            )





            class APIQueryEngine(CustomQueryEngine):
                """RAG String Query Engine."""

                # retriever: BaseRetriever
                # response_synthesizer: BaseSynthesizer
                llm: OpenAI
                qa_prompt: PromptTemplate
                input_files: list[str]
                def custom_query(self, query_str: str):
                    context_strs = ""
                    for input_file in self.input_files:
                        try:
                            context_strs += AutoAPIMD().generate_api_docs(input_file, 'api_documentation_mermaidz.md')
                        except:
                            pass

                    response = self.llm.complete(
                        qa_prompt.format(context_str=context_strs, query_str=query_str)
                    )

                    return str(response)

            path_lists = {
                "llmada":['/Users/zhaoxuefeng/GitHub/llmada/src/llmada/core.py'],
                "canvaz":['/Users/zhaoxuefeng/GitHub/canvaz/src/canvaz/core.py'],
                "kanbanz":['/Users/zhaoxuefeng/GitHub/kanbanz/src/kanbanz/core.py'],
                "appscriptz":['/Users/zhaoxuefeng/GitHub/appscriptz/src/appscriptz/core.py'],
                "toolsz":['/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/dev.py','/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/freedom_function.py'],
                "mermaidz":['/Users/zhaoxuefeng/GitHub/mermaidz/src/mermaidz/core.py'],
                "promptlibz":['/Users/zhaoxuefeng/GitHub/promptlibz/src/promptlibz/core.py'],
                "obwikilink":['/Users/zhaoxuefeng/GitHub/obwikilink/src/obwikilink/core.py'],

            }

            descript_dicts = {
                "llmada":"""
根据提供的API文档信息，这个包似乎是一个用于适配不同语言大模型的框架。它定义了一些抽象类和具体的适配器类，用于与不同的模型进行交互。以下是一些关键点：

1. **抽象类和接口**: `ModelAdapter`是一个抽象基类，定义了与语言大模型交互的基本接口，如`set_model`、`set_temperature`、`product`和`chat`等方法。子类需要实现这些方法以适配具体的模型。

2. **具体适配器**: 包含多个具体的适配器类，如`BianXieAdapter`、`ArkAdapter`、`GoogleAdapter`和`KimiAdapter`，每个适配器类都实现了与特定模型的交互逻辑。这些适配器类通常需要API密钥和API基础URL来进行初始化。

3. **多模态支持**: `ModelModalAdapter`及其子类提供了多模态交互的支持，允许处理富文本格式的提示。

4. **异常处理**: 定义了一个`ResourceExhaustedError`异常，用于处理资源配额超出的情况。

总体来看，这个包提供了一种结构化的方式来与不同的语言大模型进行交互，具有良好的扩展性和适应性。通过定义抽象类和具体实现，用户可以方便地切换和使用不同的模型。
""",
                "canvaz":"""
这个包提供了一套用于操作和管理Canvas文件的工具。它的核心功能是通过Node和Edge对象来表示Canvas中的节点和边，并允许用户通过修改这些对象的属性来操作Canvas内容。包中定义了多个类，包括Color和Range枚举类，用于表示颜色和搜索范围，Node和Edge类用于表示Canvas中的节点和边，Canvas类则提供了一系列方法来操作Canvas文件。

从功能上看，这个包提供了丰富的操作接口，比如添加节点、通过ID或颜色选择节点或边、通过文本内容筛选节点或边等。这些功能使得用户可以方便地对Canvas文件进行各种操作和查询。此外，包还支持将Canvas内容导出为文件或Mermaid格式，这对于需要将Canvas内容进行持久化存储或可视化展示的场景非常有用。

总体而言，这个包设计得比较全面，提供了多种操作Canvas文件的方式，适合需要对Canvas文件进行复杂操作的用户。不过，包中有一些方法（如add_edge、delete、select_by_styleAttributes）尚未实现，可能需要进一步开发以完善功能。
""",
                "kanbanz":"""
这个包似乎是一个用于管理看板（Kanban）的SDK，特别是与Obsidian结合使用的工具。它通过处理特定格式的Markdown文件来管理任务。以下是我对这个包的一些看法：

1. **功能全面**: 包含了管理看板所需的基本功能，如任务的插入、删除、查询等。通过不同的任务池（如预备池、就绪池、阻塞池等）来管理任务的状态，提供了一个结构化的任务管理方式。

2. **灵活性**: 提供了通过关键字查询任务的功能，以及通过不同方式（如代码或LLM）预估任务时间的选项，显示出一定的灵活性。

3. **集成性**: 通过KanBanManager类，可以将任务从多个canvas文件中提取并汇总到看板中，显示出与其他工具（如Obsidian）的良好集成能力。

4. **自动化**: 提供了任务同步和排序的功能，可以自动化地将任务从预备池移动到就绪池，再到执行池，帮助用户更高效地管理任务。

5. **可扩展性**: 由于使用了枚举类来定义任务池类型，未来可以很容易地扩展新的任务状态或功能。

总体来说，这个包为用户提供了一种结构化且自动化的方式来管理任务，特别适合那些使用Obsidian进行个人或团队任务管理的人。
""",
                "appscriptz":"""
这个包似乎是一个用于与macOS应用程序进行交互的Python库。它提供了一些类和函数，用于通过AppleScript与macOS的备忘录、提醒事项、日历、快捷指令等应用进行操作。以下是对这个包的一些看法：

1. **功能多样**：包中包含多个类和函数，涵盖了备忘录、提醒事项、日历事件管理、用户界面显示以及快捷指令的执行等功能。这使得它在自动化和脚本化macOS任务方面非常有用。

2. **AppleScript集成**：通过AppleScript与macOS应用程序进行交互，这使得该包能够利用macOS的原生功能来执行复杂的任务。

3. **灵活性**：提供了多种方法来处理不同的任务，例如创建和更新日历事件、显示对话框和选择框、运行快捷指令等。这种灵活性使得用户可以根据自己的需求进行定制。

4. **缺少文档**：虽然方法的参数和返回值有详细说明，但类本身缺少文档字符串，这可能会对理解类的整体用途和设计意图造成一定困难。

5. **用户交互**：提供了一些用于用户交互的功能，如显示对话框和选择框，这对于需要用户输入的自动化任务非常有帮助。

总体而言，这个包对于需要在macOS上进行自动化操作的开发者来说是一个有用的工具，特别是在需要与系统应用进行交互的场景中。

""",
                "toolsz":"""
这个包提供了一些开发支持工具，主要功能包括生成Git提交历史的可视化图表和自动生成Python文件的API文档。它包含两个主要类：`GitHubManager`和`AutoAPIMD`，以及一些辅助函数。

1. **GitHubManager**: 这个类的主要功能是处理GitHub仓库的提交历史。它可以生成Mermaid格式的Git图表，并提供一些基本的运行方法。

2. **AutoAPIMD**: 这个类用于自动生成Python文件的API文档。它能够解析Python文件，提取模块、类、方法和函数的签名及文档字符串，并生成Markdown格式的文档。这对于需要维护大型代码库的开发者来说是一个非常有用的工具，因为它可以自动化文档生成过程，节省时间和精力。

3. **辅助函数**: 这些函数提供了一些额外的功能，比如输入输出校验、异常管理、函数打包和多行输入处理等。

总体来看，这个包对于开发者特别是需要处理Git历史和生成API文档的场景非常有帮助。它通过自动化一些常见的开发任务，提高了效率和代码的可维护性
""",
                "mermaidz":"""
一个mermaid包
""",
                "promptlibz":"""
这个包似乎是一个用于管理和存储 Prompt 的工具。它提供了一个结构化的方式来创建、保存、加载、列出和删除不同版本的 Prompt。以下是对这个包的一些看法：

1. **模块化设计**：包的设计是模块化的，分为三个主要类：`BaseManagedPrompt`、`PromptRepository` 和 `PromptManager`。这种设计使得每个类都有明确的职责，便于维护和扩展。

2. **功能全面**：提供了从创建到管理 Prompt 的完整功能集，包括保存、加载、列出和删除 Prompt 及其版本。这对于需要频繁管理不同 Prompt 版本的用户来说非常有用。

3. **灵活性**：`PromptRepository` 类允许用户指定存储的基本目录，这为用户提供了灵活性，可以根据自己的需求调整存储位置。

4. **高级接口**：`PromptManager` 提供了一个高级接口，简化了对 Prompt 的管理操作，使得用户可以更方便地添加、获取和删除 Prompt。

5. **缺少文档**：尽管方法的功能从名称上可以推测，但缺少详细的文档说明可能会对新用户造成一定的使用障碍。增加详细的文档和示例代码会提高可用性。

总体来说，这个包对于需要管理 Prompt 的开发者来说是一个有用的工具，尤其是在处理多个版本的情况下。通过进一步完善文档和提供更多的使用示例，可以提升其易用性和用户体验
""",
                "obwikilink":"""
这个包似乎是一个用于处理Obsidian Markdown文档的工具，特别是用于创建和管理Obsidian的wikilinks和标签。它提供了一系列类和方法，帮助用户在Markdown文档中识别、创建和插入wikilinks，以及提取和添加标签。

以下是一些关键功能：

1. **WikiLink类**：用于表示Obsidian的wikilink，提供了验证和获取目标路径的方法。

2. **WikiLinkFactory类**：用于从文本或目标名称创建WikiLink对象。

3. **ILinkGenerationStrategy接口及其实现**：定义了生成wikilink的策略接口，并提供了基于关键词和相似度的策略实现。

4. **ObsidianMarkdownSDK类**：提供了一个简化的接口，用于与Obsidian Markdown文档交互。它支持读取和写入Markdown文件、查找和插入wikilinks、重构内容为wikilink、提取文档部分、查找和添加标签等操作。

总体而言，这个包为用户提供了一个强大的工具集，帮助他们更高效地管理和构建Obsidian笔记中的知识网络。通过使用不同的链接生成策略，用户可以根据自己的需求自动化地生成wikilinks
"""
            }
            
            engines = {}

            for name,path_list in path_lists.items():
                engines[name] = APIQueryEngine(
                                                qa_prompt=qa_prompt,
                                                llm = Settings.llm,
                                                input_files = path_list
                                            )

            api_query_engine_tools = []
            api_query_engine_tools_map = {}

            for engine_name, engine in engines.items():
                qetool = QueryEngineTool(
                    query_engine=engine,
                    metadata=ToolMetadata(
                        name=engine_name,
                        description=descript_dicts[engine_name],
                    ),
                )
                api_query_engine_tools.append(qetool)
                api_query_engine_tools_map[engine_name] = qetool

            agent = ReActAgent(
                tools=api_query_engine_tools,
                # llm=OpenAI(model="gpt-4o-mini"),
                # system_prompt="..."
            )

            handler = agent.run(prompt_with_history)
            async for ev in handler.stream_events():
                if isinstance(ev, AgentStream):
                    # print(f"{ev.delta}", end="", flush=True)
                    yield f"{ev.delta}"

        elif model == "ReactAgent_API_Expert":
            from toolsz.dev import AutoAPIMD
            from llama_index.core.query_engine import CustomQueryEngine
            from llama_index.llms.openai import OpenAI
            from llama_index.core import PromptTemplate
            from llama_index.core.tools import QueryEngineTool, ToolMetadata
            from llama_index.core import Settings
            from llama_index.core.agent.workflow import ReActAgent
            from llama_index.core.workflow import Context
            from llama_index.core.agent.workflow import ToolCallResult, AgentStream

            import querypipz
            qa_prompt = PromptTemplate(
                "API文档信息如下.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information and not prior knowledge, "
                "answer the query.\n"
                "Query: {query_str}\n"
                "Answer: "
            )





            class APIQueryEngine(CustomQueryEngine):
                """RAG String Query Engine."""

                # retriever: BaseRetriever
                # response_synthesizer: BaseSynthesizer
                llm: OpenAI
                qa_prompt: PromptTemplate
                input_files: list[str]
                def custom_query(self, query_str: str):
                    context_strs = ""
                    for input_file in self.input_files:
                        try:
                            context_strs += AutoAPIMD().generate_api_docs(input_file, 'api_documentation_mermaidz.md')
                        except:
                            pass

                    response = self.llm.complete(
                        qa_prompt.format(context_str=context_strs, query_str=query_str)
                    )

                    return str(response)

            path_lists = {
                "llmada":['/Users/zhaoxuefeng/GitHub/llmada/src/llmada/core.py'],
                "canvaz":['/Users/zhaoxuefeng/GitHub/canvaz/src/canvaz/core.py'],
                "kanbanz":['/Users/zhaoxuefeng/GitHub/kanbanz/src/kanbanz/core.py'],
                "appscriptz":['/Users/zhaoxuefeng/GitHub/appscriptz/src/appscriptz/core.py'],
                "toolsz":['/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/dev.py','/Users/zhaoxuefeng/GitHub/toolsz/src/toolsz/freedom_function.py'],
                "mermaidz":['/Users/zhaoxuefeng/GitHub/mermaidz/src/mermaidz/core.py'],
                "promptlibz":['/Users/zhaoxuefeng/GitHub/promptlibz/src/promptlibz/core.py'],
                "obwikilink":['/Users/zhaoxuefeng/GitHub/obwikilink/src/obwikilink/core.py'],

            }

            descript_dicts = {
                "llmada":"""
根据提供的API文档信息，这个包似乎是一个用于适配不同语言大模型的框架。它定义了一些抽象类和具体的适配器类，用于与不同的模型进行交互。以下是一些关键点：

1. **抽象类和接口**: `ModelAdapter`是一个抽象基类，定义了与语言大模型交互的基本接口，如`set_model`、`set_temperature`、`product`和`chat`等方法。子类需要实现这些方法以适配具体的模型。

2. **具体适配器**: 包含多个具体的适配器类，如`BianXieAdapter`、`ArkAdapter`、`GoogleAdapter`和`KimiAdapter`，每个适配器类都实现了与特定模型的交互逻辑。这些适配器类通常需要API密钥和API基础URL来进行初始化。

3. **多模态支持**: `ModelModalAdapter`及其子类提供了多模态交互的支持，允许处理富文本格式的提示。

4. **异常处理**: 定义了一个`ResourceExhaustedError`异常，用于处理资源配额超出的情况。

总体来看，这个包提供了一种结构化的方式来与不同的语言大模型进行交互，具有良好的扩展性和适应性。通过定义抽象类和具体实现，用户可以方便地切换和使用不同的模型。
""",
                "canvaz":"""
这个包提供了一套用于操作和管理Canvas文件的工具。它的核心功能是通过Node和Edge对象来表示Canvas中的节点和边，并允许用户通过修改这些对象的属性来操作Canvas内容。包中定义了多个类，包括Color和Range枚举类，用于表示颜色和搜索范围，Node和Edge类用于表示Canvas中的节点和边，Canvas类则提供了一系列方法来操作Canvas文件。

从功能上看，这个包提供了丰富的操作接口，比如添加节点、通过ID或颜色选择节点或边、通过文本内容筛选节点或边等。这些功能使得用户可以方便地对Canvas文件进行各种操作和查询。此外，包还支持将Canvas内容导出为文件或Mermaid格式，这对于需要将Canvas内容进行持久化存储或可视化展示的场景非常有用。

总体而言，这个包设计得比较全面，提供了多种操作Canvas文件的方式，适合需要对Canvas文件进行复杂操作的用户。不过，包中有一些方法（如add_edge、delete、select_by_styleAttributes）尚未实现，可能需要进一步开发以完善功能。
""",
                "kanbanz":"""
这个包似乎是一个用于管理看板（Kanban）的SDK，特别是与Obsidian结合使用的工具。它通过处理特定格式的Markdown文件来管理任务。以下是我对这个包的一些看法：

1. **功能全面**: 包含了管理看板所需的基本功能，如任务的插入、删除、查询等。通过不同的任务池（如预备池、就绪池、阻塞池等）来管理任务的状态，提供了一个结构化的任务管理方式。

2. **灵活性**: 提供了通过关键字查询任务的功能，以及通过不同方式（如代码或LLM）预估任务时间的选项，显示出一定的灵活性。

3. **集成性**: 通过KanBanManager类，可以将任务从多个canvas文件中提取并汇总到看板中，显示出与其他工具（如Obsidian）的良好集成能力。

4. **自动化**: 提供了任务同步和排序的功能，可以自动化地将任务从预备池移动到就绪池，再到执行池，帮助用户更高效地管理任务。

5. **可扩展性**: 由于使用了枚举类来定义任务池类型，未来可以很容易地扩展新的任务状态或功能。

总体来说，这个包为用户提供了一种结构化且自动化的方式来管理任务，特别适合那些使用Obsidian进行个人或团队任务管理的人。
""",
                "appscriptz":"""
这个包似乎是一个用于与macOS应用程序进行交互的Python库。它提供了一些类和函数，用于通过AppleScript与macOS的备忘录、提醒事项、日历、快捷指令等应用进行操作。以下是对这个包的一些看法：

1. **功能多样**：包中包含多个类和函数，涵盖了备忘录、提醒事项、日历事件管理、用户界面显示以及快捷指令的执行等功能。这使得它在自动化和脚本化macOS任务方面非常有用。

2. **AppleScript集成**：通过AppleScript与macOS应用程序进行交互，这使得该包能够利用macOS的原生功能来执行复杂的任务。

3. **灵活性**：提供了多种方法来处理不同的任务，例如创建和更新日历事件、显示对话框和选择框、运行快捷指令等。这种灵活性使得用户可以根据自己的需求进行定制。

4. **缺少文档**：虽然方法的参数和返回值有详细说明，但类本身缺少文档字符串，这可能会对理解类的整体用途和设计意图造成一定困难。

5. **用户交互**：提供了一些用于用户交互的功能，如显示对话框和选择框，这对于需要用户输入的自动化任务非常有帮助。

总体而言，这个包对于需要在macOS上进行自动化操作的开发者来说是一个有用的工具，特别是在需要与系统应用进行交互的场景中。

""",
                "toolsz":"""
这个包提供了一些开发支持工具，主要功能包括生成Git提交历史的可视化图表和自动生成Python文件的API文档。它包含两个主要类：`GitHubManager`和`AutoAPIMD`，以及一些辅助函数。

1. **GitHubManager**: 这个类的主要功能是处理GitHub仓库的提交历史。它可以生成Mermaid格式的Git图表，并提供一些基本的运行方法。

2. **AutoAPIMD**: 这个类用于自动生成Python文件的API文档。它能够解析Python文件，提取模块、类、方法和函数的签名及文档字符串，并生成Markdown格式的文档。这对于需要维护大型代码库的开发者来说是一个非常有用的工具，因为它可以自动化文档生成过程，节省时间和精力。

3. **辅助函数**: 这些函数提供了一些额外的功能，比如输入输出校验、异常管理、函数打包和多行输入处理等。

总体来看，这个包对于开发者特别是需要处理Git历史和生成API文档的场景非常有帮助。它通过自动化一些常见的开发任务，提高了效率和代码的可维护性
""",
                "mermaidz":"""
一个mermaid包
""",
                "promptlibz":"""
这个包似乎是一个用于管理和存储 Prompt 的工具。它提供了一个结构化的方式来创建、保存、加载、列出和删除不同版本的 Prompt。以下是对这个包的一些看法：

1. **模块化设计**：包的设计是模块化的，分为三个主要类：`BaseManagedPrompt`、`PromptRepository` 和 `PromptManager`。这种设计使得每个类都有明确的职责，便于维护和扩展。

2. **功能全面**：提供了从创建到管理 Prompt 的完整功能集，包括保存、加载、列出和删除 Prompt 及其版本。这对于需要频繁管理不同 Prompt 版本的用户来说非常有用。

3. **灵活性**：`PromptRepository` 类允许用户指定存储的基本目录，这为用户提供了灵活性，可以根据自己的需求调整存储位置。

4. **高级接口**：`PromptManager` 提供了一个高级接口，简化了对 Prompt 的管理操作，使得用户可以更方便地添加、获取和删除 Prompt。

5. **缺少文档**：尽管方法的功能从名称上可以推测，但缺少详细的文档说明可能会对新用户造成一定的使用障碍。增加详细的文档和示例代码会提高可用性。

总体来说，这个包对于需要管理 Prompt 的开发者来说是一个有用的工具，尤其是在处理多个版本的情况下。通过进一步完善文档和提供更多的使用示例，可以提升其易用性和用户体验
""",
                "obwikilink":"""
这个包似乎是一个用于处理Obsidian Markdown文档的工具，特别是用于创建和管理Obsidian的wikilinks和标签。它提供了一系列类和方法，帮助用户在Markdown文档中识别、创建和插入wikilinks，以及提取和添加标签。

以下是一些关键功能：

1. **WikiLink类**：用于表示Obsidian的wikilink，提供了验证和获取目标路径的方法。

2. **WikiLinkFactory类**：用于从文本或目标名称创建WikiLink对象。

3. **ILinkGenerationStrategy接口及其实现**：定义了生成wikilink的策略接口，并提供了基于关键词和相似度的策略实现。

4. **ObsidianMarkdownSDK类**：提供了一个简化的接口，用于与Obsidian Markdown文档交互。它支持读取和写入Markdown文件、查找和插入wikilinks、重构内容为wikilink、提取文档部分、查找和添加标签等操作。

总体而言，这个包为用户提供了一个强大的工具集，帮助他们更高效地管理和构建Obsidian笔记中的知识网络。通过使用不同的链接生成策略，用户可以根据自己的需求自动化地生成wikilinks
"""
            }
            
            engines = {}

            for name,path_list in path_lists.items():
                engines[name] = APIQueryEngine(
                                                qa_prompt=qa_prompt,
                                                llm = Settings.llm,
                                                input_files = path_list
                                            )

            api_query_engine_tools = []
            api_query_engine_tools_map = {}

            for engine_name, engine in engines.items():
                qetool = QueryEngineTool(
                    query_engine=engine,
                    metadata=ToolMetadata(
                        name=engine_name,
                        description=descript_dicts[engine_name],
                    ),
                )
                api_query_engine_tools.append(qetool)
                api_query_engine_tools_map[engine_name] = qetool

            agent = ReActAgent(
                tools=api_query_engine_tools,
                # llm=OpenAI(model="gpt-4o-mini"),
                # system_prompt="..."
            )

            handler = agent.run(prompt_with_history)
            async for ev in handler.stream_events():
                if isinstance(ev, AgentStream):
                    # print(f"{ev.delta}", end="", flush=True)
                    yield f"{ev.delta}"


        elif model == "long_memory_v2_retriver":
            if not self.query:
                director = Director(BuilderFactory(BuilderType.CHAT_HISTORY_MEMORY_BUILDER))
                self.query = director.construct()
            if len(prompt_with_history.split('\n')) == 1:
                self.query.reload()

            relevant_memories = self.query.retrieve_search(prompt_no_history)
            memories_str = '\n'.join([i.metadata.get('docs') for i in relevant_memories])
            yield memories_str

        elif model == 'chat_with_long_memory_v2':
            """
            # 电脑 内存就是对应chat_history
            # 硬盘 + 内置硬盘 其实就是 大模型潜意识与知识库维度
            # 还要再加一些 寄存器的方式
            """
            logger.info(f"running {model}")

            self.bx.set_model("gemini-2.5-flash-preview-04-17-nothinking")
            system_prompt = ""
            if not self.query:
                director = Director(BuilderFactory(BuilderType.CHAT_HISTORY_MEMORY_BUILDER))
                self.query = director.construct()
            if len(prompt_with_history.split('\n')) == 1:
                self.query.reload()

            if prompt_no_history.startswith("上传记忆"):
                import datetime
                now = datetime.datetime.now()
                date_str_ymd = now.strftime("%Y-%m-%d %H:%M:%S")  # 年-月-日
                #TODO 安装最新版后更新
                # 上传记忆${'tags':"成功",'date':"date_str_ymd"}
                self.query.update(prompt_with_history,metadata = {"tags":'合格',"date":date_str_ymd})
                yield '上传完成'
            elif prompt_no_history.startswith('上传文章'):
                context = f"user: {prompt_no_history}\nassistant: 上传完成"
                print(context,'contextxxxxxxxx')
                self.query.update(context)
                yield '上传完成'
            else:
                with check_time("retriver_search_time",logger = logger):
                    relevant_memories = self.query.retrieve_search(prompt_no_history)
                    memories_str = '\n'.join([i.metadata.get('docs') for i in relevant_memories])
                    prompt = system_prompt +"\n"+ memories_str +"\n"+prompt_with_history
                time1 = time.time()
                for word in self.bx.product_stream(prompt):
                    logger.debug(f"first_tokens_time: {time.time()-time1}")
                    yield word
        elif model == 'chat_with_long_memory_v3':
            """
            # 电脑 内存就是对应chat_history
            # 硬盘 + 内置硬盘 其实就是 大模型潜意识与知识库维度
            # 还要再加一些 寄存器的方式
            """
            logger.info(f"running {model}")

            self.bx.set_model("gemini-2.5-flash-preview-04-17-nothinking")
            system_prompt = ""
            if not self.query:
                director = Director(BuilderFactory(BuilderType.CHAT_HISTORY_MEMORY_BUILDER))
                self.query = director.construct()
            if len(prompt_with_history.split('\n')) == 1:
                self.query.reload()

            if prompt_no_history.startswith("上传记忆"):
                import datetime
                now = datetime.datetime.now()
                date_str_ymd = now.strftime("%Y-%m-%d %H:%M:%S")  # 年-月-日
                #TODO 安装最新版后更新
                # 上传记忆${'tags':"成功",'date':"date_str_ymd"}
                self.query.update(prompt_with_history,metadata = {"tags":'合格',"belong":self.user,"date":date_str_ymd})
                yield '上传完成'
            elif prompt_no_history.startswith('上传文章'):
                context = f"user: {prompt_no_history}\nassistant: 上传完成"
                print(context,'contextxxxxxxxx')
                self.query.update(context)
                yield '上传完成'
            elif prompt_no_history.startswith('登录:'):
                user = prompt_no_history.replace("登录:",'')
                self.user = user
            else:
                with check_time("retriver_search_time",logger = logger):
                    relevant_memories = self.query.retrieve_search(prompt_no_history)
                    memories_str = '\n'.join([i.metadata.get('docs') for i in relevant_memories])
                    prompt = system_prompt +"\n"+ memories_str +"\n"+prompt_with_history
                time1 = time.time()
                for word in self.bx.product_stream(prompt):
                    logger.debug(f"first_tokens_time: {time.time()-time1}")
                    yield word

        elif model == 'Custom_Agent_Latest':
            logger.info(f"running {model}")

            yield "TODO"


        else:
            yield 'pass'

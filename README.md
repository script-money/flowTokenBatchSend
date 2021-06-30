# Flow群发脚本

从表格读取比例发放FlowToken。

`pip install -r requirements.txt` 安装依赖

.env.example重命名，然后填入自己的账户和私钥（私钥导出参考[Flow 主网命令行转账步骤](https://script.money/posts/027-flow_mainnet_cli_transaction/) ）

修改send_multiple的参数，然后`python send_multiple.py`发起转账交易

> 余额查询 [https://flowscan.org/](https://flowscan.org/)
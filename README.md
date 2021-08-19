# Flow 群发脚本

从表格读取比例发放 FlowToken。

`pip install -r requirements.txt` 安装依赖

.env.example 重命名去掉 example，然后填入自己的账户和私钥（私钥导出参考[Flow 主网命令行转账步骤](https://script.money/posts/027-flow_mainnet_cli_transaction/) ）

flow_test.csv.example 重命名去掉 example, 编辑要发送各地址的比例

`python send_multiple.py [转账的总数]`发起转账交易

> 余额查询 [https://flowscan.org/](https://flowscan.org/)

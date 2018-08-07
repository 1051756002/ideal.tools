#!/usr/bin/python3

from ideal.config import *;
from handle.index import *;

# 帮助文档
def doCmdToHelp():
	print(
		'  ** ideal框架辅助工具 **\n'
		'  *                     *\n'
		'  *  项目构建 - build   *\n'
		'  *  指令说明 - help    *\n'
		'  *  退出系统 - exit    *\n'
		'  *  工具版本 - version *\n'
		'  *                     *\n'
		'  ***********************'
	);

# 退出系统
def doCmdToExit():
	exit();

# 查看版本
def doCmdToVersion():
	print('Version: {0}'.format(ideal['version']));

# 构建项目
def doCmdToBuild(argvs):
	handleBuild(argvs);

def mainLoop():
	while True:
		ipt_cmd = input("指令: ");
		ipt_cmd = ipt_cmd.strip();

		if len(ipt_cmd) == 0: continue;

		process = ipt_cmd.split();
		mainCmd = process[0];

		if mainCmd == 'build':
			doCmdToBuild(process[1:]);
		elif mainCmd == 'version':
			doCmdToVersion();
		elif mainCmd == 'help':
			doCmdToHelp();
		elif mainCmd == 'exit':
			doCmdToExit();
mainLoop();

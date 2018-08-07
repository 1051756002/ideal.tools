import time;
from ideal.config import *;
from .build_h5 import *;
from .build_wxgame import *;

# 处理构建工作
def handleBuild(argvs):
	# ipt_cmd = input('构建平台[h5|wxgame]:  请输入构建平台 (h5 | wxgame): ');

	i = 0;
	build_type = ideal['ud']['build_type'];
	build_src = ideal['ud']['build_src'];
	build_dest = ideal['ud']['build_dest'];

	while i < len(argvs):
		if argvs[i] in ['-t', '--type']:
			build_type = argvs[i + 1];
			i += 2;
		elif argvs[i] in ['-s', '--src']:
			build_src = argvs[i + 1];
			i += 2;
		elif argvs[i] in ['-d', '--dest']:
			build_dest = argvs[i + 1];
			i += 2;
		else:
			i += 1;

	if build_type in ['h5', 'wxgame']:
		print('构建平台 =>', build_type);
		print('项目地址 =>', build_src);
		print('发布地址 =>', build_dest);

		setUserData('build_type', build_type);
		setUserData('build_src', build_src);
		setUserData('build_dest', build_dest);

		if build_type == 'h5':
			buildToH5();
		elif build_type == 'wxgame':
			buildToWxGame();
	else:
		print('暂不支持"{0}"平台的构建'.format(build_type));


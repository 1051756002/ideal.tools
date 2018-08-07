import re;
import os, shutil;
from ideal.config import *;

def buildToH5():
	tools_path = ideal['creator_path'];
	build_src = ideal['ud']['build_src'];
	dest_path = ideal['ud']['build_dest'];

	build_arr = dict(
		platform = 'build_type',
		md5Cache = 'build_md5',
		buildPath = 'build_dest',
		title = 'build_title'
	);

	build_str = '';
	for key in build_arr:
		val = ideal['ud'][build_arr[key]];
		if key == 'platform':
			if val == 'h5':
				val = 'web-mobile';
			elif val == 'wxgame':
				val = 'wechatgame';
		build_str += '{0}={1};'.format(key, val);

	# 清空生成目录
	print('正在清空生成目录...');
	cleanPath(dest_path);

	print('正在构建项目, 请耐心等候...');
	prepcmd = '{0} --path "{1}" --build "{2}"'.format(tools_path, build_src, build_str);
	matchs = re.findall(r'Built to "(.*?)" successfully', os.popen(prepcmd).read());

	if matchs:
		print('正在处理生成文件...');
		_doFile(os.path.join(dest_path, 'web-mobile/'));
		print('构建成功!');
	else:
		print('构建失败!');

def cleanPath(path, removeself=False):
	files = os.listdir(path);
	for file in files:
		filepath = os.path.join(path, file);
		if os.path.isfile(filepath):
			os.remove(filepath);
		else:
			cleanPath(filepath, True);
	if removeself == True:
		os.rmdir(path);

# 处理宏定义
def doIdealMacro(temp, attr):
	def replaceFn(reg):
		key = reg.group('key');
		value = reg.group('value');
		if key in attr and attr[key] == True:
			return reg.group('value').strip();
		else:
			return '';

	return re.sub(r'@ideal\.define\((?P<key>.*?)\)(?P<value>.*?)@ideal.undef', replaceFn, temp, flags=re.S|re.M);

# 处理模板定义
def doIdealTemplate(temp, attr):
	def replaceFn(reg):
		key = reg.group('key');
		if key in attr:
			return attr[key];
		else:
			return '';

	return re.sub(r'@ideal\.temp\((?P<key>.*?)\)', replaceFn, temp, flags=re.S|re.M);

# 复原MD5文件名
def _filterMD5FileName(filepath):
	newfilepath = re.sub(r'([a-z|0-9]*?)\.[0-9|a-z]*?\.js', r'\1.js', filepath);
	os.rename(filepath, newfilepath);
	return newfilepath;

# index.html
def _doFileToIndex(filepath):
	temppath = os.path.abspath('./template/build_h5/index.php');
	fr = open(temppath, 'r', encoding='utf-8');
	readlines = fr.readlines();
	fr.close();

	tempcontent = ''.join(readlines);
	usedcontent = doIdealMacro(tempcontent, { "EnableEruda": True });
	usedcontent = doIdealTemplate(usedcontent, { 'title': '爱摩罗棋牌，精彩只为等你来！' });

	fw = open(filepath, 'w', encoding='utf-8');
	fw.write(usedcontent);
	fw.close();

	_filterMD5FileName(filepath);
	os.rename(filepath, filepath[:-5] + '.php');

	print('[finish the work] ./index.php');

# main.js
def _doFileToMain(filepath):
	temppath = os.path.abspath('./template/build_h5/main.js');
	fr = open(temppath, 'r', encoding='utf-8');
	readlines = fr.readlines();
	fr.close();

	def replaceFn(reg):
		prepcode = 'echo ' + reg.group('code');
		return os.popen(prepcode).read()[0:-1];

	tempcontent = ''.join(readlines);
	usedcontent = re.sub(r'@ideal.code\((?P<code>.*)\)', replaceFn, tempcontent, re.M);

	fw = open(filepath, 'w', encoding='utf-8');
	fw.write(usedcontent);
	fw.close();

	_filterMD5FileName(filepath);

	print('[finish the work] ./main.js');

# ./src
def _doFileToSrc(filepath):
	files = os.listdir(filepath);
	for file in files:
		# 文件完整地址
		fpath = os.path.join(filepath, file);
		# 过滤MD5文件名
		fpath = _filterMD5FileName(fpath);

		print('[finish the work] ./src/' + re.sub(r'([a-z|0-9]*?)\.[0-9|a-z]*?\.js', r'\1.js', file));

def _doFile(destpath):
	files = os.listdir(destpath);
	# 需要保留的文件
	retains = ['res', 'src', 'main.js', 'index.html'];

	for file in files:
		filepath = os.path.join(destpath, file);

		if file not in retains:
			os.remove(filepath);
		elif file == 'src':
			_doFileToSrc(filepath);
		elif re.search(r'index[\.|0-9|a-z]*?\.html', file):
			_doFileToIndex(filepath);
		elif re.search(r'main[\.|0-9|a-z]*?\.js', file):
			_doFileToMain(filepath);

	files = os.listdir(destpath);
	for file in files:
		filepath = os.path.join(destpath, file);
		shutil.move(filepath, ideal['ud']['build_dest']);
	os.rmdir(destpath);

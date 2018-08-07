import os;
import win32file;
import win32con;

# 工具版本号
__version = '1.0.0 beta';
# 用户数据
__user_data = dict();
# 用户数据文件路径
__user_data_path = './ideal/user.data';
# Creator工具路径
__creator_path = '';


# 初始化用户数据文件
if os.path.exists(__user_data_path) == False:
	fw = open(__user_data_path, 'w', encoding='utf-8');
	fw.write('build_type = h5\n');
	fw.write('build_src = E:/svn/h5_framework/\n');
	fw.write('build_dest = F:/Users/home/Desktop/dest/\n');
	fw.write('build_md5 = 0\n');
	fw.write('build_title = h5_framework\n');
	fw.close();

# 搜索指定路径
def __searchPath(path):
	for fname in os.listdir(path):
		attr_code = win32file.GetFileAttributes(path + fname);
		if attr_code & win32con.FILE_ATTRIBUTE_HIDDEN:
			continue;
		if os.path.isdir(path + fname):
			return __searchPath(path + fname + '/');
		elif fname == 'CocosCreator.exe':
			return path + fname;
	return False;

# 初始化Ceator工具路径
for i in range(97, 97 + 26):
	path = chr(i) + ':/';
	if os.path.isdir(path):
		f = __searchPath(path);
		if f != False:
			__creator_path = f;
			break;

if len(__creator_path) == 0:
	print('警告: 未检测到Creator工具, 可能会导致部分功能无法使用.');


# 初始化用户数据
def initUserData():
	fr = open(__user_data_path, 'r', encoding='utf-8');
	readlines = fr.readlines();
	fr.close();
	for line in readlines:
		if line.endswith('\n'):
			line = line[0:-1];
		line2 = line.split('=');
		key = line2[0].strip();
		val = line2[1].strip();
		__user_data[key] = val;

# 设置用户数据
def setUserData(key, val):
	fr = open(__user_data_path, 'r', encoding='utf-8');
	readlines = fr.readlines();
	fr.close();

	added = True;
	bakLines = [];
	for line in readlines:
		line2 = line.split('=');
		k = line2[0].strip();
		v = line2[1].strip();
		if k == key: v = val; added = False;
		bakLines.append('{0} = {1}\n'.format(k, v));

	if added == True:
		bakLines.append('{0} = {1}\n'.format(key, val));

	fw = open(__user_data_path + '.bak', 'w', encoding='utf-8');
	fw.writelines(bakLines);
	fw.close();

	os.remove(__user_data_path);
	os.rename(__user_data_path + '.bak', __user_data_path);

	__user_data[key] = val;

ideal = dict(
	version = __version,
	creator_path = __creator_path,
	ud = __user_data,
);

initUserData();

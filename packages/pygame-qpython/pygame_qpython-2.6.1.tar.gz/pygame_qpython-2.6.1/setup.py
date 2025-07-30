import os,shutil
from time import time
from setuptools import setup, find_packages
swp=__file__[:__file__.rfind('/')+1]+'libs/'
src='/data/data/org.qpython.plus/files'
dst=os.environ.get('HOME') or '/'

count=0;total=24655
size=0;max=933329742
getsize=os.path.getsize
i=0
copy2=shutil.copy2
def copy3(Src,Dst):
    global count,size,i
    copy4(Src,Dst)
    count+=1
    size+=getsize(Src)
    t=time()
    if t-i>=1:
        print('\033[1;35;40m%7.3f%%\033[0m\033[1A'%(min(count/total,size/max)*100))
        i=t
def copy4(Src,Dst):
    try:
        cont=open(Src).read()
        cont=cont.replace(src,dst)
        open(Dst,'w').write(cont)
    except:
        copy2(Src,Dst)

if src==dst:
    copy4=copy2

print('Copying in Progress ……')
try:
    shutil.copytree(swp,dst,dirs_exist_ok=True,copy_function=copy3)
except:
    pass
print('\033[KDone .\n')

long_description="""
Pygame for qpython
"""
current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    pass

setup(name='pygame-qpython',
      version='2.6.1',
      description='Pygame for QPython',
      author='The QPYPI Team',
      author_email='qpypi@qpython.org',
      url='https://pypi.org/project/pygame-qpython/',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Android",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.12",
            "Topic :: Software Development",
        ],
      license="Apache Software License (Apache 2.0)",
      install_requires=['pillow-qpython'],
      python_requires='==3.12.*'
     )
print('\nPlease check \033[1;36;40mXServer_XSDL_QPython.apk\033[0m is installed before you can test \033[1;36;40mpygame\033[0m and \033[1;36;40mopencv\033[0m image show .')